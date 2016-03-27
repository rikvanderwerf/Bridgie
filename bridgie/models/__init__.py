import logging
import transaction
from bridgie.models.meta import DBSession as session

# import eventfriendcore.models.user  # noqa

log = logging.getLogger(__name__)


def commit():
    log.debug("Committing session: %r", session.dirty)
    transaction.commit()


def persist(obj):
    log.debug("persisting object %r", obj)
    session.add(obj)


def delete(obj):
    log.debug("deleting object %r", obj)
    session.delete(obj)


def merge(obj):
    log.debug("merging %r", obj)
    return session.merge(obj)


def rollback():
    log.debug("Rolling back session: %r", session.dirty)
    return session.rollback()


def expire(obj, attrs=None):
    args = (obj,)
    if attrs:
        args = (obj, attrs)
    session.expire(*args)
