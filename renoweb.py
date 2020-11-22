from pyrenoweb.errors import ResultError
from pyrenoweb.client import RenoWeb, RenoWebData
from pyrenoweb.const import color
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

    # Get a RenoWeb Object
    session = ClientSession()

    if len(argv) < 1:
        print(
            f"{color.BOLD}\nusage:{color.END}\n"
            f"renoweb.py {color.BOLD}find{color.END} <municipality name> <zip_code> <road name> <house number> - Get the ID's you need to get pickup data\n"
            f"renoweb.py {color.BOLD}data{color.END} <municipality id> <address id> - Show pickup data for the Address\n"
            f"or to get individual ID's:\n"
            f"renoweb.py {color.BOLD}municipality{color.END} - Find your Municipality ID\n"
            f"renoweb.py {color.BOLD}road{color.END} <municipality id> <zip_code> <road name> - Find your Road ID\n"
            f"renoweb.py {color.BOLD}address{color.END} <municipality id> <road id> <house number> - Find your Address ID\n"
            f"renoweb.py {color.BOLD}find_municipality{color.END} <zip_code> <road name> <start id> <end id> - Find Municipality ID - Takes a Long Time\n"
        )
        sys.exit(2)
    else:
        renoweb = RenoWeb(API_KEY, API_KEY2, session)
        if argv[0] == "municipality":
            # Print List of Municipalities
            data = await renoweb.get_municipalities()
            print(f"{color.BOLD}\nMUNICIPALITY LIST\n**************************{color.END}")
            for row in data:
                print(f"{row['municipalityname']} - ID: {color.BLUE}{row['municipalitycode']}{color.END}")
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
            print(f"\n{color.RED}PICK-UP'S\n**************************{color.END}\n")
            for row in data:
                item = data.get(row)
                print(
                    f"{color.BOLD}TYPE{color.END}: {row}\n"
                    f"{color.BOLD}DESCRIPTION{color.END}: {item['description']}\n"
                    f"{color.BOLD}NEXT PICK-UP{color.END}: {item['nextpickupdatetext']}\n"
                    f"{color.BOLD}DATE{color.END}: {item['nextpickupdate']}\n"
                    f"{color.BOLD}SCHEDULE{color.END}: {item['schedule']}\n"
                    f"{color.BOLD}DAYS TO PICK-UP{color.END}: {item['daysuntilpickup']}\n"
                )
        else:
            print(
                f"{color.BOLD}\nusage:{color.END}\n"
                f"renoweb.py {color.BOLD}find{color.END} <municipality name> <zip_code> <road name> <house number> - Get the ID's you need to get pickup data\n"
                f"renoweb.py {color.BOLD}data{color.END} <municipality id> <address id> - Show pickup data for the Address\n"
                f"or to get individual ID's:\n"
                f"renoweb.py {color.BOLD}municipality{color.END} - Find your Municipality ID\n"
                f"renoweb.py {color.BOLD}road{color.END} <municipality id> <zip_code> <road name> - Find your Road ID\n"
                f"renoweb.py {color.BOLD}address{color.END} <municipality id> <road id> <house number> - Find your Address ID\n"
                f"renoweb.py {color.BOLD}find_municipality{color.END} <zip_code> <road name> <start id> <end id> - Find Municipality ID - Takes a Long Time\n"
            )

    # Close the Session
    await session.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(run_function(sys.argv[1:]))
loop.close()


