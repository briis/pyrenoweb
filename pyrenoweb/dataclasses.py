"""Defines the Data Classes used."""

import datetime


class PickupData:
    """A representation of all data available for a Pickup Location."""

    def __init__(self, data):
        """Pick-Up data."""

        self._type = data["type"]
        self._description = data["description"]
        self._nextpickupdatetext= data["nextpickupdate"]
        self._nextpickupdate = data["nextpickupdatetimestamp"]
        self._schedule = data["schedule"]

    @property
    def type(self) -> str:
        """Return Sensor Type."""
        return self._type
        
    @property
    def description(self) -> str:
        """Return Sensor Description."""
        return self._description
        
    @property
    def nextpickupdatetext(self) -> str:
        """Return Next pickup date as text."""
        return self._nextpickupdatetext
        
    @property
    def nextpickupdate(self) -> datetime.date:
        """Return Next pickup date as Date."""
        next_pickup = datetime.date.fromtimestamp(int(self._nextpickupdate))
        return next_pickup.isoformat()
        
    @property
    def schedule(self) -> str:
        """ReturnPick-Up schedule."""
        return self._schedule
        
    @property
    def daysuntilpickup(self) -> int:
        """Return days until next pick-up."""
        next_pickup = datetime.date.fromtimestamp(int(self._nextpickupdate))
        today = datetime.date.today()
        return (next_pickup - today).days

