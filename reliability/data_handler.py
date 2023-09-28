from dataclasses import dataclass
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from reliability import data_model
from reliability.database.session_factory import SessionFactory
from typing import List
from datetime import date, time


@dataclass
class StormSurgeBarrierDataHandler:
    # Any other handlers can be added here if required

    def __post_init__(self):
        pass

    def upsert_barrier(self, barrier_dict: dict):
        """Insert a new storm surge barrier or update an existing one."""
        session = SessionFactory()
        existing_barrier = session.query(data_model.StormSurgeBarriers).filter_by(
            Abbreviation=barrier_dict['Abbreviation']).first()

        if existing_barrier is not None:
            for key, value in barrier_dict.items():
                setattr(existing_barrier, key, value)
        else:
            new_barrier = data_model.StormSurgeBarriers(**barrier_dict)
            session.add(new_barrier)

        session.commit()

    def put_closure_data(self, closure_dict: dict):
        """Insert closure data into the database."""
        session = SessionFactory()
        new_closure = data_model.StormSurgeBarrierClosureEvents(**closure_dict)
        session.add(new_closure)
        session.commit()

    def get_all_barriers(self) -> list[dict]:
        """Retrieve all storm surge barriers from the database."""
        session = SessionFactory()
        barriers = session.query(data_model.StormSurgeBarriers).all()
        return jsonable_encoder([barrier.to_dict() for barrier in barriers])

    def get_all_closures(self) -> list[dict]:
        """Retrieve all closures for storm surge barriers from the database."""
        session = SessionFactory()
        closures = session.query(
            data_model.StormSurgeBarrierClosureEvents).all()
        return jsonable_encoder([closure.to_dict() for closure in closures])

    def upsert_closure_data_list(self, closure_list: list, abbreviation: str):
        """Upsert a list of closure data into the database."""
        session = SessionFactory()

        # Identify the barrier ID based on the abbreviation
        barrier_id = session.query(data_model.StormSurgeBarriers.ID).filter_by(
            Abbreviation=abbreviation).first()

        for closure_dict in closure_list:
            try:
                # Skip record if StartDate or EndDate is 'NaT'
                if closure_dict["StartDate"] == 'NaT' or closure_dict["EndDate"] == 'NaT':
                    continue

                # Check if record exists
                existing_record = session.query(data_model.StormSurgeBarrierClosureEvents).filter_by(
                    StartDate=closure_dict["StartDate"],
                    EndDate=closure_dict["EndDate"],
                    BarrierID=barrier_id
                ).first()

                if existing_record:
                    # Update existing record
                    for key, value in closure_dict.items():
                        setattr(existing_record, key, value)
                else:
                    # Insert new record
                    new_closure = data_model.StormSurgeBarrierClosureEvents(
                        **closure_dict, BarrierID=barrier_id)
                    session.add(new_closure)

            except Exception as e:
                print(f"Skipping record due to error: {e}")
                continue

        session.commit()

    def insert_single_closure(self, abbreviation: str, start_date: date, start_time: time, end_date: date, end_time: time, closure_event_type: str, success: bool):
        """Insert a single closure data into the database."""
        session = SessionFactory()

        # Identify the barrier ID based on the abbreviation
        barrier_id = session.query(data_model.StormSurgeBarriers.ID).filter_by(
            Abbreviation=abbreviation).first()

        # Create dictionary from provided data
        closure_dict = {
            "StartDate": start_date,
            "StartTime": start_time,
            "EndDate": end_date,
            "EndTime": end_time,
            "ClosureEventType": closure_event_type,
            "Success": success
        }

        # Check for duplicate entries based on StartDate, EndDate, and BarrierID
        existing_record = session.query(data_model.StormSurgeBarrierClosureEvents).filter_by(
            StartDate=start_date,
            EndDate=end_date,
            BarrierID=barrier_id
        ).first()

        if existing_record:
            print("Duplicate entry found. Skipping record.")
            return False

        # Insert new record
        new_closure = data_model.StormSurgeBarrierClosureEvents(
            **closure_dict, BarrierID=barrier_id)
        session.add(new_closure)
        session.commit()

        return True

    def get_all_abbreviations(self) -> list[str]:
        """Retrieve all abbreviations for storm surge barriers from the database."""
        session = SessionFactory()
        abbreviations = session.query(
            data_model.StormSurgeBarriers.Abbreviation).all()
        return [item[0] for item in abbreviations]
