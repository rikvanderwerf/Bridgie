from pyramid.view import view_config
from bridgie.models.location import (list_locations, LocationSchema, get_location_by_id)


@view_config(route_name='location.list',
             renderer='json',
             request_method='GET',
             permission='public')
def list(request):
    return LocationSchema(many=True).dump(list_locations())


@view_config(route_name='location.get',
             renderer='json',
             request_method='GET',
             permission='public')
def get(request):
    location_id = request.matchdict['location_id']
    return LocationSchema().dump(get_location_by_id(location_id))