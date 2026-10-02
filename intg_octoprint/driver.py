"""
OctoPrint driver for Unfolded Circle Remote.

:copyright: (c) 2026 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

import logging
from typing import Any

from ucapi import Entity, button
from ucapi_framework import BaseIntegrationDriver
from intg_octoprint.config import OctoPrintConfig
from intg_octoprint.device import OctoPrintDevice
from intg_octoprint.button import (
    OctoPrintPauseButton,
    OctoPrintResumeButton,
    OctoPrintStopButton,
    OctoPrintHomeButton,
    OctoPrintConnectButton,
    OctoPrintDisconnectButton,
)
from intg_octoprint.remote import OctoPrintRemote
from intg_octoprint.sensor import (
    OctoPrintStatusSensor,
    OctoPrintProgressSensor,
    OctoPrintTimeRemainingSensor,
    OctoPrintFileSensor,
    OctoPrintConnectionSensor,
)

_LOG = logging.getLogger(__name__)

# Entity IDs are "<type>.<device id>_<suffix>" (remote: "remote.<device id>").
_ENTITY_SUFFIXES = (
    "_time_remaining",
    "_connection",
    "_disconnect",
    "_progress",
    "_connect",
    "_status",
    "_resume",
    "_pause",
    "_stop",
    "_home",
    "_file",
)


class OctoPrintDriver(BaseIntegrationDriver[OctoPrintDevice, OctoPrintConfig]):
    """OctoPrint integration driver."""

    def __init__(self):
        super().__init__(
            device_class=OctoPrintDevice,
            entity_classes=[
                OctoPrintPauseButton,
                OctoPrintResumeButton,
                OctoPrintStopButton,
                OctoPrintHomeButton,
                OctoPrintConnectButton,
                OctoPrintDisconnectButton,
                OctoPrintRemote,
                OctoPrintStatusSensor,
                OctoPrintProgressSensor,
                OctoPrintTimeRemainingSensor,
                OctoPrintFileSensor,
                OctoPrintConnectionSensor,
            ],
            driver_id="octoprint",
        )

    def map_device_state(self, device_state: Any) -> Any:
        """Keep button states intact.

        The framework maps entity states through the media player state set,
        which turns the button state AVAILABLE into UNKNOWN.
        """
        if str(device_state) in (button.States.AVAILABLE.value, button.States.UNAVAILABLE.value):
            return button.States(str(device_state))
        return super().map_device_state(device_state)

    def device_from_entity_id(self, entity_id: str) -> str | None:
        """Return the device identifier for an entity ID.

        The framework default takes the part after the first "." as the device,
        which for "button.<device id>_pause" would include the suffix.
        """
        if not entity_id or "." not in entity_id:
            return None
        rest = entity_id.split(".", 1)[1]
        for suffix in _ENTITY_SUFFIXES:
            if rest.endswith(suffix):
                return rest[: -len(suffix)]
        return rest

    def create_entities(
        self, device_config: OctoPrintConfig, device: OctoPrintDevice
    ) -> list[Entity]:
        """Create entity instances."""
        _LOG.info("Creating entities for %s", device_config.name)
        return [
            OctoPrintPauseButton(device_config, device),
            OctoPrintResumeButton(device_config, device),
            OctoPrintStopButton(device_config, device),
            OctoPrintHomeButton(device_config, device),
            OctoPrintConnectButton(device_config, device),
            OctoPrintDisconnectButton(device_config, device),
            OctoPrintRemote(device_config, device),
            OctoPrintStatusSensor(device_config, device),
            OctoPrintProgressSensor(device_config, device),
            OctoPrintTimeRemainingSensor(device_config, device),
            OctoPrintFileSensor(device_config, device),
            OctoPrintConnectionSensor(device_config, device),
        ]
