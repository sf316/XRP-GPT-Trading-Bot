from xrpl.clients import WebsocketClient
from xrpl.models import OfferCreate

url = "wss://s.altnet.rippletest.net:51233"

with WebsocketClient(url) as client:
    offer = client.request(
        OfferCreate(
            account= '' #wallet address
        )
    )