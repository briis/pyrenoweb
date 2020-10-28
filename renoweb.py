from pyrenoweb.client import RenoeWeb
from aiohttp import ClientSession
import asyncio
import logging
import sys

API_KEY = "DDDD4A1D-DDD1-4436-DDDD-3F374DD683A1"
API_KEY2 = "346B43B0-D1F0-4AFC-9EE8-C4AD1BFDC218"

_LOGGER = logging.getLogger(__name__)


async def run_function(argv):

    logging.basicConfig(level=logging.DEBUG)

    # Get a RenoWeb Object
    session = ClientSession()

    if len(argv) < 1:
        print(
            "\nFølgende kommandoer kan bruges:\n"
            "renoweb.py kommuner - Find dit Kommune ID\n"
            "renoweb.py vej <kommune id> <vejnavn> - Find dit Vej ID\n"
            "renoweb.py adresse <kommune id> <vej id> <hus nummer> - Find dit Adresse ID\n"
            "renoweb.py data <kommune id> <adresse id> - Vis Data for adressen\n"
        )
        sys.exit(2)
    else:
        if argv[0] == "kommuner":
            # Print List of Municipalities
            renoweb = RenoeWeb(API_KEY, session)
            data = await renoweb.get_municipalities()
            print("\nKOMMUNE LISTE\n**************************")
            for row in data:
                print(f"BY: {row['municipalityname']} - KODE: {row['municipalitycode']}")
        elif argv[0] == "vej":
            # Print list of Road ID's
            renoweb = RenoeWeb(API_KEY2, session)
            data = await renoweb.get_roadids(argv[1], argv[2])
            print("\nVEJ LISTE\n**************************")
            print(f"VEJ: {data['name']} - KODE: {data['id']}")
        elif argv[0] == "adresse":
            # Print list of Address ID's
            renoweb = RenoeWeb(API_KEY2, session)
            data = await renoweb.get_addressids(argv[1], argv[2], argv[3])
            print("\nADRESSE LISTE\n**************************")
            # print(json.dumps(data, indent=1))
            for row in data:
                print(
                    f"VEJ: {row['streetname']} {row['streetBuildingIdentifier']} - KODE: {row['id']}"
                )
        elif argv[0] == "data":
            # Print location data
            renoweb = RenoeWeb(API_KEY2, session)
            data = await renoweb.get_pickup_data(argv[1], argv[2])
            print("\nAfhentning\n**************************\n")
            for row in data:
                print(
                    f"TYPE: {row['type']}\n"
                    f"BESKRIVELSE: {row['description']}\n"
                    f"NÆSTE AFHENTNING: {row['nextpickupdate']}\n"
                    f"DATO: {row['nextpickupdatetimestamp']}\n"
                    f"FREKVENS: {row['pickupdates']}\n"
                )
        else:
            print(
                "\nFølgende kommandoer kan bruges:\n"
                "renoweb.py kommuner - Find dit Kommune ID\n"
                "renoweb.py vej <kommune id> <vejnavn> <hus nummer> - Find dit Vej ID\n"
                "renoweb.py data <kommune id> <adresse id> - Vis Data for adressen\n"
            )

    # Close the Session
    await session.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(run_function(sys.argv[1:]))
loop.close()
