from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Optional
from enum import Enum
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


class ClosureEventTypeEnum(str, Enum):
    STORM = 'STORM'
    OPS = 'OPS'
    TEST = 'TEST'


class ClosureEventResultEnum(str, Enum):
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'


class SingleClosureEvent(BaseModel):
    StartDate: date = Field(..., description="The start date of the event",
                            example="2023-09-28")
    EndDate: date = Field(..., description="The end date of the event",
                          example="2023-09-29")
    StartTime: str = Field(
        ...,
        description="The start time of the event (in HH:MM format)",
        regex="^(?:[01]\d|2[0-3]):[0-5]\d$",
        example="08:00"
    )
    EndTime: str = Field(
        ...,
        description="The end time of the event (in HH:MM format)",
        regex="^(?:[01]\d|2[0-3]):[0-5]\d$",
        example="18:00"
    )
    ClosureEventType: ClosureEventTypeEnum = Field(
        ..., description="Type of the closure event")
    ClosureEventResult: ClosureEventResultEnum = Field(
        ..., description="Result of the closure event")
    BarrierID: int = Field(..., description="The ID of the barrier")
    WaterLevel: float = Field(...,
                              description="The water level at the time of the event",
                              example=1.5)


class BetaDistributionInput(BaseModel):
    abbreviation: str
    closure_type: Optional[str] = None
    prior_failure_rate: Optional[float] = None


class BetaDistributionResult(BaseModel):
    expected_failure_rate: float
