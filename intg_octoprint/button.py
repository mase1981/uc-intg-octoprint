"""
OctoPrint Button entities.

:copyright: (c) 2026 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

import logging
from typing import Any
from ucapi import StatusCodes
from ucapi.button import Button, Attributes
from intg_octoprint.config import OctoPrintConfig
from intg_octoprint.device import OctoPrintDevice

_LOG = logging.getLogger(__name__)


class OctoPrintPauseButton(Button):
    """Button to pause the current print job."""

    def __init__(self, device_config: OctoPrintConfig, device: OctoPrintDevice):
        """Initialize the pause button."""
        self._device = device
        self._device_config = device_config

        entity_id = f"button.{device_config.identifier}_pause"

        super().__init__(
            entity_id,
            f"{device_config.name} Pause",
            [],
            {Attributes.STATE: "UNAVAILABLE"},
            cmd_handler=self.handle_command,
        )

    async def handle_command(
        self, entity: Button, cmd_id: str, params: dict[str, Any] | None
    ) -> StatusCodes:
        """Handle button press."""
        _LOG.info("[%s] Pause button pressed", self.id)
        try:
            success = await self._device.pause_job()
            return StatusCodes.OK if success else StatusCodes.SERVER_ERROR
        except Exception as err:
            _LOG.error("[%s] Error: %s", self.id, err)
            return StatusCodes.SERVER_ERROR


class OctoPrintResumeButton(Button):
    """Button to resume the current print job."""

    def __init__(self, device_config: OctoPrintConfig, device: OctoPrintDevice):
        """Initialize the resume button."""
        self._device = device
        self._device_config = device_config

        entity_id = f"button.{device_config.identifier}_resume"

        super().__init__(
            entity_id,
            f"{device_config.name} Resume",
            [],
            {Attributes.STATE: "UNAVAILABLE"},
            cmd_handler=self.handle_command,
        )

    async def handle_command(
        self, entity: Button, cmd_id: str, params: dict[str, Any] | None
    ) -> StatusCodes:
        """Handle button press."""
        _LOG.info("[%s] Resume button pressed", self.id)
        try:
            success = await self._device.resume_job()
            return StatusCodes.OK if success else StatusCodes.SERVER_ERROR
        except Exception as err:
            _LOG.error("[%s] Error: %s", self.id, err)
            return StatusCodes.SERVER_ERROR


class OctoPrintStopButton(Button):
    """Button to stop/cancel the current print job."""

    def __init__(self, device_config: OctoPrintConfig, device: OctoPrintDevice):
        """Initialize the stop button."""
        self._device = device
        self._device_config = device_config

        entity_id = f"button.{device_config.identifier}_stop"

        super().__init__(
            entity_id,
            f"{device_config.name} Stop",
            [],
            {Attributes.STATE: "UNAVAILABLE"},
            cmd_handler=self.handle_command,
        )

    async def handle_command(
        self, entity: Button, cmd_id: str, params: dict[str, Any] | None
    ) -> StatusCodes:
        """Handle button press."""
        _LOG.info("[%s] Stop button pressed", self.id)
        try:
            success = await self._device.stop_job()
            return StatusCodes.OK if success else StatusCodes.SERVER_ERROR
        except Exception as err:
            _LOG.error("[%s] Error: %s", self.id, err)
            return StatusCodes.SERVER_ERROR


class OctoPrintHomeButton(Button):
    """Button to home all printer axes."""

    def __init__(self, device_config: OctoPrintConfig, device: OctoPrintDevice):
        """Initialize the home button."""
        self._device = device
        self._device_config = device_config

        entity_id = f"button.{device_config.identifier}_home"

        super().__init__(
            entity_id,
            f"{device_config.name} Home",
            [],
            {Attributes.STATE: "UNAVAILABLE"},
            cmd_handler=self.handle_command,
        )

    async def handle_command(
        self, entity: Button, cmd_id: str, params: dict[str, Any] | None
    ) -> StatusCodes:
        """Handle button press."""
        _LOG.info("[%s] Home button pressed", self.id)
        try:
            success = await self._device.home_axes()
            return StatusCodes.OK if success else StatusCodes.SERVER_ERROR
        except Exception as err:
            _LOG.error("[%s] Error: %s", self.id, err)
            return StatusCodes.SERVER_ERROR


class OctoPrintConnectButton(Button):
    """Button to connect to the printer."""

    def __init__(self, device_config: OctoPrintConfig, device: OctoPrintDevice):
        """Initialize the connect button."""
        self._device = device
        self._device_config = device_config

        entity_id = f"button.{device_config.identifier}_connect"

        super().__init__(
            entity_id,
            f"{device_config.name} Connect",
            [],
            {Attributes.STATE: "UNAVAILABLE"},
            cmd_handler=self.handle_command,
        )

    async def handle_command(
        self, entity: Button, cmd_id: str, params: dict[str, Any] | None
    ) -> StatusCodes:
        """Handle button press."""
        _LOG.info("[%s] Connect button pressed", self.id)
        try:
            success = await self._device.connect_printer()
            return StatusCodes.OK if success else StatusCodes.SERVER_ERROR
        except Exception as err:
            _LOG.error("[%s] Error: %s", self.id, err)
            return StatusCodes.SERVER_ERROR


class OctoPrintDisconnectButton(Button):
    """Button to disconnect from the printer."""

    def __init__(self, device_config: OctoPrintConfig, device: OctoPrintDevice):
        """Initialize the disconnect button."""
        self._device = device
        self._device_config = device_config

        entity_id = f"button.{device_config.identifier}_disconnect"

        super().__init__(
            entity_id,
            f"{device_config.name} Disconnect",
            [],
            {Attributes.STATE: "UNAVAILABLE"},
            cmd_handler=self.handle_command,
        )

    async def handle_command(
        self, entity: Button, cmd_id: str, params: dict[str, Any] | None
    ) -> StatusCodes:
        """Handle button press."""
        _LOG.info("[%s] Disconnect button pressed", self.id)
        try:
            success = await self._device.disconnect_printer()
            return StatusCodes.OK if success else StatusCodes.SERVER_ERROR
        except Exception as err:
            _LOG.error("[%s] Error: %s", self.id, err)
            return StatusCodes.SERVER_ERROR
