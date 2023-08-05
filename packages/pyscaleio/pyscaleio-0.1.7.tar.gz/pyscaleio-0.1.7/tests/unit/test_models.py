from __future__ import unicode_literals

import json
import psys
import six
import uuid

import mock
import pytest
import httmock

from collections import Sequence
from object_validator import String, Integer, DictScheme
from six import text_type as str

import pyscaleio
from pyscaleio import constants
from pyscaleio import exceptions

from pyscaleio import ScaleIOClient
from pyscaleio.manager import ScaleIOClientsManager
from pyscaleio.models import BaseResource, Sdc, StoragePool, System
from pyscaleio.models import Volume, ExportsInfo


@pytest.fixture
def client(request):

    client = ScaleIOClient.from_args("localhost", "admin", "passwd")
    pyscaleio.add_client(client)
    request.addfinalizer(ScaleIOClientsManager().deregister)
    return client


@pytest.fixture
def modelklass(request):

    def generate_klass(name, subclasses, dict):
        if six.PY2:
            name = psys.b(name)
        else:
            name = psys.u(name)
        return type(name, subclasses, dict)
    return generate_klass


@httmock.urlmatch(path=r".*login")
def login_payload(url, request):
    return httmock.response(200,
        json.dumps("some_random_token_string"),
        request=request
    )


def mock_resource_get(resource, resource_id, payload):
    path = r".*/api/instances/{0}::{1}".format(resource, resource_id)

    @httmock.urlmatch(path=path, method="get")
    def instance_of_payload(url, request):
        return httmock.response(200, payload, request=request)
    return instance_of_payload


def mock_resources_get(resource, payload):
    path = r".*/api/types/{0}/instances".format(resource)

    @httmock.urlmatch(path=path, method="get")
    def instances_of_payload(url, request):
        return httmock.response(200, payload, request=request)
    return instances_of_payload


def mock_volume(override=None):
    volume_model = {
        "id": str(uuid.uuid4()),
        "sizeInKb": (8 * constants.GIGABYTE) // constants.KILOBYTE,
        "storagePoolId": str(uuid.uuid4()),
        "useRmcache": False,
        "volumeType": constants.VOLUME_TYPE_THICK,
        "mappedSdcInfo": []
    }
    volume_model.update(override or {})
    return volume_model


def test_base_model_name(client):

    assert BaseResource.__resource__ is None
    with mock.patch("pyscaleio.models.BaseResource.__scheme__", {}):
        assert BaseResource._get_name() == "BaseResource"
        assert BaseResource(instance={})._get_name() == "BaseResource"

        with mock.patch(
            "pyscaleio.models.BaseResource.__resource__",
            "TestResourceName"
        ):
            assert BaseResource._get_name() == "TestResourceName"
            assert BaseResource(instance={})._get_name() == "TestResourceName"


@pytest.mark.parametrize(("name", "result"), [
    ("Volume", "Volume"), ("VTree", "VTree"),
    ("StoragePool", "StoragePool"), ("Sdc", "Sdc"),
])
def test_custom_model_name(client, modelklass, name, result):

    assert BaseResource.__resource__ is None
    with mock.patch("pyscaleio.models.BaseResource.__scheme__", {}):
        klass = modelklass(name, (BaseResource,), {"__scheme__": {}})
        assert klass._get_name() == result
        assert klass(instance={})._get_name() == result


@pytest.mark.parametrize("scheme", [
    {}, {"id": String()}
])
def test_base_model_scheme(client, modelklass, scheme):

    with mock.patch("pyscaleio.models.BaseResource.__scheme__", scheme):
        result = BaseResource._get_scheme()
        assert isinstance(result, DictScheme)
        assert result._DictScheme__scheme == scheme

        result = BaseResource(instance={"id": "test"})._get_scheme()
        assert isinstance(result, DictScheme)
        assert result._DictScheme__scheme == scheme


@pytest.mark.parametrize(("scheme", "data"), [
    ({"name": String()}, {"name": "test"}),
    (
        {"name": String(), "size": Integer()},
        {"name": "test", "size": 8 * constants.GIGABYTE}
    )
])
def test_custom_model_scheme(client, modelklass, scheme, data):

    base_scheme = {"id": String()}
    full_scheme = base_scheme
    full_scheme.update(scheme)

    data = data
    data.update({"id": "test_id"})

    with mock.patch(
        "pyscaleio.models.BaseResource.__scheme__",
        base_scheme
    ):
        klass = modelklass("Volume", (BaseResource,), {"__scheme__": scheme})
        result = klass._get_scheme()
        assert isinstance(result, DictScheme)
        assert result._DictScheme__scheme == full_scheme

        result = klass(instance=data)._get_scheme()
        assert isinstance(result, DictScheme)
        assert result._DictScheme__scheme == full_scheme


def test_model_initialize(client, modelklass):

    with mock.patch("pyscaleio.models.BaseResource.__scheme__", {}):
        klass = modelklass("Volume", (BaseResource,), {"__scheme__": {}})

        volume_id = "test"
        volume_payload = mock_resource_get(
            "Volume", volume_id, {"id": volume_id})
        with httmock.HTTMock(login_payload, volume_payload):
            assert klass() == {}
            assert len(klass()) == 0

            assert klass(instance_id=volume_id) == {"id": volume_id}

        assert klass(instance={"id": volume_id}) == {"id": volume_id}


def test_model_initialize_negative(client, modelklass):

    with mock.patch("pyscaleio.models.BaseResource.__scheme__", {}):
        klass = modelklass("Volume", (BaseResource,), {"__scheme__": {}})

        with pytest.raises(exceptions.ScaleIONotBothParameters):
            klass(instance_id="test", instance={"id": "test"})


def test_model_validation(client, modelklass):

    klass = modelklass("Volume", (BaseResource,), {
        "__scheme__": {
            "name": String()
        }
    })

    volume_payload = mock_resource_get("Volume", "test", {
        "id": "test",
        "name": "test_volume"
    })
    with httmock.HTTMock(login_payload, volume_payload):
        volume = klass("test")
        assert volume.get("id") == "test"
        assert volume.get("name") == "test_volume"


def test_model_validation_negative(client, modelklass):

    klass = modelklass("Volume", (BaseResource,), {
        "__scheme__": {
            "name": String()
        }
    })
    volume_payload = mock_resource_get("Volume", "test", {"id": "test"})
    with httmock.HTTMock(login_payload, volume_payload):
        with pytest.raises(exceptions.ScaleIOValidationError) as e:
            klass("test")
        assert "instance['name'] is missing" in str(e)


@pytest.mark.parametrize(("old_payload", "new_payload"), [
    (
        {"id": "test", "name": "test_volume"},
        {"id": "test", "name": "test_volume_changed"},
    ),
    (
        {"id": "test"},
        {"id": "test", "name": "test_volume"},
    ),
    (
        {"id": "test", "name": "test_volume"},
        {"id": "test"},
    )
])
def test_model_update(client, modelklass, old_payload, new_payload):

    klass = modelklass("Volume", (BaseResource,), {
        "__scheme__": {
            "name": String(optional=True)
        }
    })
    volume_payload = mock_resource_get("Volume", "test", old_payload)
    volume_update_payload = mock_resource_get("Volume", "test", new_payload)

    with httmock.HTTMock(login_payload, volume_payload):
        volume = klass("test")
        assert volume == old_payload

    with httmock.HTTMock(volume_update_payload):
        volume.update()
        assert volume == new_payload


def test_model_one(client, modelklass):

    klass = modelklass("Volume", (BaseResource,), {
        "__scheme__": {
            "name": String(optional=True)
        }
    })
    payload = {"id": "test", "name": "test_volume"}
    volume_payload = mock_resource_get("Volume", "test", payload)

    with httmock.HTTMock(login_payload, volume_payload):
        volume = klass.one("test")
        assert volume == payload


def test_model_all(client, modelklass):

    klass = modelklass("Volume", (BaseResource,), {
        "__scheme__": {
            "name": String(optional=True)
        }
    })
    payload = [{
        "id": "test{0}".format(i),
        "name": "test_volume{0}".format(i)
    } for i in range(1, 2 + 1)]
    volumes_payload = mock_resources_get("Volume", payload)

    with httmock.HTTMock(login_payload, volumes_payload):
        volumes = klass.all()
        assert len(volumes) == 2
        assert sorted(["test1", "test2"]) == sorted(v["id"] for v in volumes)


def test_model_all_by_ids(client, modelklass):

    klass = modelklass("Volume", (BaseResource,), {
        "__scheme__": {
            "name": String(optional=True)
        }
    })
    payload = [{
        "id": "test{0}".format(i),
        "name": "test_volume{0}".format(i)
    } for i in range(1, 3 + 1)]

    def mocked_action(name, action, args):
        return [item for item in payload if item["id"] in args["ids"]]

    with mock.patch(
        "pyscaleio.ScaleIOClient.perform_action_on_type",
        side_effect=mocked_action
    ):
        volumes = klass.all(instance_ids=["test2", "test3"])
        assert len(volumes) == 2

        volumes = klass.all(instance_ids="test2")
        assert len(volumes) == 1
        assert volumes[0]["id"] == "test2"


def test_volume_model(client):

    volume_payload = mock_resource_get(Volume._get_name(), "test",
        mock_volume({"id": "test"})
    )
    system_payload = mock_resources_get(System._get_name(), [{
        "id": "system"
    }])
    with httmock.HTTMock(login_payload, volume_payload, system_payload):
        volume = Volume("test")

        assert volume.name is None
        assert volume.size == 8 * constants.GIGABYTE
        assert volume.type == constants.VOLUME_TYPE_THICK
        assert isinstance(volume.exports, Sequence)
        assert not volume.exports

        with mock.patch("pyscaleio.models.System.__scheme__", {}):
            assert volume.path == "/dev/disk/by-id/emc-vol-system-test"


def test_volume_model_exports(client):

    volume_exports = [{
        "sdcId": "sdc01",
        "sdcIp": "127.0.0.1",
        "limitIops": 0,
        "limitBwInMbps": 0
    }]
    volume_payload = mock_resource_get(Volume._get_name(), "test",
        mock_volume({
            "id": "test",
            "mappedSdcInfo": volume_exports
        })
    )
    sdc_payloads = [mock_resource_get(Sdc._get_name(), sdc_id, {
        "id": sdc_id,
        "sdcIp": sdc_id,
        "sdcGuid": str(uuid.uuid4()),
        "sdcApproved": True,
        "mdmConnectionState": constants.SDC_MDM_STATE_CONNECTED,
    }) for sdc_id in ("sdc0{0}".format(i) for i in range(1, 3))]

    with httmock.HTTMock(login_payload, volume_payload):
        volume = Volume("test")

        assert volume.exports
        assert isinstance(volume.exports, (Sequence, ExportsInfo))

    with httmock.HTTMock(*sdc_payloads):
        sdc1 = Sdc("sdc01")
        sdc2 = Sdc("sdc02")

        assert sdc1 in volume.exports
        assert sdc2 not in volume.exports
        assert "some_string" not in volume.exports


@pytest.mark.parametrize(("kw", "result"), [
    ({"sdc_id": "test"}, {"sdcId": "test"}),
    ({"sdc_guid": "test"}, {"guid": "test"}),
    (
        {"sdc_id": "test", "multiple": True},
        {"sdcId": "test", "allowMultipleMappings": "TRUE"}
    ),
])
def test_volume_export(client, kw, result):

    with mock.patch("pyscaleio.models.Volume.__scheme__", {}):
        volume = Volume(instance={"id": "test", "links": []})

    with mock.patch("pyscaleio.ScaleIOClient.perform_action_on") as m:
        volume.export(**kw)
        m.assert_called_once_with("Volume", "test", "addMappedSdc", result)


@pytest.mark.parametrize(("kw", "result"), [
    ({"sdc_id": "test"}, {"sdcId": "test"}),
    ({"sdc_guid": "test"}, {"guid": "test"}),
    ({}, {"allSdcs": ""})
])
def test_volume_unexport(client, kw, result):

    with mock.patch("pyscaleio.models.Volume.__scheme__", {}):
        volume = Volume(instance={"id": "test", "links": []})

    with mock.patch("pyscaleio.ScaleIOClient.perform_action_on") as m:
        volume.unexport(**kw)
        m.assert_called_once_with("Volume", "test", "removeMappedSdc", result)


@pytest.mark.parametrize("method", ["export", "unexport"])
def test_volume_unexport_negative(client, method):

    with mock.patch("pyscaleio.models.Volume.__scheme__", {}):
        volume = Volume(instance={"id": "test", "links": []})

    with mock.patch("pyscaleio.ScaleIOClient.perform_action_on") as m:
        with pytest.raises(exceptions.ScaleIONotBothParameters):
            getattr(volume, method)(**{"sdc_id": "test", "sdc_guid": "test"})
        m.assert_not_called()


@pytest.mark.parametrize(("kw", "result"), [
    ({"sdc_id": "test", "iops": 1000}, {"sdcId": "test", "iopsLimit": "1000"}),
    ({"sdc_id": "test", "iops": 0}, {"sdcId": "test", "iopsLimit": "0"}),
    ({"sdc_guid": "test", "mbps": 2048}, {"guid": "test", "bandwidthLimitInKbps": "2097152"}),
    ({"sdc_guid": "test", "mbps": 0}, {"guid": "test", "bandwidthLimitInKbps": "0"})
])
def test_volume_throttle_positive(client, kw, result):

    with mock.patch("pyscaleio.models.Volume.__scheme__", {}):
        volume = Volume(instance={"id": "test", "links": []})

    with mock.patch("pyscaleio.ScaleIOClient.perform_action_on") as m:
        volume.throttle(**kw)
        m.assert_called_once_with("Volume", "test", "setMappedSdcLimits", result)


@pytest.mark.parametrize(("kw", "exception"), [
    ({"sdc_id": "test"}, exceptions.ScaleIORequiredParameters),
    ({"sdc_id": "test", "iops": 5}, exceptions.ScaleIOInvalidLimit),
    ({"sdc_id": "test", "mbps": 1024.5}, exceptions.ScaleIOInvalidLimit),
    ({"sdc_id": "test", "sdc_guid": "test_guid"}, exceptions.ScaleIONotBothParameters),
])
def test_volume_throttle_negative(client, kw, exception):

    with mock.patch("pyscaleio.models.Volume.__scheme__", {}):
        volume = Volume(instance={"id": "test", "links": []})

    with mock.patch("pyscaleio.ScaleIOClient.perform_action_on") as m:
        with pytest.raises(exception):
            volume.throttle(**kw)
        m.assert_not_called()


@pytest.mark.parametrize(("kw", "result"), [
    ({}, {}), ({"name": "test_snapshot"}, {"snapshotName": "test_snapshot"})
])
def test_volume_snapshot(client, kw, result):
    volume_data = {
        "id": "base_volume",
        "links": [],
        "volumeType": constants.VOLUME_TYPE_THIN,
        "useRmcache": False,
        "sizeInKb": 1048576,
        "storagePoolId": "pool_id"
    }
    volume = Volume(instance=volume_data)

    snapshot_data = volume_data.copy()
    snapshot_data.update({
        "id": "volume_snapshot",
        "volumeType": constants.VOLUME_TYPE_SNAPSHOT,
        "ancestorVolume": "base_volume",
    })
    snapshot_payload = mock_resource_get(Volume._get_name(),
        "volume_snapshot", snapshot_data)

    system_payload = mock_resources_get(System._get_name(), [{
        "id": "test", "restrictedSdcModeEnabled": True
    }])
    method_data = {
        "snapshotDefs": [dict({"volumeId": "base_volume"}, **result)]
    }
    with httmock.HTTMock(login_payload, system_payload, snapshot_payload):
        with mock.patch(
            "pyscaleio.ScaleIOClient.perform_action_on",
            side_effect=[{"volumeIdList": ["volume_snapshot"]}]
        ) as m:
            snapshot = volume.snapshot(**kw)
            m.assert_called_once_with("System", "test", "snapshotVolumes", method_data)

        assert isinstance(snapshot, Volume)
        assert snapshot.type == constants.VOLUME_TYPE_SNAPSHOT
        assert snapshot.get("ancestorVolume") == "base_volume"


@pytest.mark.parametrize(("kw", "result"), [
    ({"name": "test"}, {"name": "test"}),
    ({"rmcache": True}, {"useRmcache": True}),
    ({"thin": False}, {"volumeType": constants.VOLUME_TYPE_THICK}),
])
def test_volume_create(client, kw, result):

    args = (1, "test_pool")
    full_result = {
        "volumeSizeInKb": str(1048576),
        "storagePoolId": "test_pool",
        "volumeType": constants.VOLUME_TYPE_THIN,
    }
    full_result.update(result)

    with mock.patch("pyscaleio.models.MutableResource.create") as m:
        Volume.create(*args, **kw)
        m.assert_called_once_with(full_result)


def test_volume_one_by_name(client):

    volume_id = "test_id"
    volume_name = "test_name"

    volume_payload = mock_resource_get(Volume._get_name(), volume_id, {
        "id": volume_id,
        "name": volume_name
    })

    call_args = (Volume._get_name(), "queryIdByKey", {"name": volume_name})
    with mock.patch("pyscaleio.models.Volume.__scheme__", {}):
        with mock.patch(
            "pyscaleio.ScaleIOClient.perform_action_on_type",
            side_effect=[volume_id]
        ) as m:
            with httmock.HTTMock(login_payload, volume_payload):
                volume = Volume.one_by_name(volume_name)
            m.assert_called_once_with(*call_args)

            assert isinstance(volume, Volume)
            assert volume.name == volume_name
            assert volume["id"] == volume_id


@pytest.mark.parametrize(("kw", "result"), [
    ({"checksum": True}, {"checksumEnabled": "TRUE"}),
    ({"rfcache": True}, {"useRfcache": "TRUE"}),
    (
        {"checksum": True, "rfcache": True},
        {"checksumEnabled": "TRUE", "useRfcache": "TRUE"}
    ),
    ({"name": "test_pool"}, {"name": "test_pool"})
])
def test_storage_pool_create(client, kw, result):

    args = ("domain_id",)
    full_result = {
        "protectionDomainId": "domain_id",
        "checksumEnabled": "FALSE",
        "useRfcache": "FALSE",
    }
    full_result.update(result)

    with mock.patch("pyscaleio.models.MutableResource.create") as m:
        StoragePool.create(*args, **kw)
        m.assert_called_once_with(full_result)


def test_storage_pool_one_by_name(client):

    pool_id = "test_id"
    pool_name = "test_name"
    domain_id = "domain_id"
    domain_name = "domain_name"

    pool_payload = mock_resource_get(StoragePool._get_name(), pool_id, {
        "id": pool_id,
        "name": pool_name,
        "protectionDomainId": domain_id,
        "checksumEnabled": False,
        "useRfcache": False,
    })

    call_args = (StoragePool._get_name(), "queryIdByKey", {
        "name": pool_name,
        "protectionDomainName": domain_name,
    })
    with mock.patch(
        "pyscaleio.ScaleIOClient.perform_action_on_type",
        side_effect=[pool_id]
    ) as m:
        with httmock.HTTMock(login_payload, pool_payload):
            pool = StoragePool.one_by_name(pool_name, domain_name)
        m.assert_called_once_with(*call_args)

        assert isinstance(pool, StoragePool)
        assert pool.name == pool_name
        assert pool["id"] == pool_id
        assert pool.checksum_enabled is False
        assert pool.rfcache_enabled is False


def test_sdc_one_by_ip(client):

    sdc_id = "test_id"
    sdc_ip = "172.20.34.126"
    sdc_guid = str(uuid.uuid4()).upper()

    sdc_payload = mock_resource_get(Sdc._get_name(), sdc_id, {
        "id": sdc_id,
        "name": "test_sdc",
        "sdcIp": sdc_ip,
        "sdcGuid": sdc_guid,
        "sdcApproved": True,
        "mdmConnectionState": constants.SDC_MDM_STATE_CONNECTED,
    })

    call_args = (Sdc._get_name(), "queryIdByKey", {"ip": sdc_ip})
    with mock.patch(
        "pyscaleio.ScaleIOClient.perform_action_on_type",
        side_effect=[sdc_id]
    ) as m:
        with httmock.HTTMock(login_payload, sdc_payload):
            sdc = Sdc.one_by_ip(sdc_ip)
        m.assert_called_once_with(*call_args)

        assert isinstance(sdc, Sdc)
        assert sdc["id"] == sdc_id
        assert sdc.name == "test_sdc"
        assert sdc.ip == sdc_ip
        assert sdc.guid == sdc_guid
        assert sdc.is_approved
        assert sdc.is_connected
