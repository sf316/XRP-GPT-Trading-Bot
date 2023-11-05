from xrpl.clients import WebsocketClient
from xrpl.models import BookOffers
from xrpl.models.currencies.issued_currency import IssuedCurrency
from xrpl.models.currencies import XRP

url = "wss://s.altnet.rippletest.net:51233"

def parse_order(order):
    is_sell_offer = bool(order['Flags'] & 131072)
    offer_type = 'ask' if is_sell_offer else 'bid'
    
    # Extract currency and amount for TakerGets
    taker_gets = order['TakerGets']
    if isinstance(taker_gets, dict):
        taker_gets_currency = taker_gets['currency']
        taker_gets_amount = float(taker_gets['value'])
    else:
        taker_gets_currency = 'XRP'
        taker_gets_amount = float(taker_gets) / 10**6 
    
    # Extract currency and amount for TakerPays
    taker_pays = order['TakerPays']
    if isinstance(taker_pays, dict):
        taker_pays_currency = taker_pays['currency']
        taker_pays_amount = float(taker_pays['value'])
    else:
        taker_pays_currency = 'XRP'
        taker_pays_amount = float(taker_pays) / 10**6
    
    # Calculate price per unit
    if offer_type == 'ask':
        price_per_unit = taker_pays_amount / taker_gets_amount
    else:
        price_per_unit = taker_gets_amount / taker_pays_amount
    
    return {
        'type': offer_type,
        'taker_gets_currency': taker_gets_currency,
        'taker_gets_amount': taker_gets_amount,
        'taker_pays_currency': taker_pays_currency,
        'taker_pays_amount': taker_pays_amount,
        'price_per_unit': price_per_unit
    }

with WebsocketClient(url) as client:

    desired_currency = IssuedCurrency(
        currency="TST", # Focus on "TST"
        issuer="rP9jPyP5kyvFRb6ZiRghAGw5u8SGAmU4bd" # Must find a valid issuer who owns desired currency
        )
    owned_currency = XRP()

    # Look up Offers. -----------------------------------------------------------
    # To buy TST, look up Offers where "TakerGets" is TST:
    orderbook_info = client.request(
        BookOffers(
            taker_gets=desired_currency, 
            taker_pays=owned_currency,
        )
    )
    
    print(f"Orderbook:\n{orderbook_info.result['offers'][-1]}")

    for order in orderbook_info.result['offers']:
        print(parse_order(order))