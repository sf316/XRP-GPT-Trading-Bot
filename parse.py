def parse_order(order):
    is_sell_offer = bool(order['Flags'] & 131072)
    offer_type = 'ask' if is_sell_offer else 'bid'
    
    taker_gets = order['TakerGets']
    if isinstance(taker_gets, dict):
        taker_gets_currency = taker_gets['currency']
        taker_gets_amount = float(taker_gets['value'])
    else:
        taker_gets_currency = 'XRP'
        taker_gets_amount = float(taker_gets) / 10**6 

    taker_pays = order['TakerPays']
    if isinstance(taker_pays, dict):
        taker_pays_currency = taker_pays['currency']
        taker_pays_amount = float(taker_pays['value'])
    else:
        taker_pays_currency = 'XRP'
        taker_pays_amount = float(taker_pays) / 10**6
    
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