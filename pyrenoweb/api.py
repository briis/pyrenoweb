"""This module contains the code to get garbage data from Renoweb."""
from __future__ import annotations

import abc
import datetime
import json
import logging

from typing import Any
from urllib.request import urlopen

import aiohttp

from .const import (
    API_URL_DATA,
    API_URL_SEARCH,
    MUNICIPALITIES_LIST,
)
from .data import RenoWebPickupData

_LOGGER = logging.getLogger(__name__)


class RenowWebNotSupportedError(Exception):
    """Raised when the municipality is not supported."""

class RenowWebNotValidAddressError(Exception):
    """Raised when the address is not found."""

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

        # _LOGGER.debug("URL: %s", url)
        # _LOGGER.debug("BODY: %s", body)
        is_new_session = False
        if self.session is None:
            self.session = aiohttp.ClientSession()
            is_new_session = True

        headers = {'Content-Type': 'application/json'}
        self.session.headers.update(headers)

        async with self.session.post(url, data=json.dumps(body)) as response:
            if response.status != 200:
                if is_new_session:
                    await self.session.close()

                if response.status == 400:
                    raise RenowWebNotSupportedError("Municipality not supported")

                if response.status == 404:
                    raise RenowWebNotSupportedError("Municipality not supported")

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


    async def async_init(self) -> None:
        """Initialize the connection."""
        if self._municipality is not None:
            for key, value in MUNICIPALITIES_LIST.items():
                if key == self._municipality.lower():
                    self._municipality_url = value
                    break

            url = f"https://{self._municipality_url}{API_URL_SEARCH}"
            body = {"searchterm":f"{self._street} {self._house_number}", "addresswithmateriel":7}
            data: dict[str, Any] = await self._api.async_api_request(url, body)


    async def get_address_id(self, street: str, house_number: str) -> str:
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

            return self._address_id
        else:
            raise RenowWebNotSupportedError("Cannot find Municipality")

    async def get_data(self, address_id: str) -> dict[str, Any]:
        """Get the garbage collection data."""

        pickup_data: list[RenoWebPickupData] = []
        if self._municipality_url is not None:
            url = f"https://{self._municipality_url}{API_URL_DATA}"
            body = {"adrid":f"{address_id}", "common":"false"}
            data = await self._api.async_api_request(url, body)
            result = json.loads(data['d'])
            garbage_data = result['list']
            for row in garbage_data:
                pickup_data.append(
                    RenoWebPickupData(
                        row['id'],
                        row['materielnavn'],
                        row['ordningnavn'],
                        row['toemningsdage'],
                        row['toemningsdato'],
                        row['mattypeid'],
                        row['antal'],
                        row['vejnavn'],
                        row['fractionid'],
                        row['modulId'],
                    )
                )
            return pickup_data