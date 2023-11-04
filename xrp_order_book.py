from xrpl.clients import WebsocketClient
from xrpl.models import BookOffers
from xrpl.models.currencies.issued_currency import IssuedCurrency
from xrpl.models.currencies import XRP

url = "wss://s.altnet.rippletest.net:51233"

with WebsocketClient(url) as client:

    desired_currency = IssuedCurrency(
        currency="TST",
        issuer="rP9jPyP5kyvFRb6ZiRghAGw5u8SGAmU4bd"
        )
    owned_currency = XRP()

    # Look up Offers. -----------------------------------------------------------
    # To buy TST, look up Offers where "TakerGets" is TST:
    print("Requesting orderbook information...")
    orderbook_info = client.request(
        BookOffers(
            ledger_index="current",
            taker_gets=desired_currency, 
            taker_pays=owned_currency,
        )
    )
    
    print(f"Orderbook:\n{orderbook_info.result['offers']}")