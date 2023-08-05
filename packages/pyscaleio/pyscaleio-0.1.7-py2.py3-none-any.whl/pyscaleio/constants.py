from __future__ import unicode_literals

"""Common constants."""

KILOBYTE = 1024
"""Bytes in kilobyte."""

MEGABYTE = 1024 * KILOBYTE
"""Bytes in megabyte."""

GIGABYTE = 1024 * MEGABYTE
"""Bytes in gigabyte."""

TERABYTE = 1024 * GIGABYTE
"""Bytes in terabyte."""


MINUTE_SECONDS = 60
"""Seconds in minute."""

HOUR_SECONDS = 60 * MINUTE_SECONDS
"""Seconds in hour."""

DAY_SECONDS = 24 * HOUR_SECONDS
"""Seconds in day."""

WEEK_SECONDS = 7 * DAY_SECONDS
"""Seconds in week."""

MONTH_SECONDS = 30 * DAY_SECONDS
"""Seconds in average month."""


VOLUME_TYPE_THIN = "ThinProvisioned"
"""Volume type with thin provisioning."""

VOLUME_TYPE_THICK = "ThickProvisioned"
"""Volume type with think provisioning."""

VOLUME_TYPE_SNAPSHOT = "Snapshot"
"""Volume type Snapshot."""

VOLUME_TYPES = [
    VOLUME_TYPE_THIN,
    VOLUME_TYPE_THICK,
    VOLUME_TYPE_SNAPSHOT,
]
"""Valid volume types."""


VOLUME_REMOVE_ONLY_ME = "ONLY_ME"
"""Remove only current volume."""

VOLUME_REMOVE_DESCENDANTS = "INCLUDING_DESCENDANTS"
"""Remove current volume with descendants."""

VOLUME_REMOVE_DESCENDANTS_ONLY = "DESCENDANTS_ONLY"
"""Remove only descendants of current volume."""

VOLUME_REMOVE_VTREE = "WHOLE_VTREE"
"""Remove whole VTree."""

VOLUME_REMOVE_MODES = [
    VOLUME_REMOVE_ONLY_ME,
    VOLUME_REMOVE_DESCENDANTS,
    VOLUME_REMOVE_DESCENDANTS_ONLY,
    VOLUME_REMOVE_VTREE,
]
"""Valid volume remove modes"""


SDC_MDM_STATE_CONNECTED = "Connected"
"""SDC MDM connected state."""

SDC_MDM_STATE_DISCONNECTED = "Disconnected"
"""SDC MDM disconnected state."""

SDC_MDM_STATES = [
    SDC_MDM_STATE_CONNECTED,
    SDC_MDM_STATE_DISCONNECTED,
]
"""Valid SDC MDM connection states."""
