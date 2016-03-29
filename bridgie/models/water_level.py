from sqlalchemy import (Column, DateTime, func, Integer,
                        ForeignKey, Boolean)
from sqlalchemy.orm import relationship
from datetime import datetime
from marshmallow import Schema, fields
from bridgie.models.meta import Base, DBSession as session


class WaterLevelSchema(Schema):
    id = fields.Int()
    time = fields.Str(load_from="tijd", required=True)
    water_level_height = fields.Str(load_from="waarde", required=True)
    datetime = fields.Date()


class WaterLevel(Base):
    __tablename__ = 'water_level'

    id = Column(Integer, primary_key=True)

    location_id = Column(Integer, ForeignKey('location.id'))
    time = Column(Integer)
    water_level_height = Column(Integer)  # in cm
    predicted = Column(Boolean)

    location = relationship('Location', backref='waterlevels')

    date_created = Column(DateTime(timezone=True), default=func.now())
    date_updated = Column(DateTime(timezone=True),
                          default=func.now(),
                          onupdate=func.current_timestamp())


    @property
    def datetime(self):
        return datetime.utcfromtimestamp(self.time)

    def set_fields(self, data=None):
        for key, value in data.items():
            setattr(self, key, value)


def get_water_level_by_id(id):
    return session.query(WaterLevel).get(id)


def get_water_level(location_id, time):
    q = session.query(WaterLevel)
    q = q.filter(WaterLevel.location_id == location_id)
    return q.filter(WaterLevel.time == time).one()


def list_water_levels_by_location(location_id):
    q = session.query(WaterLevel).filter(WaterLevel.location_id == location_id)
    return q.order_by(WaterLevel.time.desc())
