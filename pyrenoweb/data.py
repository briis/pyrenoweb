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
