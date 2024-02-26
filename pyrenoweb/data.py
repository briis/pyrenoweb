import datetime as dt
from dataclasses import dataclass, field
import logging

from .const import (
    ICON_LIST,
    NAME_LIST,
)
EPOCHORDINAL = dt.datetime(1970, 1, 1).toordinal()
UTC = dt.UTC

_LOGGER = logging.getLogger(__name__)

@dataclass
class RenoWebAddressInfo:
    """Represent RenoWeb address info."""
    address_id: str
    kommunenavn: str
    vejnavn: str
    husnr: str

@dataclass
class RenoWebCollectionData:
    """Represent RenoWeb collection data."""
    restaffaldmadaffald: dt.datetime
    restmad: dt.datetime
    dagrenovation: dt.datetime
    metalglas: dt.datetime
    pappi: dt.datetime
    farligtaffald: dt.datetime
    farligtaffaldmiljoboks: dt.datetime
    flis: dt.datetime
    tekstiler: dt.datetime
    jern: dt.datetime
    papir: dt.datetime
    papirmetal: dt.datetime
    pap: dt.datetime
    plastmetal: dt.datetime
    storskrald: dt.datetime
    storskraldogtekstilaffald: dt.datetime
    haveaffald: dt.datetime
    next_pickup: dt.datetime
    next_pickup_item: str

@dataclass(order=True)
class RenoWebPickupData:
    """Represent RenoWeb pickup data."""
    sort_index: int = field(init=False, repr=False)
    id: int
    materielnavn: str
    ordningnavn: str
    toemningsdage: str
    toemningsdato: str
    toemningsint: int
    mattypeid: int
    antal: int
    vejnavn: str
    fractionid: int
    modulId: int

    @property
    def icon(self) -> str:
        """Return the icon."""
        if self.ordningnavn is None:
            return None

        for key, value in ICON_LIST.items():
            if self.ordningnavn == key:
                return value
        return "mdi:delete-empty"

    @property
    def name(self) -> str:
        """Return the name."""
        if self.ordningnavn is None:
            return None

        for key, value in NAME_LIST.items():
            if self.ordningnavn == key:
                return value
        return self.ordningnavn

    @property
    def pickup_date(self) -> dt.datetime:
        """Return the pickup date."""
        if self.toemningsdato is None:
            return None

        if self.toemningsdato == "Ingen tømningsdato fundet!":
            return None

        index = self.toemningsdato.rfind(" ")
        return dt.datetime.strptime(f"{self.toemningsdato[index+1:]} 00:00:00", "%d-%m-%Y %H:%M:%S").isoformat()

    @property
    def timestamp(self) -> float:
        """Return the timestamp."""
        if self.toemningsdato is None:
            return None

        if self.toemningsdato == "Ingen tømningsdato fundet!":
            return None

        index = self.toemningsdato.rfind(" ")
        return utc_to_timestamp(as_utc(dt.datetime.strptime(f"{self.toemningsdato[index+1:]} 00:00:00", "%d-%m-%Y %H:%M:%S")))

def as_utc(dattim: dt.datetime) -> dt.datetime:
    """Return a datetime as UTC time.

    Assumes datetime without tzinfo to be in the DEFAULT_TIME_ZONE.
    """
    if dattim.tzinfo == UTC:
        return dattim
    if dattim.tzinfo is None:
        tz = dt.datetime.now(dt.timezone.utc).astimezone().tzinfo
        dattim = dattim.replace(tzinfo=tz)

    return dattim.astimezone(UTC)

def utc_to_timestamp(utc_dt: dt.datetime) -> float:
    """Fast conversion of a datetime in UTC to a timestamp."""
    # Taken from
    # https://github.com/python/cpython/blob/3.10/Lib/zoneinfo/_zoneinfo.py#L185
    return (
        (utc_dt.toordinal() - EPOCHORDINAL) * 86400
        + utc_dt.hour * 3600
        + utc_dt.minute * 60
        + utc_dt.second
        + (utc_dt.microsecond / 1000000)
    )
