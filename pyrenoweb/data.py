import datetime
from dataclasses import dataclass, field

from .const import (
    ICON_LIST,
    NAME_LIST,
)

@dataclass
class RenoWebPickupData:
    """Represent RenoWeb pickup data."""
    id: int
    materielnavn: str
    ordningnavn: str
    toemningsdage: str
    toemningsdato: str
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
    def pickup_date(self) -> datetime.date:
        """Return the pickup date."""
        if self.toemningsdato is None:
            return None

        index = self.toemningsdato.rfind(" ")
        return datetime.datetime.strptime(self.toemningsdato[index+1:], "%d-%m-%Y").date()
