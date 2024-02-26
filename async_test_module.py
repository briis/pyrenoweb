# ruff: noqa: F401
"""This module is only used to run some realtime data tests using the async functions, while developing the module.
"""
from __future__ import annotations

import asyncio
import aiohttp
import logging
import time
import sys

from pyrenoweb import GarbageCollection, RenoWebAddressInfo, RenoWebPickupData

_LOGGER = logging.getLogger(__name__)

async def main() -> None:
    """Async test module."""

    logging.basicConfig(level=logging.DEBUG)
    start = time.time()

    session = aiohttp.ClientSession()
    garbage = GarbageCollection(municipality=sys.argv[2], session=session)
    await garbage.async_init()

    if sys.argv[1] == "address_id":
        try:
            address_data: RenoWebAddressInfo = await garbage.get_address_id(street=sys.argv[3],house_number=sys.argv[4])
            print("")
            print("========================================================")
            print("Address ID: ", address_data.address_id)
            print("Kommune: ", address_data.kommunenavn)
            print("Vejnavn: ", address_data.vejnavn)
            print("Hus nr.: ", address_data.husnr)

        except Exception as err:
            print(err)


    elif sys.argv[1] == "data":
        try:
            garbage_data: RenoWebPickupData = await garbage.get_data(address_id=sys.argv[3])
            for row in garbage_data:
                print("")
                print("========================================================")
                print("Name: ", row.name)
                print("Ordnings Navn: ", row.ordningnavn)
                print("Material Navn: ", row.materielnavn)
                print("Tømnings dato: ", row.toemningsdato)
                print("Tømnings int: ", row.toemningsint)
                print("Pickup Date: ", row.pickup_date)
                print("UTC Timestamp: ", row.timestamp)
                print("Fraction: ", row.fractionid)
                print("Type Id: ", row.mattypeid)
                print("Icon: ", row.icon)
                print("")

        except Exception as err:
            print(err)


    if session is not None:
        await session.close()

    end = time.time()

    _LOGGER.info("Execution time: %s seconds", end - start)

asyncio.run(main())