import datetime as dt
from dataclasses import dataclass
import logging

_LOGGER = logging.getLogger(__name__)


@dataclass
class RenoWebAddressInfo:
    """Represent RenoWeb address info."""

    address_id: str
    kommunenavn: str
    vejnavn: str
    husnr: str


@dataclass(frozen=True)
class PickupType:
    """Define a waste pickup type."""

    date: dt.date | None = None
    group: str | None = None
    friendly_name: str | None = None
    icon: str | None = None
    entity_picture: str | None = None
    description: str | None = None
    last_updated: str | None = None


@dataclass(frozen=True)
class PickupEvents:
    """Represent RenoWeb collection data."""

    restaffaldmadaffald: list[PickupType] | None = None
    batterier: list[PickupType] | None = None
    elektronik: list[PickupType] | None = None
    papirglasdaaser: list[PickupType] | None = None
    glas: list[PickupType] | None = None
    dagrenovation: list[PickupType] | None = None
    metalglas: list[PickupType] | None = None
    pappi: list[PickupType] | None = None
    farligtaffald: list[PickupType] | None = None
    farligtaffaldmiljoboks: list[PickupType] | None = None
    flis: list[PickupType] | None = None
    genbrug: list[PickupType] | None = None
    jern: list[PickupType] | None = None
    papir: list[PickupType] | None = None
    papirmetal: list[PickupType] | None = None
    pap: list[PickupType] | None = None
    plastmetal: list[PickupType] | None = None
    storskrald: list[PickupType] | None = None
    storskraldogtekstilaffald: list[PickupType] | None = None
    haveaffald: list[PickupType] | None = None
    papirglas: list[PickupType] | None = None
    plastmadkarton: list[PickupType] | None = None
    next_pickup: list[PickupType] | None = None
