from xrpl.clients import WebsocketClient
from xrpl.models import BookOffers, Tx
from xrpl.models.currencies.issued_currency import IssuedCurrency
from xrpl.models.currencies import XRP
from xrpl.utils import get_order_book_changes
from xrpl.ledger import get_fee
from wallet import import_user_wallet
from parse import parse_order, process_offer_changes

# Testnet address
url = "wss://s.altnet.rippletest.net:51233"

with WebsocketClient(url) as client:
    # Import user's profile
    user_profile = import_user_wallet(client)
    user = user_profile['account_data']['Account']
    balance = user_profile['account_data']['Balance']

    # Market info
    current_fee = get_fee(client)

    desired_currency = IssuedCurrency(
        currency="TST",
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

    orders, tx_history = [], []

    for order in orderbook_info.result['offers']:
        # Sort order books info
        orders.append(parse_order(order))

        # Sort previous transactions info
        tx_id = order['PreviousTxnID']
        prev_tx_info = client.request(
            Tx(
                transaction=tx_id,
            )
        )

        if 'error' not in prev_tx_info.result.keys():
            prev_tx = get_order_book_changes(prev_tx_info.result['meta'])
            
            if len(prev_tx) > 0:
                tx_history.append(process_offer_changes(prev_tx[0]['offer_changes']))
            else:
                tx_history.append({ 
                    'avg_exchange_rate': 0.0,
                    'avg_status': 0.0,
                })
        else:
            tx_history.append({ 
                    'avg_exchange_rate': 0.0,
                    'avg_status': -1.0,
                })
            
    print(current_fee)
    print(tx_history)
    print(orders)