# main.py
from fastapi import FastAPI, Request, Path, Query, HTTPException
from typing import List
from data_handler import StormSurgeBarrierDataHandler
from fast_api_logger import log_request, log_response
from pydantic_model import StormSurgeBarrierClosureEvents, StormSurgeBarriers
from enums.closure_event_result import ClosureEventResult
from enums.closure_event_type import ClosureEventType
from datetime import date

app = FastAPI()
DATA_HANDLER = StormSurgeBarrierDataHandler()
all_abbreviations = DATA_HANDLER.get_all_abbreviations()


@app.get("/storm_surge_barrier/all/", response_model=list[StormSurgeBarriers])
async def get_storm_surge_barriers(request: Request):
    await log_request(request)
    return log_response(DATA_HANDLER.get_all_barriers())


@app.get("/storm_surge_barrier/all/closures/", response_model=list[StormSurgeBarrierClosureEvents])
async def get_barrier_closures(request: Request):
    await log_request(request)
    return log_response(DATA_HANDLER.get_all_closures())


@app.put("/storm_surge_barrier/add/")
async def upsert_storm_surge_barrier(
    Name: str = Query(..., description="Name of the barrier"),
    Abbreviation: str = Query(..., description="Abbreviation for the barrier"),
    Location: str = Query(..., description="Location of the barrier"),
    ConstructionYear: int = Query(...,
                                  description="Construction year of the barrier"),
    GateConfiguration: str = Query(...,
                                   description="Gate configuration of the barrier"),
    GateType: str = Query(..., description="Type of the gate")
):
    barrier_data = {
        "Name": Name,
        "Abbreviation": Abbreviation,
        "Location": Location,
        "ConstructionYear": ConstructionYear,
        "GateConfiguration": GateConfiguration,
        "GateType": GateType
    }
    DATA_HANDLER.upsert_barrier(barrier_data)
    return barrier_data


@app.get("/storm_surge_barrier/closures/{abbreviation}/", response_model=list[StormSurgeBarrierClosureEvents])
async def get_barrier_closures(abbreviation: str = Path(..., description="The abbreviation of the barrier")):
    return DATA_HANDLER.get_closures_by_abbreviation(abbreviation)


@app.post("/storm_surge_barrier/add/closure/")
async def insert_single_closure_event(
    request: Request,
    StartDate: date = Query(...,
                            description="The start date of the event"),
    EndDate: date = Query(..., description="The end date of the event"),
    StartTime: str = Query(
        ...,
        description="The start time of the event (in HH:MM format)",
        regex="^(?:[01]\d|2[0-3]):[0-5]\d$",
        example="08:00"
    ),
    EndTime: str = Query(
        ...,
        description="The end time of the event (in HH:MM format)",
        regex="^(?:[01]\d|2[0-3]):[0-5]\d$",
        example="18:00"
    ),
    ClosureEventType: ClosureEventType = Query(
        ..., description="Type of the closure event"),
    ClosureEventResult: ClosureEventResult = Query(
        ..., description="Result of the closure event"),
    BarrierID: int = Query(..., description="The ID of the barrier"),
    WaterLevel: float = Query(...,
                              description="The water level at the time of the event"),
    abbreviation: str = Query(...,
                              description="The abbreviation of the barrier")
):
    await log_request(request)
    closure = {
        "StartDate": StartDate,
        "EndDate": EndDate,
        "StartTime": StartTime,
        "EndTime": EndTime,
        "ClosureEventType": ClosureEventType,
        "ClosureEventResult": ClosureEventResult,
        "BarrierID": BarrierID,
        "WaterLevel": WaterLevel
    }
    response = DATA_HANDLER.insert_single_closure_event(abbreviation, closure)

    if response[1] != 201:
        raise HTTPException(
            status_code=response[1], detail=response[0]["message"])

    return log_response({"message": "Insert successful"})


@app.post("/storm_surge_barrier/add/closures/{abbreviation}/")
async def insert_closure_events_endpoint(abbreviation: str, closure_data: List[dict]):
    result = DATA_HANDLER.insert_closure_events(abbreviation, closure_data)
    return result


@app.get("/storm_surge_barrier/closures/rule_of_three/{abbreviation}/")
async def get_rule_of_three(abbreviation: str, closure_type: ClosureEventType = None, rule_number: int = 3):
    return DATA_HANDLER.calculate_rule_of_three(abbreviation, closure_type, rule_number)


@app.get("/storm_surge_barrier/closures/failure_rate_update/{abbreviation}/")
async def get_beta_distribution(abbreviation: str, closure_type: ClosureEventType = None, prior_failure_rate: float = 0.5):
    return DATA_HANDLER.calculate_beta_distribution(abbreviation, closure_type, prior_failure_rate)
