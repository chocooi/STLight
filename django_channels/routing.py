# routing.py
from channels.routing import route

channel_routing = [
    route('websocket.receive', 'stlsite.consumers.ws_echo'),
]
