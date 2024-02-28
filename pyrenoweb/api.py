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
    MUNICIPALITIES_LIST,
    NAME_LIST,
    NON_SUPPORTED_ITEMS,
    SUPPORTED_ITEMS,
)
from .data import PickupEvents, PickupType, RenoWebAddressInfo, RenoWebCollectionData

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
    async def async_api_request( self, url: str) -> dict[str, Any]:
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

        headers = {'Content-Type': 'application/json'}
        # self.session.headers.update(headers)

        async with self.session.post(url, headers=headers, data=json.dumps(body)) as response:
            if response.status != 200:
                if is_new_session:
                    await self.session.close()

                if response.status == 400:
                    raise RenowWebNotSupportedError("Municipality not supported")

                if response.status == 404:
                    raise RenowWebNotSupportedError("Municipality not supported")

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
            if key == self._municipality.lower():
                self._municipality_url = value
                break


    async def async_init(self) -> None:
        """Initialize the connection."""
        if self._municipality is not None:
            url = f"https://{self._municipality_url}{API_URL_SEARCH}"
            body = {"searchterm":f"{self._street} {self._house_number}", "addresswithmateriel":7}
            await self._api.async_api_request(url, body)


    async def get_address_id(self, street: str, house_number: str) -> RenoWebAddressInfo:
        """Get the address id."""

        if self._municipality_url is not None:
            _LOGGER.debug("Municipality URL: %s", self._municipality_url)
            url = f"https://{self._municipality_url}{API_URL_SEARCH}"
            body = {"searchterm":f"{street} {house_number}", "addresswithmateriel":7}
            data: dict[str, Any] = await self._api.async_api_request(url, body)
            result = json.loads(data['d'])
            self._address_id = result['list'][0]['value']

            if self._address_id  == "0000":
                raise RenowWebNotValidAddressError("Address not found")

            address_data = RenoWebAddressInfo(
                self._address_id,
                self._municipality.capitalize(),
                street.capitalize(),
                house_number
            )
            return address_data
        else:
            raise RenowWebNotSupportedError("Cannot find Municipality")

    async def get_data(self, address_id: str) -> RenoWebCollectionData:
        """Get the garbage collection data."""

        # pickup_data: list[RenoWebPickupData] = []
        if self._municipality_url is not None:
            url = f"https://{self._municipality_url}{API_URL_DATA}"
            body = {"adrid":f"{address_id}", "common":"false"}
            data = await self._api.async_api_request(url, body)
            result = json.loads(data['d'])
            garbage_data = result['list']
            # _LOGGER.debug("Garbage data: %s", garbage_data)

            restaffaldmadaffald = None
            glas = None
            dagrenovation = None
            metalglas = None
            pappi = None
            farligtaffald = None
            farligtaffaldmiljoboks = None
            flis = None
            genbrug = None
            jern = None
            papir = None
            papirmetal = None
            pap = None
            plastmetal = None
            storskrald = None
            storskraldogtekstilaffald = None
            haveaffald = None
            papirglas = None
            plastmadkarton = None
            next_pickup = dt.datetime(2030,12,31,23,59,00)
            next_pickup_item = None


            for row in garbage_data:
                if row["ordningnavn"] in NON_SUPPORTED_ITEMS:
                    continue

                _pickup_date = None
                if row['toemningsdato'] != "Ingen tømningsdato fundet!" and row['toemningsdato'] is not None:
                    _pickup_date = to_date(row['toemningsdato'])

                key = get_garbage_type(row['ordningnavn'])
                if key == row['ordningnavn'] and key != "Bestillerordning":
                    _LOGGER.warning("Garbage type %s is not defined in the system. Please notify the developer", key)

                if key == "restaffaldmadaffald":
                    restaffaldmadaffald = _pickup_date
                elif key == "dagrenovation":
                    dagrenovation = _pickup_date
                elif key == "metalglas":
                    metalglas = _pickup_date
                elif key == "pappi":
                    pappi = _pickup_date
                elif key == "farligtaffald":
                    farligtaffald = _pickup_date
                elif key == "farligtaffaldmiljoboks":
                    farligtaffaldmiljoboks = _pickup_date
                elif key == "flis":
                    flis = _pickup_date
                elif key == "genbrug":
                    genbrug = _pickup_date
                elif key == "jern":
                    jern = _pickup_date
                elif key == "papir":
                    papir = _pickup_date
                elif key == "papirmetal":
                    papirmetal = _pickup_date
                elif key == "pap":
                    pap = _pickup_date
                elif key == "plastmetal":
                    plastmetal = _pickup_date
                elif key == "storskrald":
                    storskrald = _pickup_date
                elif key == "storskraldogtekstilaffald":
                    storskraldogtekstilaffald = _pickup_date
                elif key == "haveaffald":
                    haveaffald = _pickup_date
                elif key == "glas":
                    glas = _pickup_date
                elif key == "papirglas":
                    papirglas = _pickup_date
                elif key == "plastmadkarton":
                    plastmadkarton = _pickup_date

                if _pickup_date is not None:
                    if _pickup_date < next_pickup:
                        next_pickup = _pickup_date
                        next_pickup_item = key

            sensor_data = RenoWebCollectionData(
                restaffaldmadaffald,
                glas,
                dagrenovation,
                metalglas,
                pappi,
                farligtaffald,
                farligtaffaldmiljoboks,
                flis,
                genbrug,
                jern,
                papir,
                papirmetal,
                pap,
                plastmetal,
                storskrald,
                storskraldogtekstilaffald,
                haveaffald,
                papirglas,
                plastmadkarton,
                next_pickup,
                next_pickup_item,
            )

            return sensor_data

    async def get_pickup_data(self, address_id: str) -> RenoWebCollectionData:
        """Get the garbage collection data."""

        if self._municipality_url is not None:
            url = f"https://{self._municipality_url}{API_URL_DATA}"
            body = {"adrid":f"{address_id}", "common":"false"}
            data = await self._api.async_api_request(url, body)
            result = json.loads(data['d'])
            garbage_data = result['list']

            pickup_events: PickupEvents = {}
            _next_pickup = dt.datetime(2030,12,31,23,59,00)
            _next_pickup_event: PickupType = None

            for row in garbage_data:
                if row["ordningnavn"] in NON_SUPPORTED_ITEMS:
                    continue

                _pickup_date = None
                if row['toemningsdato'] != "Ingen tømningsdato fundet!" and row['toemningsdato'] is not None:
                    _pickup_date = to_date(row['toemningsdato'])

                key = get_garbage_type(row['ordningnavn'])
                if key == row['ordningnavn'] and key != "Bestillerordning":
                    _LOGGER.warning("Garbage type %s is not defined in the system. Please notify the developer", key)
                    continue

                _pickup_event = {
                    key: PickupType(
                        date=_pickup_date,
                        group=row["ordningnavn"],
                        friendly_name=NAME_LIST.get(key),
                        icon=ICON_LIST.get(key),
                        entity_picture=f"{key}.svg",
                        description=row["materielnavn"],
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
                            )
                        }


            pickup_events.update(_next_pickup_event)
            return pickup_events

def to_date(datetext: str) -> dt.datetime:
    """Convert a date string to a datetime object."""
    if datetext == "Ingen tømningsdato fundet!":
        return None

    index = datetext.rfind(" ")
    return dt.datetime.strptime(f"{datetext[index+1:]} 00:00:00", "%d-%m-%Y %H:%M:%S")

def get_garbage_type(item: str) -> str:
    """Get the garbage type."""
    for key, value in SUPPORTED_ITEMS.items():
        if item in value:
            return key
    return item
