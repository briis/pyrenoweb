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

import logging

from pyrenoweb.const import (
    BASE_URL,
    DEFAULT_TIMEOUT,
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

    async def get_roadids(self, municipality_id: str, road_name: str) -> None:
        """Return a Formatted list with all Roads in the Municipality."""
        endpoint = f"GetJSONRoad.aspx?municipalitycode={municipality_id}&apikey={self._api_key_2}&roadname={road_name}"
        json_data = await self.async_request("get", endpoint)

        for row in json_data["list"]:
            item = {
                "name": row.get("name"),
                "id": row.get("id"),
            }
            return item

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
                    "id": str(row.get("id")),
                }
                items.append(item)
        return items

    async def find_renoweb_ids(self, municipality_name: str, street_name: str, house_number: str):
        """Returns Municipality ID and Address ID, based on search Criteria."""
        municipality_id = None
        road_id = None
        address_id = None
        address = None

        # Search Municipalities
        json_data = await self.get_municipalities()
        for row in json_data:
            municipality = row.get("municipalityname")
            if municipality is not None and (str(municipality).lower() == municipality_name.lower()):
                municipality_id = row.get("municipalitycode")
        if municipality_id is None:
            raise MunicipalityError("Municipality is not Found")

        # Municipality Found, search for Road ID
        json_data = await self.get_roadids(municipality_id, street_name)
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
        else:
            raise ResultError("House Number not found on address")

        # We got to here, so return final results
        return {
            "municipality_id": municipality_id,
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


    async def get_pickup_data(self) -> None:
        """Return json data array with pick up data for the address."""
        endpoint = f"GetJSONContainerList.aspx?municipalitycode={self._municipality_id}&apikey={self._api_key}&adressId={self._address_id}&fullinfo=1&supportsSharedEquipment=1"
        json_data = await self.async_request("get", endpoint)
        items = []

        for row in json_data["list"]:
            module = row.get("module")
            next_pickup = datetime.date.fromtimestamp(int(row.get("nextpickupdatetimestamp")))
            today = datetime.date.today()
            next_pickup_days = (next_pickup - today).days
            item = {
                module.get("name"): {
                    "description": row.get("name"),
                    "nextpickupdate": row.get("nextpickupdate"),
                    "nextpickupdatetimestamp": next_pickup.isoformat(),
                    "pickupdates": row.get("pickupdates"),
                    "nextpickupdays": next_pickup_days,
                }
            }
            items.append(item)
        return items

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
