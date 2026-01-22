"""
OctoPrint Sensor entities.

:copyright: (c) 2026 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

import logging
from ucapi.sensor import Sensor, Attributes, DeviceClasses
from intg_octoprint.config import OctoPrintConfig
from intg_octoprint.device import OctoPrintDevice

_LOG = logging.getLogger(__name__)


class OctoPrintStatusSensor(Sensor):
    """Sensor for printer status."""

    def __init__(self, device_config: OctoPrintConfig, device: OctoPrintDevice):
        """Initialize the status sensor."""
        self._device = device
        self._device_config = device_config

        entity_id = f"sensor.{device_config.identifier}_status"

        super().__init__(
            entity_id,
            f"{device_config.name} Status",
            [],
            {
                Attributes.STATE: "Unknown",
                Attributes.VALUE: None,
                Attributes.UNIT: None,
            },
        )


class OctoPrintProgressSensor(Sensor):
    """Sensor for print progress percentage."""

    def __init__(self, device_config: OctoPrintConfig, device: OctoPrintDevice):
        """Initialize the progress sensor."""
        self._device = device
        self._device_config = device_config

        entity_id = f"sensor.{device_config.identifier}_progress"

        super().__init__(
            entity_id,
            f"{device_config.name} Progress",
            [],
            {
                Attributes.STATE: "0%",
                Attributes.VALUE: 0,
                Attributes.UNIT: "%",
            },
        )


class OctoPrintTimeRemainingSensor(Sensor):
    """Sensor for estimated time remaining."""

    def __init__(self, device_config: OctoPrintConfig, device: OctoPrintDevice):
        """Initialize the time remaining sensor."""
        self._device = device
        self._device_config = device_config

        entity_id = f"sensor.{device_config.identifier}_time_remaining"

        super().__init__(
            entity_id,
            f"{device_config.name} Time Remaining",
            [],
            {
                Attributes.STATE: "Unknown",
                Attributes.VALUE: None,
                Attributes.UNIT: None,
            },
        )


class OctoPrintFileSensor(Sensor):
    """Sensor for current file name."""

    def __init__(self, device_config: OctoPrintConfig, device: OctoPrintDevice):
        """Initialize the file sensor."""
        self._device = device
        self._device_config = device_config

        entity_id = f"sensor.{device_config.identifier}_file"

        super().__init__(
            entity_id,
            f"{device_config.name} File",
            [],
            {
                Attributes.STATE: "No File",
                Attributes.VALUE: None,
                Attributes.UNIT: None,
            },
        )


class OctoPrintConnectionSensor(Sensor):
    """Sensor for connection state."""

    def __init__(self, device_config: OctoPrintConfig, device: OctoPrintDevice):
        """Initialize the connection sensor."""
        self._device = device
        self._device_config = device_config

        entity_id = f"sensor.{device_config.identifier}_connection"

        super().__init__(
            entity_id,
            f"{device_config.name} Connection",
            [],
            {
                Attributes.STATE: "Disconnected",
                Attributes.VALUE: "disconnected",
                Attributes.UNIT: None,
            },
            device_class=DeviceClasses.CUSTOM,
        )
