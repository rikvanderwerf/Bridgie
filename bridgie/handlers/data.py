import requests
from pyramid.view import view_config
from sqlalchemy.orm.exc import NoResultFound
from bridgie.models import persist, rollback, commit
from marshmallow import ValidationError
from bridgie.models.location import (Location, LocationSchema,
                                     get_location_by_code)
from bridgie.models.water_level import (WaterLevel, WaterLevelSchema, get_water_level)



@view_config(route_name='data.get',
             renderer='json',
             request_method='GET',
             permission='public')
def get(request):
    """
    waarschijnlijk de lelijkste code ever
    """
    data = requests.get(request.registry.settings['rijkswaterstaat_url'])
    data = data.json()

    for feature in data['features']:
        try:
            result, errors = LocationSchema(strict=True).load(
                feature)
        except ValidationError as e:
            print(e)
            continue
        try:
            location = get_location_by_code(result['code'])
        except NoResultFound:
            location = Location()
        location.set_fields(result)
        location.latitude = feature['location']['lat']
        location.longitude = feature['location']['lon']
        persist(location)
        url = request.registry.settings['rijkswaterstaat_water_level_url']
        url = url + str(location.code)
        water_levels = requests.get(url).json()['H10']
        for water_level_ in water_levels:

            try:
                result, errors = WaterLevelSchema(strict=True).load(
                    water_level_)
            except ValidationError as e:
                print(e)
                continue
            try:
                water_level = get_water_level(location.id, water_level_['tijd'])
            except NoResultFound:
                water_level = WaterLevel()

            water_level.set_fields(result)
            water_level.location = location
        try:
            persist(water_level)
        except:
            rollback()
        finally:
            commit()

    return data
