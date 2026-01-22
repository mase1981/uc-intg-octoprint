"""
OctoPrint device implementation for Unfolded Circle integration.

:copyright: (c) 2026 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

import asyncio
import logging
from typing import Any
import aiohttp
from ucapi_framework import PollingDevice, DeviceEvents
from ucapi.sensor import Attributes as SensorAttributes
from ucapi.button import Attributes as ButtonAttributes
from ucapi.remote import Attributes as RemoteAttributes
from intg_octoprint.config import OctoPrintConfig

_LOG = logging.getLogger(__name__)


class OctoPrintDevice(PollingDevice):
    """OctoPrint implementation using PollingDevice."""

    def __init__(self, device_config: OctoPrintConfig, **kwargs):
        super().__init__(device_config, poll_interval=5, **kwargs)
        self._device_config = device_config
        self._session: aiohttp.ClientSession | None = None
        self._base_url = self._build_base_url()
        self._printer_state: dict[str, Any] | None = None
        self._job_state: dict[str, Any] | None = None
        self._version: dict[str, Any] | None = None

    def _build_base_url(self) -> str:
        """Build the base URL for OctoPrint API."""
        protocol = "https" if self._device_config.ssl else "http"
        path = self._device_config.path
        if not path.endswith("/"):
            path += "/"
        return f"{protocol}://{self._device_config.host}:{self._device_config.port}{path}api"

    @property
    def identifier(self) -> str:
        return self._device_config.identifier

    @property
    def name(self) -> str:
        return self._device_config.name

    @property
    def address(self) -> str:
        return self._device_config.host

    @property
    def log_id(self) -> str:
        return f"{self.name} ({self.address})"

    async def _connect(self) -> bool:
        """Establish connection to OctoPrint."""
        try:
            if self._session is None:
                self._session = aiohttp.ClientSession()

            _LOG.info("[%s] Testing connection to OctoPrint API", self.log_id)

            headers = {"X-Api-Key": self._device_config.api_key}
            async with self._session.get(
                f"{self._base_url}/version",
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    self._version = await response.json()
                    _LOG.info(
                        "[%s] Connected to OctoPrint %s",
                        self.log_id,
                        self._version.get("server", "Unknown")
                    )
                    return True
                else:
                    _LOG.error(
                        "[%s] Connection failed with status %d",
                        self.log_id,
                        response.status
                    )
                    return False

        except Exception as err:
            _LOG.error("[%s] Connection error: %s", self.log_id, err)
            return False

    async def _disconnect(self) -> None:
        """Disconnect from OctoPrint."""
        if self._session:
            await self._session.close()
            self._session = None
        self._printer_state = None
        self._job_state = None
        _LOG.info("[%s] Disconnected", self.log_id)

    async def _poll(self) -> None:
        """Poll OctoPrint for state updates."""
        if not self._session:
            return

        try:
            headers = {"X-Api-Key": self._device_config.api_key}

            async with self._session.get(
                f"{self._base_url}/printer",
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=5)
            ) as response:
                if response.status == 200:
                    self._printer_state = await response.json()
                elif response.status == 409:
                    _LOG.debug("[%s] Printer offline", self.log_id)
                    self._printer_state = None
                else:
                    _LOG.warning(
                        "[%s] Failed to get printer state: %d",
                        self.log_id,
                        response.status
                    )

            async with self._session.get(
                f"{self._base_url}/job",
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=5)
            ) as response:
                if response.status == 200:
                    self._job_state = await response.json()
                else:
                    _LOG.warning(
                        "[%s] Failed to get job state: %d",
                        self.log_id,
                        response.status
                    )

            self._emit_update()

        except asyncio.TimeoutError:
            _LOG.warning("[%s] Poll timeout", self.log_id)
        except Exception as err:
            _LOG.error("[%s] Poll error: %s", self.log_id, err)

    def _emit_update(self) -> None:
        """Emit entity update events for all entities."""
        button_pause_id = f"button.{self.identifier}_pause"
        button_resume_id = f"button.{self.identifier}_resume"
        button_stop_id = f"button.{self.identifier}_stop"
        button_home_id = f"button.{self.identifier}_home"
        button_connect_id = f"button.{self.identifier}_connect"
        button_disconnect_id = f"button.{self.identifier}_disconnect"

        remote_id = f"remote.{self.identifier}"

        sensor_status_id = f"sensor.{self.identifier}_status"
        sensor_progress_id = f"sensor.{self.identifier}_progress"
        sensor_time_remaining_id = f"sensor.{self.identifier}_time_remaining"
        sensor_file_id = f"sensor.{self.identifier}_file"
        sensor_connection_id = f"sensor.{self.identifier}_connection"

        if not self.is_connected:
            self.events.emit(
                DeviceEvents.UPDATE,
                sensor_connection_id,
                {
                    SensorAttributes.STATE: "Disconnected",
                    SensorAttributes.VALUE: "disconnected",
                }
            )
            self.events.emit(
                DeviceEvents.UPDATE,
                remote_id,
                {RemoteAttributes.STATE: "UNAVAILABLE"}
            )
            return

        printer_state_text = "Unknown"
        state_flags = {}

        if self._printer_state and "state" in self._printer_state:
            state_info = self._printer_state["state"]
            printer_state_text = state_info.get("text", "Unknown")
            state_flags = state_info.get("flags", {})

        is_printing = state_flags.get("printing", False)
        is_paused = state_flags.get("paused", False)
        is_operational = state_flags.get("operational", False)
        is_ready = state_flags.get("ready", False)

        progress = 0
        time_remaining = None
        file_name = None

        if self._job_state:
            job_info = self._job_state.get("job", {})
            progress_info = self._job_state.get("progress", {})

            file_name = job_info.get("file", {}).get("name")
            completion = progress_info.get("completion")
            if completion is not None:
                progress = round(completion, 1)

            print_time_left = progress_info.get("printTimeLeft")
            if print_time_left:
                hours, remainder = divmod(int(print_time_left), 3600)
                minutes, seconds = divmod(remainder, 60)
                time_remaining = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        self.events.emit(
            DeviceEvents.UPDATE,
            sensor_connection_id,
            {
                SensorAttributes.STATE: "Connected",
                SensorAttributes.VALUE: "connected",
            }
        )

        self.events.emit(
            DeviceEvents.UPDATE,
            sensor_status_id,
            {
                SensorAttributes.STATE: printer_state_text,
                SensorAttributes.VALUE: printer_state_text.lower().replace(" ", "_"),
            }
        )

        self.events.emit(
            DeviceEvents.UPDATE,
            sensor_progress_id,
            {
                SensorAttributes.STATE: f"{progress}%",
                SensorAttributes.VALUE: progress,
            }
        )

        if time_remaining:
            self.events.emit(
                DeviceEvents.UPDATE,
                sensor_time_remaining_id,
                {
                    SensorAttributes.STATE: time_remaining,
                    SensorAttributes.VALUE: time_remaining,
                }
            )

        if file_name:
            self.events.emit(
                DeviceEvents.UPDATE,
                sensor_file_id,
                {
                    SensorAttributes.STATE: file_name,
                    SensorAttributes.VALUE: file_name,
                }
            )

        remote_state = "ON" if is_operational else "OFF"
        self.events.emit(
            DeviceEvents.UPDATE,
            remote_id,
            {RemoteAttributes.STATE: remote_state}
        )

        self.events.emit(
            DeviceEvents.UPDATE,
            button_pause_id,
            {ButtonAttributes.STATE: "AVAILABLE" if is_printing else "UNAVAILABLE"}
        )

        self.events.emit(
            DeviceEvents.UPDATE,
            button_resume_id,
            {ButtonAttributes.STATE: "AVAILABLE" if is_paused else "UNAVAILABLE"}
        )

        self.events.emit(
            DeviceEvents.UPDATE,
            button_stop_id,
            {ButtonAttributes.STATE: "AVAILABLE" if (is_printing or is_paused) else "UNAVAILABLE"}
        )

        self.events.emit(
            DeviceEvents.UPDATE,
            button_home_id,
            {ButtonAttributes.STATE: "AVAILABLE" if is_operational else "UNAVAILABLE"}
        )

        self.events.emit(
            DeviceEvents.UPDATE,
            button_connect_id,
            {ButtonAttributes.STATE: "AVAILABLE" if not is_operational else "UNAVAILABLE"}
        )

        self.events.emit(
            DeviceEvents.UPDATE,
            button_disconnect_id,
            {ButtonAttributes.STATE: "AVAILABLE" if is_operational else "UNAVAILABLE"}
        )

    async def _api_request(
        self, method: str, endpoint: str, json_data: dict[str, Any] | None = None
    ) -> tuple[bool, dict[str, Any] | None]:
        """Make an API request to OctoPrint."""
        if not self._session:
            return False, None

        try:
            headers = {
                "X-Api-Key": self._device_config.api_key,
                "Content-Type": "application/json"
            }
            url = f"{self._base_url}/{endpoint}"

            async with self._session.request(
                method,
                url,
                headers=headers,
                json=json_data,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status in [200, 204]:
                    if response.status == 204:
                        return True, None
                    return True, await response.json()
                else:
                    _LOG.error(
                        "[%s] API request failed: %s %s - Status %d",
                        self.log_id,
                        method,
                        endpoint,
                        response.status
                    )
                    return False, None

        except Exception as err:
            _LOG.error("[%s] API request error: %s", self.log_id, err)
            return False, None

    async def pause_job(self) -> bool:
        """Pause the current print job."""
        _LOG.info("[%s] Pausing job", self.log_id)
        success, _ = await self._api_request("POST", "job", {"command": "pause", "action": "pause"})
        if success:
            await self._poll()
        return success

    async def resume_job(self) -> bool:
        """Resume the current print job."""
        _LOG.info("[%s] Resuming job", self.log_id)
        success, _ = await self._api_request("POST", "job", {"command": "pause", "action": "resume"})
        if success:
            await self._poll()
        return success

    async def stop_job(self) -> bool:
        """Cancel the current print job."""
        _LOG.info("[%s] Stopping job", self.log_id)
        success, _ = await self._api_request("POST", "job", {"command": "cancel"})
        if success:
            await self._poll()
        return success

    async def home_axes(self, axes: list[str] | None = None) -> bool:
        """Home printer axes."""
        if axes is None:
            axes = ["x", "y", "z"]
        _LOG.info("[%s] Homing axes: %s", self.log_id, axes)
        success, _ = await self._api_request("POST", "printer/printhead", {"command": "home", "axes": axes})
        return success

    async def connect_printer(self) -> bool:
        """Connect to the printer."""
        _LOG.info("[%s] Connecting to printer", self.log_id)
        success, _ = await self._api_request("POST", "connection", {"command": "connect"})
        if success:
            await asyncio.sleep(2)
            await self._poll()
        return success

    async def disconnect_printer(self) -> bool:
        """Disconnect from the printer."""
        _LOG.info("[%s] Disconnecting from printer", self.log_id)
        success, _ = await self._api_request("POST", "connection", {"command": "disconnect"})
        if success:
            await self._poll()
        return success

    async def jog(self, axis: str, distance: float) -> bool:
        """Jog a printer axis."""
        _LOG.info("[%s] Jogging %s by %f", self.log_id, axis, distance)
        command_data = {axis.lower(): distance}
        success, _ = await self._api_request("POST", "printer/printhead", {"command": "jog", **command_data})
        return success

    async def set_tool_temperature(self, tool: str, temperature: int) -> bool:
        """Set tool temperature."""
        _LOG.info("[%s] Setting %s temperature to %d", self.log_id, tool, temperature)
        targets = {tool: temperature}
        success, _ = await self._api_request("POST", "printer/tool", {"command": "target", "targets": targets})
        return success

    async def set_bed_temperature(self, temperature: int) -> bool:
        """Set bed temperature."""
        _LOG.info("[%s] Setting bed temperature to %d", self.log_id, temperature)
        success, _ = await self._api_request("POST", "printer/bed", {"command": "target", "target": temperature})
        return success
