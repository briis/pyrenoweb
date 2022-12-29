"""Dataclasses for pyRenoWeb"""
from __future__ import annotations

from dataclasses import dataclass, field

import datetime

@dataclass
class RenoWebSensorDescription:
    """Describes a RenowWeb Sensor Structur."""

    key: str

    date: datetime.datetime
    icon: str
    valid_data: bool
    days_to: int = field(init=False)
    icon_color: str = field(init=False)
    device_class: str | None = "date"
    suggested_unit_of_measurement: str | None = "date"
    name: str | None = None
    schedule: str | None = None
    picture: str | None = None

    def __post_init__(self):
        self.days_to = (self.date - datetime.datetime.now()).days

        if self.days_to == 0:
            icon_color = "#F54336"
        elif self.days_to == 1:
            icon_color = "#FFC108"
        else:
            icon_color = "#9E9E9E"
        self.icon_color = icon_color