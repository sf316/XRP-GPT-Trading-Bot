from xrpl.clients import WebsocketClient

url = "wss://s.altnet.rippletest.net:51233"

with WebsocketClient(url) as client: