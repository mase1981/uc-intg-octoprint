"""
OctoPrint configuration for Unfolded Circle integration.

:copyright: (c) 2026 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

from dataclasses import dataclass
from ucapi_framework import BaseConfigManager


@dataclass
class OctoPrintConfig:
    """OctoPrint configuration."""

    identifier: str
    name: str
    host: str
    port: int
    api_key: str
    ssl: bool = False
    path: str = "/"


class OctoPrintConfigManager(BaseConfigManager[OctoPrintConfig]):
    """Configuration manager with automatic JSON persistence."""

    pass
