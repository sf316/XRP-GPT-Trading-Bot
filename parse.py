from xrpl.clients import WebsocketClient
from xrpl.models import BookOffers, Tx
from xrpl.models.currencies.issued_currency import IssuedCurrency
from xrpl.models.currencies import XRP
from xrpl.utils import get_order_book_changes
from xrpl.ledger import get_fee
from wallet import import_user_wallet

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

def process_offer_changes(offer_changes):
    total_exchange_rate, status_counts = 0, 0

    for offer in offer_changes:        
        total_exchange_rate += float(offer['maker_exchange_rate'])
        
        status = offer['status']
        if status == "filled":
            status_counts += 1
        elif status == "partially-filled":
            status_counts += 0.5

    average_exchange_rate = (total_exchange_rate / len(offer_changes))
    status_counts /= len(offer_changes)
    
    return { 
        'avg_exchange_rate': average_exchange_rate,
        'avg_status': status_counts,
        } 

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