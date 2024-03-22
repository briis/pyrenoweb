"""This module contains the code to get garbage data from Renoweb."""
from __future__ import annotations

import abc
import datetime as dt
import json
import logging

from typing import Any

import aiohttp

from .const import (
    API_URL_DATA,
    API_URL_SEARCH,
    ICON_LIST,
    MATERIAL_LIST,
    MUNICIPALITIES_LIST,
    NAME_LIST,
    NON_MATERIAL_LIST,
    NON_SUPPORTED_ITEMS,
    SUPPORTED_ITEMS,
    WEEKDAYS,
)
from .data import PickupEvents, PickupType, RenoWebAddressInfo

_LOGGER = logging.getLogger(__name__)


class RenowWebNotSupportedError(Exception):
    """Raised when the municipality is not supported."""


class RenowWebNotValidAddressError(Exception):
    """Raised when the address is not found."""


class RenowWebNoConnection(Exception):
    """Raised when no data is received."""


class RenowWebGarbageTypeNotFound(Exception):
    """Raised when new garbage type is detected."""


class RenoWebAPIBase:
    """Base class for the API."""

    @abc.abstractmethod
    async def async_api_request(self, url: str) -> dict[str, Any]:
        """Override this."""
        raise NotImplementedError(
            "users must define async_api_request to use this base class"
        )


class RenoWebAPI(RenoWebAPIBase):
    """Class to get data from Renoweb."""

    def __init__(self) -> None:
        """Initialize the class."""
        self.session = None

    async def async_api_request(self, url: str, body: str) -> dict[str, Any]:
        """Make an API request."""

        is_new_session = False
        if self.session is None:
            self.session = aiohttp.ClientSession()
            is_new_session = True

        headers = {"Content-Type": "application/json"}
        # self.session.headers.update(headers)

        async with self.session.post(
            url, headers=headers, data=json.dumps(body)
        ) as response:
            if response.status != 200:
                if is_new_session:
                    await self.session.close()

                if response.status == 400:
                    raise RenowWebNotSupportedError("Municipality not supported")

                if response.status == 404:
                    raise RenowWebNotSupportedError("Municipality not supported")

                if response.status == 503:
                    raise RenowWebNoConnection("System API is currently not available")

                raise RenowWebNoConnection(f"Error {response.status} from {url}")

            data = await response.text()
            if is_new_session:
                await self.session.close()

            json_data = json.loads(data)
            return json_data


class GarbageCollection:
    """Class to get garbage collection data."""

    def __init__(
        self,
        municipality: str,
        session: aiohttp.ClientSession = None,
        api: RenoWebAPIBase = RenoWebAPI(),
    ) -> None:
        """Initialize the class."""
        self._municipality = municipality
        self._street = None
        self._house_number = None
        self._api = api
        self._data = None
        self._municipality_url = None
        self._address_id = None
        if session:
            self._api.session = session
        for key, value in MUNICIPALITIES_LIST.items():
            if key.lower() == self._municipality.lower():
                self._municipality_url = value
                break

    async def async_init(self) -> None:
        """Initialize the connection."""
        if self._municipality is not None:
            url = f"https://{self._municipality_url}{API_URL_SEARCH}"
            body = {
                "searchterm": f"{self._street} {self._house_number}",
                "addresswithmateriel": 0,
            }
            await self._api.async_api_request(url, body)

    async def get_address_id(
        self, zipcode: str, street: str, house_number: str
    ) -> RenoWebAddressInfo:
        """Get the address id."""

        if self._municipality_url is not None:
            _LOGGER.debug("Municipality URL: %s", self._municipality_url)
            url = f"https://{self._municipality_url}{API_URL_SEARCH}"
            body = {"searchterm": f"{street} {house_number}", "addresswithmateriel": 0}
            data: dict[str, Any] = await self._api.async_api_request(url, body)
            result = json.loads(data["d"])
            # _LOGGER.debug("Address Data: %s", result)
            if "list" not in result:
                raise RenowWebNoConnection(
                    f"Renoweb API: {result['status']['status']} - {result['status']['msg']}"
                )

            _result_count = len(result["list"])
            _item: int = 0
            _row_index: int = 0
            if _result_count > 1:
                for row in result["list"]:
                    if zipcode in row["label"]:
                        _item = _row_index
                        break
                    _row_index += 1
            self._address_id = result["list"][_item]["value"]

            if self._address_id == "0000":
                raise RenowWebNotValidAddressError("Address not found")

            address_data = RenoWebAddressInfo(
                self._address_id,
                self._municipality.capitalize(),
                street.capitalize(),
                house_number,
            )
            return address_data
        else:
            raise RenowWebNotSupportedError("Cannot find Municipality")

    async def get_pickup_data(self, address_id: str) -> PickupEvents:
        """Get the garbage collection data."""

        if self._municipality_url is not None:
            url = f"https://{self._municipality_url}{API_URL_DATA}"
            body = {"adrid": f"{address_id}", "common": "false"}
            data = await self._api.async_api_request(url, body)
            result = json.loads(data["d"])
            garbage_data = result["list"]
            # _LOGGER.debug("Garbage Data: %s", garbage_data)

            pickup_events: PickupEvents = {}
            _next_pickup = dt.datetime(2030, 12, 31, 23, 59, 00)
            _next_pickup_event: PickupType = None

            for row in garbage_data:
                if row["ordningnavn"] in NON_SUPPORTED_ITEMS:
                    continue

                _pickup_date = None
                if row["toemningsdato"] not in NON_SUPPORTED_ITEMS:
                    _pickup_date = to_date(row["toemningsdato"])
                elif str(row["toemningsdage"]).capitalize() in WEEKDAYS:
                    _pickup_date = get_next_weekday(row["toemningsdage"])
                else:
                    continue

                if (
                    "genbrug" in row["ordningnavn"].lower()
                    or "papir og glas/dåser" in row["ordningnavn"].lower()
                ):
                    key = get_garbage_type_from_material(row["materielnavn"])
                else:
                    key = get_garbage_type(row["ordningnavn"])

                if key == row["ordningnavn"] and key != "Bestillerordning":
                    _LOGGER.warning(
                        "Garbage type [%s] is not defined in the system. Please notify the developer",
                        key,
                    )
                    continue

                _last_update = dt.datetime.now()
                _pickup_event = {
                    key: PickupType(
                        date=_pickup_date,
                        group=row["ordningnavn"],
                        friendly_name=NAME_LIST.get(key),
                        icon=ICON_LIST.get(key),
                        entity_picture=f"{key}.svg",
                        description=row["materielnavn"],
                        last_updated=_last_update.strftime("%Y-%m-%d %H:%M:%S"),
                    )
                }
                pickup_events.update(_pickup_event)

                if _pickup_date is not None:
                    if _pickup_date < _next_pickup:
                        _next_pickup = _pickup_date
                        _next_pickup_event = {
                            "next_pickup": PickupType(
                                date=_pickup_date,
                                group=row["ordningnavn"],
                                friendly_name=NAME_LIST.get(key),
                                icon=ICON_LIST.get(key),
                                entity_picture=f"{key}.svg",
                                description=row["materielnavn"],
                                last_updated=_last_update.strftime("%Y-%m-%d %H:%M:%S"),
                            )
                        }

            pickup_events.update(_next_pickup_event)
            return pickup_events


def to_date(datetext: str) -> dt.datetime:
    """Convert a date string to a datetime object."""
    if datetext == "Ingen tømningsdato fundet!":
        return None

    index = datetext.rfind(" ")
    if index == -1:
        return None
    return dt.datetime.strptime(f"{datetext[index+1:]} 00:00:00", "%d-%m-%Y %H:%M:%S")


def get_garbage_type(item: str) -> str:
    """Get the garbage type."""
    # _LOGGER.debug("Affalds type: %s", item)
    for key, value in SUPPORTED_ITEMS.items():
        if item.lower() in str(value).lower():
            for entry in value:
                if item.lower() == entry.lower():
                    return key
    return item


def get_garbage_type_from_material(item: str) -> str:
    """Get the garbage type from the materialnavn."""
    _LOGGER.debug("Material: %s", item)
    for key, value in MATERIAL_LIST.items():
        if item in NON_MATERIAL_LIST:
            continue
        if item.lower() in str(value).lower():
            for entry in value:
                if item.lower() == entry.lower():
                    return key

    _LOGGER.warning(
        "Material type [%s] is not defined in the system for Genbrug. Please notify the developer",
        item,
    )
    return "genbrug"


def get_next_weekday(weekday: str) -> dt.datetime:
    weekdays = WEEKDAYS
    current_weekday = dt.datetime.now().weekday()
    target_weekday = weekdays.index(weekday.capitalize())
    days_ahead = (target_weekday - current_weekday) % 7
    next_date = dt.datetime.now() + dt.timedelta(days=days_ahead)
    return next_date
