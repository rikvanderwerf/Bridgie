from sqlalchemy import (Column, DateTime, func, Integer,
                        ForeignKey, Boolean)
from sqlalchemy.orm import relationship
from bridgie.models.meta import Base, DBSession as session


class WaterLevel(Base):
    __tablename__ = 'water_level'

    id = Column(Integer, primary_key=True)

    location_id = Column(Integer, ForeignKey('location.id'))
    timestamp = Column(DateTime())
    water_level_height = Column(Integer)  # in cm
    predicted = Column(Boolean)

    location = relationship('Location')

    date_created = Column(DateTime(timezone=True), default=func.now())
    date_updated = Column(DateTime(timezone=True),
                          default=func.now(),
                          onupdate=func.current_timestamp())


def get_water_level_by_id(id):
    return session.query(WaterLevel).get(id)


def list_water_levels():
    return session.query(WaterLevel)
