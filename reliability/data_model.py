from datetime import date, datetime
from typing import Any, List, Literal
from uuid import UUID

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.ext.hybrid import HybridExtensionType, hybrid_property
from sqlalchemy.orm import (DeclarativeBase, Mapped, class_mapper,
                            mapped_column, relationship)


class Base(DeclarativeBase):
    def to_dict(self):
        """Converts the class instance into a dictionary with all the columns and hybrid_properties as keys."""
        return {c: getattr(self, c) for c in get_columns(self.__class__)}


def get_columns(model):
    """Returns all the columns of the model class."""
    columns = [c.key for c in class_mapper(model).columns]
    hybrid_columns = [
        c.__name__
        for c in class_mapper(model).all_orm_descriptors
        if c.extension_type == HybridExtensionType.HYBRID_PROPERTY
    ]

    return columns + hybrid_columns


class StormSurgeBarriers(Base):
    __tablename__ = 'StormSurgeBarriers'
    ID: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str]
    Abbreviation: Mapped[str]
    Location: Mapped[str]
    ConstructionYear: Mapped[int]
    GateConfiguration: Mapped[str]
    GateType: Mapped[str]

    closures: Mapped["StormSurgeBarrierClosureEvents"] = relationship(
        "StormSurgeBarrierClosureEvents", lazy="joined")


class StormSurgeBarrierClosureEvents(Base):
    __tablename__ = 'StormSurgeBarrierClosureEvents'
    ID: Mapped[int] = mapped_column(primary_key=True)
    BarrierID: Mapped[int] = mapped_column(
        Integer, ForeignKey('StormSurgeBarriers.ID'))
    StartDate: Mapped[date]
    EndDate: Mapped[date]
    StartTime: Mapped[str]  # New field
    EndTime: Mapped[str]    # New field
    WaterLevel: Mapped[float]
    ClosureEventType: Mapped[str]
    ClosureEventResult: Mapped[str]

    barrier: Mapped["StormSurgeBarriers"] = relationship(
        "StormSurgeBarriers", lazy="joined")


class IndividualStormSurgeBarrierGates(Base):
    __tablename__ = 'IndividualStormSurgeBarrierGates'
    ID: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str]
    BarrierID: Mapped[int] = mapped_column(
        Integer, ForeignKey('StormSurgeBarriers.ID'))

    gate_closures: Mapped["IndividualGateClosures"] = relationship(
        "IndividualGateClosures", lazy="joined")


class IndividualGateClosures(Base):
    __tablename__ = 'IndividualGateClosures'
    ID: Mapped[int] = mapped_column(primary_key=True)
    GateID: Mapped[int] = mapped_column(Integer, ForeignKey(
        'IndividualStormSurgeBarrierGates.ID'))
    BarrierClosureID: Mapped[int] = mapped_column(
        Integer, ForeignKey('StormSurgeBarrierClosureEvents.ID'))
    StartDate: Mapped[date]
    EndDate: Mapped[date]
    ClosureResult: Mapped[str]

    gate: Mapped["IndividualStormSurgeBarrierGates"] = relationship(
        "IndividualStormSurgeBarrierGates", lazy="joined")
