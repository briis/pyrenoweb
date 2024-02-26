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

