from sqlalchemy import (Column, DateTime, func, Integer, String, Float,
                        Boolean)
from bridgie.models.meta import Base, DBSession as session
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields
from bridgie.models.water_level import (WaterLevelSchema)


class LocationSchema(Schema):
    id = fields.Int()
    code = fields.Str(load_from="loc")
    name = fields.Str(load_from="locatienaam")
    latitude = fields.Float()
    longitude = fields.Float()
    water_levels = fields.Nested(WaterLevelSchema, many=True)


class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)
    code = Column(String(5))
    name = Column(String(40))
    latitude = Column(Float)
    longitude = Column(Float)

    has_prediction = Column(Boolean)

    date_created = Column(DateTime(timezone=True), default=func.now())
    date_updated = Column(DateTime(timezone=True),
                          default=func.now(),
                          onupdate=func.current_timestamp())

    water_levels = relationship("WaterLevel", backref='Location')

    def set_fields(self, data=None):
        for key, value in data.items():
            setattr(self, key, value)


def get_location_by_id(id):
    return session.query(Location).get(id)


def list_locations():
    return session.query(Location)


def get_location_by_code(code):
    locations = session.query(Location)
    location = locations.filter(Location.code == code).one()
    return location
