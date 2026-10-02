"""
OctoPrint setup flow for Unfolded Circle integration.

:copyright: (c) 2026 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

import asyncio
import logging
from typing import Any
from ucapi import RequestUserInput
from ucapi_framework import BaseSetupFlow
from intg_octoprint.config import OctoPrintConfig
from intg_octoprint.device import OctoPrintDevice

_LOG = logging.getLogger(__name__)


class OctoPrintSetupFlow(BaseSetupFlow[OctoPrintConfig]):
    """Setup flow for OctoPrint integration."""

    def get_manual_entry_form(self) -> RequestUserInput:
        """Define manual entry fields."""
        return RequestUserInput(
            {"en": "OctoPrint Setup"},
            [
                {
                    "id": "name",
                    "label": {"en": "Device Name"},
                    "field": {"text": {"value": "OctoPrint"}},
                },
                {
                    "id": "host",
                    "label": {"en": "IP Address or Hostname"},
                    "field": {"text": {"value": ""}},
                },
                {
                    "id": "port",
                    "label": {"en": "Port"},
                    "field": {"text": {"value": "80"}},
                },
                {
                    "id": "api_key",
                    "label": {"en": "API Key"},
                    "field": {"text": {"value": ""}},
                },
                {
                    "id": "ssl",
                    "label": {"en": "Use SSL (HTTPS)"},
                    "field": {"checkbox": {"value": False}},
                },
                {
                    "id": "path",
                    "label": {"en": "Path (e.g., /octoprint/)"},
                    "field": {"text": {"value": "/"}},
                },
            ],
        )

    async def query_device(
        self, input_values: dict[str, Any]
    ) -> OctoPrintConfig | RequestUserInput:
        """
        Validate connection and create config.
        Called after user provides info.
        """
        host = input_values.get("host", "").strip()
        if not host:
            raise ValueError("IP address or hostname is required")

        api_key = input_values.get("api_key", "").strip()
        if not api_key:
            raise ValueError("API key is required")

        port = int(input_values.get("port", 80))
        name = input_values.get("name", f"OctoPrint ({host})").strip()
        ssl = input_values.get("ssl", False)
        path = input_values.get("path", "/").strip()

        if not path.startswith("/"):
            path = f"/{path}"
        if not path.endswith("/"):
            path = f"{path}/"

        _LOG.info("Setting up OctoPrint at %s:%s", host, port)

        try:
            test_config = OctoPrintConfig(
                identifier=f"octoprint_{host.replace('.', '_').replace('-', '_')}_{port}",
                name=name,
                host=host,
                port=port,
                api_key=api_key,
                ssl=ssl,
                path=path
            )

            test_device = OctoPrintDevice(test_config)
            try:
                connected = await asyncio.wait_for(
                    test_device._connect(),  # pylint: disable=protected-access
                    timeout=10.0
                )
            finally:
                await test_device._disconnect()  # pylint: disable=protected-access

            if not connected:
                raise ValueError(f"Failed to connect to OctoPrint at {host}:{port}")

            _LOG.info("Successfully connected to OctoPrint at %s:%s", host, port)
            return test_config

        except asyncio.TimeoutError:
            raise ValueError(
                f"Connection timeout to {host}:{port}\n"
                "Please verify OctoPrint is running and accessible on the network"
            ) from None
        except Exception as err:
            raise ValueError(f"Setup failed: {err}") from err
