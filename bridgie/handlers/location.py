from pyramid.view import view_config
from bridgie.models.location import (list_locations, LocationSchema)


@view_config(route_name='location.list',
             renderer='json',
             request_method='GET',
             permission='public')
def list(request):
    return LocationSchema(many=True).dump(list_locations())
