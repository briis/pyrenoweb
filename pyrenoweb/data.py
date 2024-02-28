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
    group: str | None = None
    friendly_name: str | None = None
    icon: str | None = None
    entity_picture: str | None = None
    description: str | None = None

@dataclass(frozen=True)
class PickupEvents:
    """Represent RenoWeb collection data."""
    restaffaldmadaffald: list[PickupType] | None = None
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

