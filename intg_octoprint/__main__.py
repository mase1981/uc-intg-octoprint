"""
Entry point for running as module: python -m intg_octoprint

:copyright: (c) 2026 by Meir Miyara.
:license: MPL-2.0, see LICENSE for more details.
"""

import asyncio
from intg_octoprint import main

if __name__ == "__main__":
    asyncio.run(main())
