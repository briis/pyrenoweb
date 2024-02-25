# ruff: noqa: F401
"""This module is only used to run some realtime data tests using the async functions, while developing the module.
"""
from __future__ import annotations

import asyncio
import aiohttp
import logging
import time

from pyrenoweb.api import GarbageCollection


_LOGGER = logging.getLogger(__name__)

async def main() -> None:
    """Async test module."""

    logging.basicConfig(level=logging.DEBUG)
    start = time.time()

    MUNICIPALITY = "Roskilde"
    STREET = "Toftebuen"
    HOUSE_NUMBER = "69"

    session = aiohttp.ClientSession()
    garbage = GarbageCollection(MUNICIPALITY, STREET, HOUSE_NUMBER, session)

    try:
        address_id = await garbage.get_address_id()
        _LOGGER.info("Address ID: %s", address_id)

    except Exception as err:
        print(err)

    if session is not None:
        await session.close()

    end = time.time()

    _LOGGER.info("Execution time: %s seconds", end - start)

asyncio.run(main())