from xrpl.clients import WebsocketClient
from xrpl.utils import get_order_book_changes

url = "wss://s.altnet.rippletest.net:51233"

with WebsocketClient(url) as client:
    get_order_book_changes
