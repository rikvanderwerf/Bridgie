from pyramid.view import view_config
from bridgie.models.bridge import (get_bridge_by_id, list_bridges, BridgeSchema)


@view_config(route_name='bridge.get',
             renderer='json',
             request_method='GET',
             permission='public')
def get(request):
    bridge_id = request.matchdict['bridge_id']
    bridge = get_bridge_by_id(bridge_id)
    return BridgeSchema().dump(bridge)


@view_config(route_name='bridge.list',
             renderer='json',
             request_method='GET',
             permission='public')
def list(request):
    return BridgeSchema(many=True).dump(list_bridges())