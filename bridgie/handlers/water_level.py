from pyramid.view import view_config
from bridgie.models.water_level import (WaterLevelSchema,
                                        list_water_levels_by_location)


@view_config(route_name='water_level.list',
             renderer='json',
             request_method='GET',
             permission='public')
def list(request):
    location_id = request.matchdict['location_id']
    return WaterLevelSchema(many=True).dump(list_water_levels_by_location(location_id))
