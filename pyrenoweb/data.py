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

    date: dt.datetime
    friendly_name: str | None = None
    icon: str | None = None
    entity_picture: str | None = None
    description: str | None = None

@dataclass(frozen=True)
class PickupEvents:
    """Represent RenoWeb collection data."""
    restaffaldmadaffald: list[PickupType]
    glas: list[PickupType]
    dagrenovation: list[PickupType]
    metalglas: list[PickupType]
    pappi: list[PickupType]
    farligtaffald: list[PickupType]
    farligtaffaldmiljoboks: list[PickupType]
    flis: list[PickupType]
    genbrug: list[PickupType]
    jern: list[PickupType]
    papir: list[PickupType]
    papirmetal: list[PickupType]
    pap: list[PickupType]
    plastmetal: list[PickupType]
    storskrald: list[PickupType]
    storskraldogtekstilaffald: list[PickupType]
    haveaffald: list[PickupType]
    papirglas: list[PickupType]
    plastmadkarton: list[PickupType]
    next_pickup: list[PickupType]
    next_pickup_item: str


@dataclass
class RenoWebCollectionData:
    """Represent RenoWeb collection data."""
    restaffaldmadaffald: dt.datetime
    glas: dt.datetime
    dagrenovation: dt.datetime
    metalglas: dt.datetime
    pappi: dt.datetime
    farligtaffald: dt.datetime
    farligtaffaldmiljoboks: dt.datetime
    flis: dt.datetime
    genbrug: dt.datetime
    jern: dt.datetime
    papir: dt.datetime
    papirmetal: dt.datetime
    pap: dt.datetime
    plastmetal: dt.datetime
    storskrald: dt.datetime
    storskraldogtekstilaffald: dt.datetime
    haveaffald: dt.datetime
    papirglas: dt.datetime
    plastmadkarton: dt.datetime
    next_pickup: dt.datetime
    next_pickup_item: str

