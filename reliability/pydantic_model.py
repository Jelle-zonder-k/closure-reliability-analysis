from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Optional

from pydantic import BaseModel, Field


class StormSurgeBarrierClosureEvents(BaseModel):
    ID: int
    BarrierID: int
    StartDate: date
    EndDate: date
    ClosureEventType: str
    ClosureEventResult: Optional[str]
    StartTime: Optional[str]
    EndTime: Optional[str]


class StormSurgeBarriers(BaseModel):
    Name: str
    Abbreviation: str
    Location: str
    ConstructionYear: int
    GateConfiguration: str
    GateType: str


class IndividualStormSurgeBarrierGates(BaseModel):
    ID: int
    Name: str
    BarrierID: int


class IndividualGateClosures(BaseModel):
    ID: int
    GateID: int
    BarrierClosureID: int
    StartDate: date
    EndDate: date
    ClosureResult: str


class SingleClosureData(BaseModel):
    start_date: date
    start_time: time
    end_date: date
    end_time: time
    closure_event_type: str
    success: bool
