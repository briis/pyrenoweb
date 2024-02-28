# ruff: noqa: F401
"""This module is only used to run some realtime data tests using the async functions, while developing the module.
"""
from __future__ import annotations

import asyncio
import aiohttp
import logging
import time
import sys

from pyrenoweb import GarbageCollection, MUNICIPALITIES_ARRAY, RenoWebAddressInfo, RenoWebCollectionData

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
            garbage_data: RenoWebCollectionData = await garbage.get_data(address_id=sys.argv[3])
            print("")
            print("========================================================")
            print("Rest og madaffald: ", garbage_data.restaffaldmadaffald)
            print("Glas", garbage_data.glas)
            print("Dagrenovation: ", garbage_data.dagrenovation)
            print("Metal-Glas: ", garbage_data.metalglas)
            print("PAPPI: ", garbage_data.pappi)
            print("Farligt affald: ", garbage_data.farligtaffald)
            print("Farligt affald/Miljøboks: ", garbage_data.farligtaffaldmiljoboks)
            print("Flis: ", garbage_data.flis)
            print("Genbrug: ", garbage_data.genbrug)
            print("Jern: ", garbage_data.jern)
            print("Papir: ", garbage_data.papir)
            print("Papir/metal: ", garbage_data.papirmetal)
            print("Pap: ", garbage_data.pap)
            print("Plast Metal: ", garbage_data.plastmetal)
            print("Storskrald: ", garbage_data.storskrald)
            print("Storskrald og tekstilaffald: ", garbage_data.storskraldogtekstilaffald)
            print("Haveaffald: ", garbage_data.haveaffald)
            print("Papir, Pap & Glas: ", garbage_data.papirglas)
            print("Næste Afhentningsdato: ", garbage_data.next_pickup)
            print("Næste Afhentning: ", garbage_data.next_pickup_item)
            print("")

        except Exception as err:
            print(err)

    elif sys.argv[1] == "municipalities":
        for row in MUNICIPALITIES_ARRAY:
            print(row.capitalize())

    elif sys.argv[1] == "pickup_data":
        data = await garbage.get_pickup_data(address_id=sys.argv[3])
        print(data)

    if session is not None:
        await session.close()

    end = time.time()

    _LOGGER.info("Execution time: %s seconds", end - start)

asyncio.run(main())