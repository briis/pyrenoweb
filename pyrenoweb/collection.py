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
    name: str | None = None
    schedule: str | None = None
    picture: str | None = None

    def __post_init__(self):
        self.days_to = (self.date - datetime.datetime.now()).days
