import requests
from pyramid.view import view_config
from sqlalchemy.orm.exc import NoResultFound
from bridgie.models import persist, rollback, commit
from pyramid.httpexceptions import HTTPBadRequest
from marshmallow import ValidationError
from bridgie.models.location import (Location, LocationSchema,
                                     get_location_by_code)


@view_config(route_name='data.get',
             renderer='json',
             request_method='GET',
             permission='public')
def get(request):
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
            print(result)
            location = get_location_by_code(result['code'])
        except NoResultFound:
            location = Location()
        location.set_fields(result)
        location.latitude = feature['location']['lat']
        location.longitude = feature['location']['lon']
        try:
            persist(location)
        except:
            rollback()
        finally:
            commit()

    return data
