"""
OctoPrint driver for Unfolded Circle Remote.

:copyright: (c) 2026 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

import logging
from ucapi import Entity
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
