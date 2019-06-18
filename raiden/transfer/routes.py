from raiden.transfer.state import NODE_NETWORK_REACHABLE, RouteState
from raiden.utils.typing import ChannelID, List, NodeNetworkStateMap


def filter_reachable_routes(
    route_states: List[RouteState], nodeaddresses_to_networkstates: NodeNetworkStateMap
) -> List[RouteState]:
    """ This function makes sure we use reachable routes only. """

    return [
        route
        for route in route_states
        if nodeaddresses_to_networkstates.get(route.next_hop_address) == NODE_NETWORK_REACHABLE
    ]


def exclude_routes_from_channels(
    route_states: List[RouteState], channel_ids: List[ChannelID]
) -> List[RouteState]:
    """ Keeps only routes whose forward_channel is not in the given list. """

    return [route for route in route_states if route.forward_channel_id not in channel_ids]


def prune_route_table(
    route_states: List[RouteState], selected_route: RouteState
) -> List[RouteState]:
    """ Given a selected route, returns a filtered route table that
    contains only routes using the same forward channel and removes our own
    address in the process.
    """
    return [
        RouteState(route=rs.route[1:], forward_channel_id=selected_route.forward_channel_id)
        for rs in route_states
        if rs.forward_channel_id == selected_route.forward_channel_id
    ]
