from dataclasses import dataclass
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from  import data_model
from database.session_factory import SessionFactory
from typing import List, Optional
import numpy as np


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

    def get_closures_by_abbreviation(self, abbreviation: str) -> list[dict]:
        """Retrieve all closures for a specific storm surge barrier based on its abbreviation from the database."""
        session = SessionFactory()

        # Identify the barrier ID based on the abbreviation
        barrier_id = session.query(data_model.StormSurgeBarriers.ID).filter_by(
            Abbreviation=abbreviation).first()

        if not barrier_id:
            return []  # Return empty list if no barrier found with given abbreviation

        # Fetch closures for the identified barrier
        closures = session.query(data_model.StormSurgeBarrierClosureEvents).filter_by(
            BarrierID=barrier_id
        ).all()

        # Convert the ORM objects to dictionaries
        return jsonable_encoder([closure.to_dict() for closure in closures])

    def insert_single_closure_event(self, abbreviation: str, event: dict):
        session = SessionFactory()
        barrier_id = session.query(data_model.StormSurgeBarriers.ID).filter_by(
            Abbreviation=abbreviation).first()
        if not barrier_id:
            return {"message": "Barrier not found"}, 404

        existing_record = session.query(data_model.StormSurgeBarrierClosureEvents).filter_by(
            StartDate=event["StartDate"],
            EndDate=event["EndDate"],
            BarrierID=barrier_id
        ).first()

        if existing_record:
            return {"message": "Duplicate entry found. Skipping record."}, 409

        new_event = data_model.StormSurgeBarrierClosureEvents(
            **event, BarrierID=barrier_id)
        session.add(new_event)
        session.commit()
        session.refresh(new_event)

        return {"message": "Insert successful", "inserted_event": new_event.to_dict()}, 201

    def get_all_abbreviations(self) -> list[str]:
        """Retrieve all abbreviations for storm surge barriers from the database."""
        session = SessionFactory()
        abbreviations = session.query(
            data_model.StormSurgeBarriers.Abbreviation).all()
        return [item[0] for item in abbreviations]

    def insert_closure_events(self, abbreviation: str, closure_data: List[dict]) -> dict:
        session: Session = SessionFactory()

        # Identify the barrier ID based on the abbreviation
        barrier_id = session.query(data_model.StormSurgeBarriers.ID).filter_by(
            Abbreviation=abbreviation).scalar()

        if not barrier_id:
            raise ValueError(
                f"No barrier found with abbreviation: {abbreviation}")

        skipped_records = []

        for closure in closure_data:
            closure.setdefault("ClosureEventResult", "SUCCESS")
            try:
                # Check for existing record
                existing_record = session.query(data_model.StormSurgeBarrierClosureEvents).filter_by(
                    StartDate=closure["StartDate"],
                    StartTime=closure["StartTime"],
                    BarrierID=barrier_id
                ).first()

                if existing_record:
                    # Update existing record
                    for key, value in closure.items():
                        setattr(existing_record, key, value)
                else:
                    # Insert new record
                    new_closure = data_model.StormSurgeBarrierClosureEvents(
                        BarrierID=barrier_id, **closure)
                    session.add(new_closure)

                session.commit()
            except Exception as e:
                # Catch any error and skip the record
                session.rollback()
                skipped_records.append({
                    "record": closure,
                    "error": str(e)
                })

        return {"skipped_records": skipped_records}

    def calculate_rule_of_three(self, abbreviation: str, closure_type: Optional[str] = None, rule_number: int = 3) -> dict:
        session: Session = SessionFactory()
        barrier = session.query(data_model.StormSurgeBarriers).filter_by(
            Abbreviation=abbreviation).first()

        if not barrier:
            return {
                "message": f"No barrier found with abbreviation: {abbreviation}"
            }

        if closure_type:
            successful_closures = session.query(data_model.StormSurgeBarrierClosureEvents).filter_by(
                BarrierID=barrier.ID,
                ClosureEventResult="SUCCESS",
                ClosureEventType=closure_type
            ).count()
        else:
            successful_closures = session.query(data_model.StormSurgeBarrierClosureEvents).filter_by(
                BarrierID=barrier.ID,
                ClosureEventResult="SUCCESS"
            ).count()

        # Calculate p from rule_number
        p = 1 - np.exp(-rule_number)

        # Round p to the nearest decimal ending in .005
        p_rounded = round(p * 200) / 200

        # Determine confidence level based on rounded p
        confidence_level = p_rounded * 100

        if successful_closures == 0:
            return {
                "message": f"No successful closures found for barrier: {barrier.Name}. Using the rule of {rule_number}, is not applicable in this case.",
                "failure_rate": "1 in ∞"
            }

        failure_rate_upper_bound = rule_number / successful_closures
        response = {
            "barrier_name": barrier.Name,
            "confidence_interval": f"{confidence_level:.2f}%",
            "upper_bound": failure_rate_upper_bound,
            "message": f"Based on {successful_closures} successful"
        }
        if closure_type:
            response["message"] += f" {closure_type} closures"
        else:
            response["message"] += " closures."
        response[
            "message"] += f" for barrier: {barrier.Name}, the upper bound for the {confidence_level:.2f}% confidence interval is {failure_rate_upper_bound} (1 in {int(1/failure_rate_upper_bound)}) using the rule of {rule_number}."
        return response

    def calculate_beta_distribution(self, abbreviation: str, closure_type: Optional[str] = None, prior_failure_rate: Optional[float] = None) -> dict:
        a = 1
        b = 1

        if prior_failure_rate:
            total_prior = 1 / prior_failure_rate
            a = 1
            b = total_prior - a

        session: Session = SessionFactory()
        barrier = session.query(data_model.StormSurgeBarriers).filter_by(
            Abbreviation=abbreviation).first()

        if not barrier:
            return {
                "message": f"No barrier found with abbreviation: {abbreviation}"
            }

        if closure_type:
            successful_closures = session.query(data_model.StormSurgeBarrierClosureEvents).filter_by(
                BarrierID=barrier.ID,
                ClosureEventResult="SUCCESS",
                ClosureEventType=closure_type
            ).count()
        else:
            successful_closures = session.query(data_model.StormSurgeBarrierClosureEvents).filter_by(
                BarrierID=barrier.ID,
                ClosureEventResult="SUCCESS"
            ).count()

        unsuccessful_closures = session.query(data_model.StormSurgeBarrierClosureEvents).filter_by(
            BarrierID=barrier.ID,
            ClosureEventResult="FAILURE",
            ClosureEventType=closure_type if closure_type else None
        ).count()

        a_posterior = a + unsuccessful_closures
        b_posterior = b + successful_closures

        # Calculate the expected failure rate
        expected_failure_rate = a_posterior / (a_posterior + b_posterior)

        response = {
            "barrier_name": barrier.Name,
            "prior_failure_rate": prior_failure_rate if prior_failure_rate else None,
            "posterior_mean_failure_rate": expected_failure_rate,
            "informative_prior": True if prior_failure_rate else False,
            "message": f"For barrier: {barrier.Name}, using prior {prior_failure_rate} (1 in {int(1/prior_failure_rate)}) the posterior mean failure rate is approximately {expected_failure_rate:.6f} (1 in {int(1/expected_failure_rate)})"
        }
        if closure_type:
            response["message"] += f" for {closure_type} closures."
        else:
            response["message"] += " based on all closures."

        return response
