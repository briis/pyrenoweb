import datetime
from dataclasses import dataclass, field

@dataclass
class RenowWebDataItem:
    """Represent a RenoWeb data itm."""
    key: str
    date: datetime.date
    date_long: str
    date_short: str
    icon: str
    icon_color: str
    valid_data: bool
    name: str
    schedule: str
    days_to: int
    state_text: str
    fraction_id: str
    last_refresh: datetime.datetime

@dataclass
class RenoWebDataSet:
    """Represent a RenoWeb dataset"""
    key: str
    item: list[RenowWebDataItem] = field(default_factory=list)

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
    def pickup_date(self) -> datetime.date:
        """Return the pickup date."""
        if self.toemningsdato is None:
            return None
        
        index = self.toemningsdato.rfind(" ")
        return datetime.datetime.strptime(self.toemningsdato[index+1:], "%d-%m-%Y").date()
    