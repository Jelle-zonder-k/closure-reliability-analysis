# main.py
from fastapi import FastAPI, Request, Path, Query, HTTPException
from typing import List
from reliability.data_handler import StormSurgeBarrierDataHandler
from reliability.fast_api_logger import log_request, log_response
from reliability.pydantic_model import StormSurgeBarrierClosureEvents, StormSurgeBarriers, IndividualStormSurgeBarrierGates, IndividualGateClosures
from datetime import date, time

app = FastAPI()
DATA_HANDLER = StormSurgeBarrierDataHandler()
all_abbreviations = DATA_HANDLER.get_all_abbreviations()


@app.get("/storm_surge_barriers/", response_model=list[StormSurgeBarriers])
async def get_storm_surge_barriers(request: Request):
    await log_request(request)
    return log_response(DATA_HANDLER.get_all_barriers())


@app.get("/barrier_closures/", response_model=list[StormSurgeBarrierClosureEvents])
async def get_barrier_closures(request: Request):
    await log_request(request)
    return log_response(DATA_HANDLER.get_all_closures())


@app.put("/upsert_storm_surge_barrier/", response_model=StormSurgeBarriers)
async def upsert_storm_surge_barrier(barrier: StormSurgeBarriers):
    barrier_dict = barrier.dict()
    DATA_HANDLER.upsert_barrier(barrier_dict)
    return barrier


@app.put("/barrier_closures/{abbreviation}/")
async def upsert_barrier_closures(
    closure: List[dict],
    request: Request,
    abbreviation: str = Path(...,
                             description="The abbreviation of the barrier")
):
    await log_request(request)
    DATA_HANDLER.upsert_closure_data_list(closure, abbreviation)
    return log_response({"message": "Upsert successful"})


@app.put("/single_barrier_closure/{abbreviation}/")
async def insert_single_barrier_closure(
    closure: dict,
    request: Request,
    abbreviation: str = Path(...,
                             description="The abbreviation of the barrier")
):
    await log_request(request)
    try:
        result = DATA_HANDLER.insert_single_closure(
            abbreviation=abbreviation,
            start_date=closure.start_date,
            start_time=closure.start_time,
            end_date=closure.end_date,
            end_time=closure.end_time,
            closure_event_type=closure.closure_event_type,
            success=closure.success
        )
        if result:
            response_message = {"message": "Insert successful"}
        else:
            response_message = {"message": "Duplicate entry found"}
        return log_response(response_message)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
