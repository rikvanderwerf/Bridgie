from sqlalchemy import (Column, DateTime, func, Integer,
                        Float, String)
from bridgie.models.meta import Base, DBSession as session


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


def get_bridge_by_id(id):
    return session.query(Bridge).get(id)


def list_bridges():
    return session.query(Bridge)
