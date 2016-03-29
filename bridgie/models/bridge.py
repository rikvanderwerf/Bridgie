from sqlalchemy import (Column, DateTime, func, Integer,
                        Float, String)
from bridgie.models.meta import Base, DBSession as session
from marshmallow import Schema, fields
from bridgie.models.location import list_locations, LocationSchema
from math import radians, sin, cos, asin, sqrt


class BridgeSchema(Schema):
    id = fields.Int()
    name = fields.Str(load_from="locatienaam")
    latitude = fields.Float()
    longitude = fields.Float()
    height = fields.Integer()
    closest_location = fields.Nested(LocationSchema)


class Bridge(Base):
    __tablename__ = 'bridge'

    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    latitude = Column(Float)
    longitude = Column(Float)
    height = Column(Integer)

    date_created = Column(DateTime(timezone=True), default=func.now())
    date_updated = Column(DateTime(timezone=True),
                          default=func.now(),
                          onupdate=func.current_timestamp())

    @property
    def closest_location(self):
        locations = list_locations()
        earth_radius_miles = 3956
        lowest_distance = 100000
        closest_location = ''
        for location in locations:
            dlat, dlon = (location.latitude - self.latitude, location.longitude - self.longitude)
            a = sin(dlat/2.0)**2 + cos(self.latitude) * cos(location.latitude) * sin(dlon/2.0)**2
            great_circle_distance = 2 * asin(min(1,sqrt(a)))
            d = earth_radius_miles * great_circle_distance
            if d < lowest_distance:
                lowest_distance = d
                closest_location = location

        return closest_location


def get_bridge_by_id(id):
    return session.query(Bridge).get(id)


def list_bridges():
    return session.query(Bridge)
