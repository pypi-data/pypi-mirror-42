from __future__ import unicode_literals

import collections
import json
import requests

import httmock
import mock
import pytest

from httmock import HTTMock
from psys import Error
from six import text_type as str

from pyscaleio import exceptions
from pyscaleio.client import ScaleIOSession, ScaleIOClient
from pyscaleio.manager import ScaleIOClientsManager
import pyscaleio.client
import pyscaleio.models


@pytest.fixture(scope="function")
def manager(request):
    m = ScaleIOClientsManager()
    request.addfinalizer(m.deregister)
    return m


@pytest.fixture(scope="function")
def mock_session(request):
    def generate_session(*args, **kwargs):
        if not args:
            args = ("localhost", "admin", "passwd")
        return ScaleIOSession(*args, **kwargs)
    return generate_session


@pytest.fixture(scope="function")
def mock_client(request):
    def generate_client(*args, **kwargs):
        if not args:
            args = ("localhost", "admin", "passwd")
        return ScaleIOClient.from_args(*args, **kwargs)
    return generate_client


@httmock.urlmatch(path=r".*login")
@httmock.remember_called
def login_payload(url, request):
    return httmock.response(200,
        json.dumps("some_random_token_string"),
        request=request
    )


@httmock.urlmatch(path=r".*logout")
@httmock.remember_called
def logout_payload(url, request):
    return httmock.response(200)


@httmock.urlmatch(path=r".*/api/version$", method="get")
def version_payload(url, request):
    return httmock.response(200, json.dumps(
        pyscaleio.client.__api_version__
    ), request=request)


@httmock.urlmatch(path=r".*/api/instances$", method="get")
def all_instances_payload(url, request):
    return httmock.response(200, {
        "resourceList": [1, 2],
    }, request=request)


def mock_instances_payload(resource, payload):
    path = r".*/api/types/{0}/instances".format(resource)

    @httmock.urlmatch(path=path, method="get")
    @httmock.remember_called
    def instances_of_payload(url, request):
        return httmock.response(200,
            json.dumps(payload), request=request)
    return instances_of_payload


@httmock.urlmatch(path=r".*/types/(\w+)/instances", method="post")
def create_instance_payload(url, request):
    return httmock.response(201, {"id": "test"}, request=request)


@pytest.mark.parametrize(("is_secure", "scheme"), [
    (True, "https"), (False, "http")
])
def test_session_initialize(mock_session, is_secure, scheme):

    client = mock_session(is_secure=is_secure)
    assert client.host == "localhost"
    assert client.user == "admin"
    assert client.passwd == "passwd"

    assert not client.token
    assert isinstance(
        client._ScaleIOSession__session,
        requests.Session)
    headers = client._ScaleIOSession__session.headers
    assert "Accept" in headers
    assert headers["Accept"] == "application/json; version=2.0"
    assert headers["Content-Type"] == "application/json"

    assert client.endpoint == "{0}://localhost/api/".format(scheme)


def test_session_login_positive(mock_session):

    client = mock_session()
    assert not client.token
    assert not client._ScaleIOSession__session.auth

    with HTTMock(login_payload):
        client.login()

    assert client.token == "some_random_token_string"
    assert client._ScaleIOSession__session.auth == ("admin", "some_random_token_string")


@pytest.mark.parametrize(("code", "message", "exc"), [
    (401, "Unauthorized", exceptions.ScaleIOAuthError),
    (500, "Server error", requests.HTTPError)
])
def test_session_login_negative(mock_session, code, message, exc):

    @httmock.urlmatch(path=r".*login")
    def login_payload(url, request):
        return httmock.response(code,
            json.dumps({
                "message": message,
                "httpStatusCode": code,
                "errorCode": 0
            }), request=request)

    client = mock_session()
    assert not client.token
    assert not client._ScaleIOSession__session.auth

    with HTTMock(login_payload):
        with pytest.raises(exc) as e:
            client.login()

    if isinstance(e, exceptions.ScaleIOError):
        assert e.status_code == code
        assert e.error_code == 0
        assert str(e) == message

    assert not client.token
    assert not client._ScaleIOSession__session.auth


def test_session_send_request(mock_session):

    @httmock.urlmatch(path=r"/api/test/instance")
    def request_payload(url, request):
        return httmock.response(200,
            json.dumps({"response": "test"}),
            request=request
        )

    client = mock_session()
    client.token = "some_token"

    with HTTMock(request_payload):
        result = client.get("test/instance")

    assert result == {"response": "test"}


@pytest.mark.parametrize(("effect", "result", "retries"), [
    (
        [
            (401, {"message": "Unauthorized", "httpStatusCode": 401}),
            (200, {"response": "test"})
        ],
        {"response": "test"}, 2
    ),
    (
        [
            (401, {"message": "Unauthorized", "httpStatusCode": 401}),
            (401, {"message": "Unauthorized", "httpStatusCode": 401}),
            (200, {"response": "test"})
        ],
        {"response": "test"}, 3
    )
])
def test_session_send_request_retries(mock_session, effect, result, retries):

    mock_handler = mock.Mock(side_effect=effect)

    @httmock.all_requests
    @httmock.remember_called
    def request_payload(url, request):
        code, payload = mock_handler()
        return httmock.response(code, json.dumps(payload),
            request=request
        )

    client = mock_session()
    client.token = "expired_token"

    with HTTMock(login_payload, request_payload):
        real_result = client.get("test/instance")

    assert real_result == result
    assert mock_handler.call_count == retries
    assert client.token == "some_random_token_string"

    assert login_payload.call["count"] == retries - 1
    assert request_payload.call["count"] == retries


def test_session_send_request_with_login(mock_session):

    @httmock.all_requests
    def api_payload(url, request):
        return httmock.response(200, json.dumps({"response": "test"}))

    client = mock_session()

    with HTTMock(login_payload, api_payload):
        result = client.get("test/instance")

    assert result == {"response": "test"}
    assert client.token == "some_random_token_string"


def test_session_send_request_negative(mock_session):

    @httmock.all_requests
    def api_exception(url, request):
        return httmock.response(500, json.dumps({
            "message": "Server error",
            "httpStatusCode": 500,
            "errorCode": 0
        }))

    client = mock_session()
    assert not client.token

    with HTTMock(login_payload, api_exception):
        with pytest.raises(exceptions.ScaleIOError) as e:
            client.get("test/instance")

    exc = e.value
    assert exc.status_code == 500
    assert exc.error_code == 0
    assert "code=500" in str(exc)
    assert "message=Server error" in str(exc)


def test_session_send_request_malformed(mock_session):

    @httmock.urlmatch(path=r"/api/test/instance")
    def request_payload(url, request):
        return httmock.response(200,
            "<?xml version='1.0' encoding='UTF-8'?>",
            request=request
        )

    client = mock_session()
    client.token = "some_token"

    with HTTMock(request_payload):
        with pytest.raises(exceptions.ScaleIOMalformedError):
            client.get("test/instance")


def test_session_logout(mock_session):

    client = mock_session()
    assert not client.token

    with HTTMock(logout_payload):
        client.logout()
    assert not logout_payload.call["called"]

    with HTTMock(login_payload, logout_payload):
        client.login()
        assert client.token

        client.logout()

    assert not client.token


def test_client_initialize(mock_session):

    with pytest.raises(Error) as e:
        ScaleIOClient(object())

    assert "must be initialized with ScaleIOSession" in str(e)

    client = ScaleIOClient(mock_session())
    assert client
    assert isinstance(client, ScaleIOClient)

    assert client.session
    assert isinstance(client.session, ScaleIOSession)

    with HTTMock(login_payload, version_payload):
        result = client.get_version()
        assert isinstance(result, float)
        assert result == pyscaleio.client.__api_version__


def test_client_getters(mock_client):

    client = mock_client()

    with HTTMock(login_payload, all_instances_payload):
        result = client.get_all_instances()
        assert isinstance(result, collections.MutableMapping)
        assert "resourceList" in result
        assert isinstance(result["resourceList"], list)

    instances_of_payload = mock_instances_payload(
        "Resource", [{"field": 1}, {"field": 2}]
    )
    with HTTMock(login_payload, instances_of_payload):
        result = client.get_instances_of("Resource")
        assert result
        assert isinstance(result, list)


def test_client_create_instance(mock_client):

    client = mock_client()

    with HTTMock(login_payload, create_instance_payload):
        instance_id = client.create_instance_of(
            "Volume", {"name": "test_volume"})
        assert isinstance(instance_id, str)
        assert instance_id == "test"


def test_client_lazy_get_system(mock_client):

    client = mock_client()

    systems_payload = mock_instances_payload(
        "System", [{"id": "test", "name": "test_name"}]
    )
    with HTTMock(login_payload, systems_payload):
        with mock.patch("pyscaleio.models.System.__scheme__", {}):
            result = client.system

            assert systems_payload.call["called"]
            assert systems_payload.call["count"] == 1

            assert isinstance(result, pyscaleio.models.System)
            assert result["id"] == "test"

            second_result = client.system
            assert result == second_result

            assert systems_payload.call["count"] == 1


def test_client_manager_register(manager):

    assert manager is ScaleIOClientsManager()

    client = ScaleIOClient.from_args("localhost", "admin", "passwd")
    manager.register(client)

    assert manager.clients
    assert len(manager.clients) == 1
    assert client.session.host in manager.clients

    assert manager.default is client

    registered_client = manager.get_client()
    assert registered_client is client

    manager.deregister("localhost")
    assert not manager.clients


def test_client_manager_register_negative(manager):

    assert manager is ScaleIOClientsManager()

    client = ScaleIOClient.from_args("localhost", "admin", "passwd")

    with pytest.raises(exceptions.ScaleIOEmptyClientRegistry):
        manager.get_client()

    with pytest.raises(exceptions.ScaleIOClientNotRegistered):
        manager.get_client("localhost")

    with pytest.raises(exceptions.ScaleIOInvalidClient):
        manager.register(object())

    client = ScaleIOClient.from_args("localhost", "admin", "passwd")
    manager.register(client)
    with pytest.raises(exceptions.ScaleIOClientAlreadyRegistered):
        manager.register(client)


def test_model_inject_client(manager, mock_client):

    manager.register(mock_client("localhost", "admin", "passwd"))

    assert pyscaleio.client._get_client({}) == pyscaleio.get_client()
    assert pyscaleio.client._get_client({"host": "localhost"}) == pyscaleio.get_client()

    second_client = mock_client("test_host", "admin", "passwd")
    assert pyscaleio.client._get_client({"client": second_client}) == second_client


def test_model_inject_client_negative():

    with pytest.raises(exceptions.ScaleIONotBothParameters):
        pyscaleio.client._get_client({"client": "test", "host": "test"})

    with pytest.raises(exceptions.ScaleIOInvalidClient):
        pyscaleio.client._get_client({"client": "test"})
