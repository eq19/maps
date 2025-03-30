# integrations from other modules
from app import app
from app.apihandlers import gdaxHandler
from app import dbmanager

#python imports
import gdax
import datetime
import json
import time
import sys

#building ETH-USD Realtime orderbook
# wsClient = gdaxHandler.myWebsocketClient()
# wsClient.start()
# print(wsClient.url, wsClient.products)
# while (wsClient.message_count < 50):
#     print ("\nmessage_count =", "{} \n".format(wsClient.message_count))
#     time.sleep(1)
# wsClient.close()


#starting orderbook
order_book = gdaxHandler.OrderBookConsole()
order_book.start()
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    order_book.close()

if order_book.error:
    sys.exit(1)
else:
    sys.exit(0)