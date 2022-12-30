"""Wrapper to retrieve Sensor data from RenoWeb API
   Specifically developed to wotk with Home Assistant
   Developed by: @briis
   Github: https://github.com/briis/pyrenoweb
   License: MIT
"""

import asyncio
from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError
from typing import Optional
import sys
import datetime
import json

import logging

from pyrenoweb.const import (
    BASE_URL,
    DAWA_URL,
    DEFAULT_TIMEOUT,
    NO_WASTE_SCHEDULE_TIMESTAMP,
    WASTE_LIST,
)
from pyrenoweb.errors import (
    InvalidApiKey,
    RequestError,
    ResultError,
    MunicipalityError,
)

_LOGGER = logging.getLogger(__name__)


class RenoWeb:
    """Main class to retrive data."""

    def __init__(
        self,
        api_key: str,
        api_key_2: str,
        session: Optional[ClientSession] = None,
    ):
        self._api_key = api_key
        self._api_key_2 = api_key_2
        self._session: ClientSession = session

    async def get_municipalities(self) -> None:
        """Return a Formatted list with all Municipalities."""
        endpoint = f"AFP2/GetAffaldsportal2Config.aspx?appidentifier={self._api_key}"
        json_data = await self.async_request("get", endpoint)
        items = []
        for row in json_data["list"]:
            item = {
                "municipalityname": row.get("municipalityname"),
                "municipalitycode": row.get("municipalitycode"),
            }
            items.append(item)
        return items

    async def get_municipalities_new(self) -> None:
        """Return a Formatted list with all Municipalities."""
        json_data = await self.async_request("get", None)
        items = []

        for row in json_data:
            item = {
                "municipalityname": row.get("navn"),
                "municipalitycode": row.get("kode"),
            }
            items.append(item)
        return items

    async def get_municipalities_raw(self) -> None:
        """Return a Un-Formatted json array with all Municipalities."""
        endpoint = f"AFP2/GetAffaldsportal2Config.aspx?appidentifier={self._api_key}"
        json_data = await self.async_request("get", endpoint)

        return json_data

    async def find_municipality(self, zipcode: str, road_name: str, start_id: int, end_id: int) -> None:
        """Loops through Municipality ID's to see if we can find an ID."""

        items = []
        for id in range(int(start_id), int(end_id)):
            try:
                _LOGGER.info(f"Trying ID {id}")
                endpoint = f"GetJSONRoad.aspx?municipalitycode={id}&apikey={self._api_key_2}&roadname={road_name}"
                json_data = await self.async_request("get", endpoint)
                if json_data["status"]["msg"] == "Ok":
                    _LOGGER.info(f"Found Road")
                    for row in json_data["list"]:
                        postal_start = str(row.get("name")).find("(") + 1
                        postal = str(row.get("name"))[postal_start:postal_start + 4]
                        if postal == zipcode:
                            item = {
                                "municipality_id": id,
                                "name": row.get("name"),
                                "id": row.get("id"),
                            }
                            items.append(item)
            except:
                pass

            await asyncio.sleep(0.5)    

        if len(items) == 0:            
            item = {
                "municipality_id": "Not Found",
                "name": None,
                "id": None,
            }
            items.append(item)

        return items

    async def get_roadids(self, municipality_id: str, zipcode: str, road_name: str) -> None:
        """Return a Formatted list with all Roads in the Municipality."""
        endpoint = f"GetJSONRoad.aspx?municipalitycode={municipality_id}&apikey={self._api_key_2}&roadname={road_name}"
        json_data = await self.async_request("get", endpoint)
        item = {}
        if "list" in json_data:
            for row in json_data["list"]:
                postal_start = str(row.get("name")).find("(") + 1
                postal = str(row.get("name"))[postal_start:postal_start + 4]
                if postal == zipcode:
                    item = {
                        "name": row.get("name"),
                        "id": row.get("id"),
                    }
            return item
        else:
            return None

    async def get_addressids(
        self, municipality_id: str, road_id: str, house_number: str
    ) -> None:
        """Return a Formatted list with all Roads in the Municipality."""
        endpoint = f"GetJSONAdress.aspx?municipalitycode={municipality_id}&apikey={self._api_key_2}&roadid={road_id}"
        json_data = await self.async_request("get", endpoint)
        items = []

        for row in json_data["list"]:
            building_id = str(row.get("streetBuildingIdentifier"))
            if building_id == house_number:
                item = {
                    "streetname": row.get("streetname"),
                    "streetBuildingIdentifier": str(
                        row.get("streetBuildingIdentifier")
                    ),
                    "address": row.get("presentationString"),
                    "districtName": row.get("districtName"),
                    "id": str(row.get("id")),
                }
                items.append(item)
        return items

    async def find_renoweb_ids(self, municipality_name: str, zipcode: str, street_name: str, house_number: str):
        """Returns Municipality ID and Address ID, based on search Criteria."""
        municipality_id = None
        road_id = None
        address_id = None
        address = None
        districtName = None

        # Search Municipalities
        if not municipality_name.isnumeric():
            json_data = await self.get_municipalities_new()
            for row in json_data:
                municipality = row.get("municipalityname")
                if municipality is not None and (str(municipality).lower() == municipality_name.lower()):
                    municipality_id = row.get("municipalitycode")
            if municipality_id is None:
                raise MunicipalityError("Municipality is not Found")
        else:
            municipality_id = municipality_name

        # Municipality Found, search for Road ID
        json_data = await self.get_roadids(municipality_id, zipcode, street_name)
        if json_data is not None:
            road_id = json_data.get("id")
        else:
            raise ResultError("Municipality found, but Road Name is not")

        # Road found, search for Address ID
        json_data = await self.get_addressids(municipality_id, road_id, house_number)
        if json_data is not None:
            # return json_data
            for row in json_data:
                address_id = row.get("id")
                address = row.get("address")
                districtName = row.get("districtName")
        else:
            raise ResultError("House Number not found on address")

        # We got to here, so return final results
        return {
            "municipality_id": municipality_id,
            "municipality": districtName,
            "address_id": address_id,
            "address": address,
            "road_id": road_id,
        }

    async def async_request(self, method: str, endpoint: str) -> dict:
        """Make a request against the Weatherbit API."""

        use_running_session = self._session and not self._session.closed

        if use_running_session:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))

        if endpoint is None:
            url = DAWA_URL
        else:
            url = f"{BASE_URL}/{endpoint}"

        try:
            async with session.request(method, url) as resp:
                resp.raise_for_status()
                data = await resp.json()
                return data
        except asyncio.TimeoutError:
            raise RequestError(f"Request to endpoint timed out: {BASE_URL}/{endpoint}")
        except ClientError as err:
            if "Forbidden" in str(err):
                raise InvalidApiKey(
                    "Your API Key is invalid or does not support this operation"
                )
            else:
                raise RequestError(f"Error requesting data from {BASE_URL}: {str(err)}")
        except:
            raise RequestError(f"Error occurred: {sys.exc_info()[1]}")
        finally:
            if not use_running_session:
                await session.close()

class RenoWebData:
    """Class to retrive pick-up data."""

    def __init__(
        self,
        api_key: str,
        municipality_id: str,
        address_id: str,
        session: Optional[ClientSession] = None,
    ):
        self._api_key = api_key
        self._municipality_id = municipality_id
        self._address_id = address_id
        self._session: ClientSession = session

    async def fetch_waste_data(self) -> None:
        """Return json data with the schedules for waste pick-up."""
        endpoint = f"GetJSONContainerList.aspx?municipalitycode={self._municipality_id}&apikey={self._api_key}&adressId={self._address_id}&fullinfo=1&supportsSharedEquipment=1"
        json_data = await self.async_request("get", endpoint)
        entries = {}
        if json_data["list"] is not None:
            for row in json_data["list"]:
                module = row.get("module")
                fraction_name = module.get("fractionname").replace("/", "_")
                fraction_id = row.get("id")
                if row.get("nextpickupdatetimestamp").isnumeric():
                    next_pickup = datetime.datetime.utcfromtimestamp(int(row.get("nextpickupdatetimestamp")))
                    valid_data = True
                else:
                    # There is currently no data for the Waste Type, so set a future date
                    next_pickup = datetime.datetime.utcfromtimestamp(NO_WASTE_SCHEDULE_TIMESTAMP)
                    valid_data = False

                name = row["name"]
                schedule = row.get("pickupdates")
                icon_list = list(filter(lambda WASTE_LIST: WASTE_LIST['type'] == fraction_name, WASTE_LIST))

                sensor_item = {
                    f"{fraction_name}_{fraction_id}": {
                        "key": f"{fraction_name}",
                        "date": next_pickup,
                        "icon": icon_list[0]['icon'],
                        "valid_data": valid_data,
                        "name": name,
                        "schedule": schedule,
                    }
                } 
                entries.update(sensor_item)

        return entries

    # async def get_pickup_data(self) -> None:
    #     """Return json data array with pick up data for the address."""
    #     endpoint = f"GetJSONContainerList.aspx?municipalitycode={self._municipality_id}&apikey={self._api_key}&adressId={self._address_id}&fullinfo=1&supportsSharedEquipment=1"
    #     json_data = await self.async_request("get", endpoint)
    #     items = {}
    #     item = {}
    #     min_pickup_days = 999
    #     min_pickup_timestamp = None
    #     min_pickup_date = None
    #     for row in json_data["list"]:
    #         module = row.get("module")
    #         fraction_name = module.get("fractionname").replace("/", "_")
    #         fraction_id = row.get("id")
    #         _LOGGER.info(f"{fraction_name}{fraction_id}")
    #         if row.get("nextpickupdatetimestamp").isnumeric():
    #             next_pickup = datetime.date.fromtimestamp(int(row.get("nextpickupdatetimestamp")))
    #             today = datetime.date.today()
    #             next_pickup_days = (next_pickup - today).days

    #             # Check if this is the next Pickup
    #             if next_pickup_days < min_pickup_days:
    #                 min_pickup_days = next_pickup_days
    #                 min_pickup_timestamp = row.get("nextpickupdatetimestamp")
    #                 min_pickup_date = next_pickup.isoformat()

    #             item = {
    #                 f"{fraction_name}_{fraction_id}": {
    #                     "description": row.get("name"),
    #                     "nextpickupdatetext": row.get("nextpickupdate"),
    #                     "nextpickupdatetimestamp": row.get("nextpickupdatetimestamp"),
    #                     "updatetime": datetime.datetime.now(),
    #                     "nextpickupdate": next_pickup.isoformat(),
    #                     "schedule": row.get("pickupdates"),
    #                     "daysuntilpickup": next_pickup_days,
    #                 }
    #             }
    #         else:
    #             # Nect Pick-Up is yet to be specified - Happens around year-end
    #             element = datetime.datetime.strptime("01/01/2020", "%d/%m/%Y")
    #             ts = datetime.datetime.timestamp(element)
    #             item = {
    #                 f"{fraction_name}_{fraction_id}": {
    #                     "description": row.get("name"),
    #                     "nextpickupdatetext": "Ingen planlagte tømninger",
    #                     "nextpickupdatetimestamp": ts,
    #                     "updatetime": datetime.datetime.now(),
    #                     "nextpickupdate": element.date().isoformat(),
    #                     "schedule": row.get("pickupdates"),
    #                     "daysuntilpickup": -1,
    #                 }
    #             }
    #         items.update(item)
    #     # Add Minimum Pickup Days Sensor
    #     item = {
    #         "days_until_next_pickup": {
    #             "description": "Days until next pickup",
    #             "nextpickupdatetext": "",
    #             "nextpickupdatetimestamp": min_pickup_timestamp,
    #             "updatetime": datetime.datetime.now(),
    #             "nextpickupdate": min_pickup_date,
    #             "schedule": "",
    #             "daysuntilpickup": min_pickup_days,
    #         }
    #     }
    #     items.update(item)

    #     return items


    async def get_raw_pickup_data(self) -> None:
        """Return raw json data array with pick up data for the address."""
        endpoint = f"GetJSONContainerList.aspx?municipalitycode={self._municipality_id}&apikey={self._api_key}&adressId={self._address_id}&fullinfo=1&supportsSharedEquipment=1"
        json_data = await self.async_request("get", endpoint)
        return json_data

    async def async_request(self, method: str, endpoint: str) -> dict:
        """Make a request against the Weatherbit API."""

        use_running_session = self._session and not self._session.closed

        if use_running_session:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))

        try:
            async with session.request(method, f"{BASE_URL}/{endpoint}") as resp:
                resp.raise_for_status()
                data = await resp.json()
                return data
        except asyncio.TimeoutError:
            raise RequestError(f"Request to endpoint timed out: {BASE_URL}/{endpoint}")
        except ClientError as err:
            if "Forbidden" in str(err):
                raise InvalidApiKey(
                    "Your API Key is invalid or does not support this operation"
                )
            else:
                raise RequestError(f"Error requesting data from {BASE_URL}: {str(err)}")
        except:
            raise RequestError(f"Error occurred: {sys.exc_info()[1]}")
        finally:
            if not use_running_session:
                await session.close()
