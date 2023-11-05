from xrpl.clients import WebsocketClient
from xrpl.models import OfferCreate

url = "wss://s.altnet.rippletest.net:51233"

with WebsocketClient(url) as client:
    client.request(
        OfferCreate(
            account="rJ9rRe2cxkFrcN7Ug4EK8QenK3YCjuk9mN"
        )
    )