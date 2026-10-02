"""
OctoPrint Remote entity.

:copyright: (c) 2026 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

import logging
from typing import Any
from ucapi import StatusCodes
from ucapi.remote import (
    Attributes,
    Commands,
    Features,
    Remote,
)
from intg_octoprint.config import OctoPrintConfig
from intg_octoprint.device import OctoPrintDevice

_LOG = logging.getLogger(__name__)

SIMPLE_COMMANDS = [
    "PAUSE",
    "RESUME",
    "STOP",
    "HOME",
    "HOME_X",
    "HOME_Y",
    "HOME_Z",
    "JOG_X_PLUS",
    "JOG_X_MINUS",
    "JOG_Y_PLUS",
    "JOG_Y_MINUS",
    "JOG_Z_PLUS",
    "JOG_Z_MINUS",
    "CONNECT",
    "DISCONNECT",
]


class OctoPrintRemote(Remote):
    """Remote entity for OctoPrint."""

    def __init__(self, device_config: OctoPrintConfig, device: OctoPrintDevice):
        """Initialize with device reference."""
        self._device = device
        self._device_config = device_config

        entity_id = f"remote.{device_config.identifier}"
        entity_name = f"{device_config.name} Remote"

        features = [Features.SEND_CMD]
        attributes = {Attributes.STATE: "UNAVAILABLE"}

        user_interface = {
            "pages": [
                {
                    "page_id": "main",
                    "name": "Main Controls",
                    "grid": {"width": 4, "height": 6},
                    "items": [
                        {"type": "text", "text": "Pause", "command": {"cmd_id": "PAUSE"}, "location": {"x": 0, "y": 0}},
                        {"type": "text", "text": "Resume", "command": {"cmd_id": "RESUME"}, "location": {"x": 1, "y": 0}},
                        {"type": "text", "text": "Stop", "command": {"cmd_id": "STOP"}, "location": {"x": 2, "y": 0}},
                        {"type": "text", "text": "Home", "command": {"cmd_id": "HOME"}, "location": {"x": 3, "y": 0}},
                        {"type": "text", "text": "Connect", "command": {"cmd_id": "CONNECT"}, "location": {"x": 0, "y": 1}, "size": {"width": 2, "height": 1}},
                        {"type": "text", "text": "Disconnect", "command": {"cmd_id": "DISCONNECT"}, "location": {"x": 2, "y": 1}, "size": {"width": 2, "height": 1}},
                    ],
                },
                {
                    "page_id": "jog",
                    "name": "Jog Controls",
                    "grid": {"width": 4, "height": 6},
                    "items": [
                        {"type": "text", "text": "X+", "command": {"cmd_id": "JOG_X_PLUS"}, "location": {"x": 0, "y": 0}},
                        {"type": "text", "text": "X-", "command": {"cmd_id": "JOG_X_MINUS"}, "location": {"x": 1, "y": 0}},
                        {"type": "text", "text": "Y+", "command": {"cmd_id": "JOG_Y_PLUS"}, "location": {"x": 2, "y": 0}},
                        {"type": "text", "text": "Y-", "command": {"cmd_id": "JOG_Y_MINUS"}, "location": {"x": 3, "y": 0}},
                        {"type": "text", "text": "Z+", "command": {"cmd_id": "JOG_Z_PLUS"}, "location": {"x": 0, "y": 1}},
                        {"type": "text", "text": "Z-", "command": {"cmd_id": "JOG_Z_MINUS"}, "location": {"x": 1, "y": 1}},
                        {"type": "text", "text": "Home X", "command": {"cmd_id": "HOME_X"}, "location": {"x": 0, "y": 2}},
                        {"type": "text", "text": "Home Y", "command": {"cmd_id": "HOME_Y"}, "location": {"x": 1, "y": 2}},
                        {"type": "text", "text": "Home Z", "command": {"cmd_id": "HOME_Z"}, "location": {"x": 2, "y": 2}},
                        {"type": "text", "text": "Home All", "command": {"cmd_id": "HOME"}, "location": {"x": 3, "y": 2}},
                    ],
                },
            ]
        }

        super().__init__(
            entity_id,
            entity_name,
            features,
            attributes,
            simple_commands=SIMPLE_COMMANDS,
            ui_pages=user_interface["pages"],
            cmd_handler=self.handle_command,
        )

    async def handle_command(
        self, entity: Remote, cmd_id: str, params: dict[str, Any] | None
    ) -> StatusCodes:
        """Handle remote commands.

        The Remote sends simple commands (UI page buttons, activities) as
        ``send_cmd`` with the command name in ``params["command"]``, and lists of
        them as ``send_cmd_sequence``.
        """
        _LOG.info("[%s] Remote command: %s %s", self.id, cmd_id, params or "")
        params = params or {}

        if cmd_id == Commands.SEND_CMD:
            return await self._run_command(str(params.get("command", "")))
        if cmd_id == Commands.SEND_CMD_SEQUENCE:
            result = StatusCodes.OK
            for command in params.get("sequence", []) or []:
                status = await self._run_command(str(command))
                if status != StatusCodes.OK:
                    result = status
            return result
        return await self._run_command(cmd_id)

    async def _run_command(self, cmd_id: str) -> StatusCodes:
        """Run one simple command."""
        try:
            if cmd_id == "PAUSE":
                success = await self._device.pause_job()
                return StatusCodes.OK if success else StatusCodes.SERVER_ERROR

            elif cmd_id == "RESUME":
                success = await self._device.resume_job()
                return StatusCodes.OK if success else StatusCodes.SERVER_ERROR

            elif cmd_id == "STOP":
                success = await self._device.stop_job()
                return StatusCodes.OK if success else StatusCodes.SERVER_ERROR

            elif cmd_id == "HOME":
                success = await self._device.home_axes()
                return StatusCodes.OK if success else StatusCodes.SERVER_ERROR

            elif cmd_id == "HOME_X":
                success = await self._device.home_axes(["x"])
                return StatusCodes.OK if success else StatusCodes.SERVER_ERROR

            elif cmd_id == "HOME_Y":
                success = await self._device.home_axes(["y"])
                return StatusCodes.OK if success else StatusCodes.SERVER_ERROR

            elif cmd_id == "HOME_Z":
                success = await self._device.home_axes(["z"])
                return StatusCodes.OK if success else StatusCodes.SERVER_ERROR

            elif cmd_id == "JOG_X_PLUS":
                success = await self._device.jog("x", 10)
                return StatusCodes.OK if success else StatusCodes.SERVER_ERROR

            elif cmd_id == "JOG_X_MINUS":
                success = await self._device.jog("x", -10)
                return StatusCodes.OK if success else StatusCodes.SERVER_ERROR

            elif cmd_id == "JOG_Y_PLUS":
                success = await self._device.jog("y", 10)
                return StatusCodes.OK if success else StatusCodes.SERVER_ERROR

            elif cmd_id == "JOG_Y_MINUS":
                success = await self._device.jog("y", -10)
                return StatusCodes.OK if success else StatusCodes.SERVER_ERROR

            elif cmd_id == "JOG_Z_PLUS":
                success = await self._device.jog("z", 1)
                return StatusCodes.OK if success else StatusCodes.SERVER_ERROR

            elif cmd_id == "JOG_Z_MINUS":
                success = await self._device.jog("z", -1)
                return StatusCodes.OK if success else StatusCodes.SERVER_ERROR

            elif cmd_id == "CONNECT":
                success = await self._device.connect_printer()
                return StatusCodes.OK if success else StatusCodes.SERVER_ERROR

            elif cmd_id == "DISCONNECT":
                success = await self._device.disconnect_printer()
                return StatusCodes.OK if success else StatusCodes.SERVER_ERROR

            return StatusCodes.NOT_IMPLEMENTED

        except Exception as err:
            _LOG.error("[%s] Remote command error: %s", self.id, err)
            return StatusCodes.SERVER_ERROR
