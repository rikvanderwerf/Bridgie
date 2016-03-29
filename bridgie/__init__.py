from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from.models.meta import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('data.get', '/')
    config.add_route('location.list', '/locations')
    config.add_route('bridge.add', '/bridge/add')
    config.add_route('bridge.get', '/bridge/{bridge_id}')
    config.add_route('bridge.list', '/bridges')
    config.add_route('water_level.list', '/locations/{location_id}/water_levels')
    config.scan('bridgie.handlers')
    return config.make_wsgi_app()
