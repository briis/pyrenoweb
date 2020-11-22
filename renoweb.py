from pyrenoweb.errors import ResultError
from pyrenoweb.client import RenoWeb, RenoWebData
from aiohttp import ClientSession
import asyncio
import logging
import sys
import json

API_KEY = "DDDD4A1D-DDD1-4436-DDDD-3F374DD683A1"
API_KEY2 = "346B43B0-D1F0-4AFC-9EE8-C4AD1BFDC218"

_LOGGER = logging.getLogger(__name__)


async def run_function(argv):

    logging.basicConfig(level=logging.DEBUG)

    # Define some Colors when Printing
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    # Get a RenoWeb Object
    session = ClientSession()

    if len(argv) < 1:
        print(
            "\nusage:\n"
            "renoweb.py find <municipality name> <zip_code> <road name> <house number> - Get the ID's you need to get pickup data\n"
            "renoweb.py data <municipality id> <address id> - Show pickup data for the Address\n"
            "or to get individual ID's:\n"
            "renoweb.py municipality - Find your Municipality ID\n"
            "renoweb.py road <municipality id> <zip_code> <road name> - Find your Road ID\n"
            "renoweb.py address <municipality id> <road id> <house number> - Find your Address ID\n"
            "renoweb.py find_municipality <zip_code> <road name> <start id> <end id> - Find Municipality ID - Takes a Long Time\n"
        )
        sys.exit(2)
    else:
        renoweb = RenoWeb(API_KEY, API_KEY2, session)
        if argv[0] == "municipality":
            # Print List of Municipalities
            data = await renoweb.get_municipalities()
            print(f"{BOLD}\nMUNICIPALITY LIST\n**************************{END}")
            for row in data:
                print(f"{row['municipalityname']} - ID: {BLUE}{row['municipalitycode']}{END}")
        elif argv[0] == "find_municipality":
            # See if we can find a Municipality ID
            data = await renoweb.find_municipality(argv[1], argv[2], argv[3], argv[4])
            print("\nMUNICIPALITIES WITH THIS ROAD\n**************************")
            for row in data:
                print(
                    f"MUNICIPALITY ID: {row['municipality_id']} - ROADNAME: {row['name']}"
                )
        elif argv[0] == "road":
            # Print list of Road ID's
            data = await renoweb.get_roadids(argv[1], argv[2], argv[3])
            print("\nROAD LIST\n**************************")
            if data is not None:
                print(f"ROAD: {data['name']} - ID: {data['id']}")
            else:
                print("Road Not found in this Municipality")
        elif argv[0] == "address":
            # Print list of Address ID's
            data = await renoweb.get_addressids(argv[1], argv[2], argv[3])
            print("\nADDRESS LIST\n**************************")
            for row in data:
                print(
                    f"ROAD: {row['streetname']} {row['streetBuildingIdentifier']} - ID: {row['id']}"
                )
        elif argv[0] == "find":
            # Find needed ID's based on Municipality, Streetname and House number
            try:
                data = await renoweb.find_renoweb_ids(argv[1], argv[2], argv[3], argv[4])
                print("\nID NUMBERS\n**************************")
                print(
                    f"MUNICIPALITY ID: {data['municipality_id']}\n"
                    f"MUNICIPALITY NAME: {data['municipality']}\n"
                    f"ADDRESS ID: {data['address_id']}\n"
                    f"ADDRESS: {data['address']}\n"
                )
            except ResultError as error:
                print(error)
                pass

        elif argv[0] == "data":
            # Print location data
            renoweb = RenoWebData(API_KEY2, argv[1], argv[2], session)
            data = await renoweb.get_pickup_data()
            # print(json.dumps(data, indent=1))
            print(f"\n{RED}PICK-UP'S\n**************************{END}\n")
            for row in data:
                item = data.get(row)
                print(
                    f"{BOLD}TYPE{END}: {row}\n"
                    f"{BOLD}DESCRIPTION{END}: {item['description']}\n"
                    f"{BOLD}NEXT PICK-UP{END}: {item['nextpickupdatetext']}\n"
                    f"{BOLD}DATE{END}: {item['nextpickupdate']}\n"
                    f"{BOLD}SCHEDULE{END}: {item['schedule']}\n"
                    f"{BOLD}DAYS TO PICK-UP{END}: {item['daysuntilpickup']}\n"
                )
        else:
            print(
                "\nusage:\n"
                "renoweb.py find <municipality name> <zip_code> <road name> <house number> - Get the ID's you need to get pickup data\n"
                "renoweb.py data <municipality id> <address id> - Show pickup data for the Address\n"
                "or to get individual ID's:\n"
                "renoweb.py municipality - Find your Municipality ID\n"
                "renoweb.py road <municipality id> <zip_code> <road name> - Find your Road ID\n"
                "renoweb.py address <municipality id> <road id> <house number> - Find your Address ID\n"
                "renoweb.py find_municipality <zip_code> <road name> <start id> <end id> - Find Municipality ID - Takes a Long Time\n"
            )

    # Close the Session
    await session.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(run_function(sys.argv[1:]))
loop.close()


