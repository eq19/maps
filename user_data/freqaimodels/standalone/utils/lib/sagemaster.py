from datetime import datetime
import time
import requests
import logging
import json
from lib import helpers

'''
SageMaster API Integration
'''

logger = logging.getLogger(__name__)

class SageMasterClient:

    #add constructor with configuration (api key, webhook url, trader name, etc)
    def __init__(self, api_key, webhook_url, trader_nickname):
        self.API_KEY = api_key
        self.WEBHOOK_URL = webhook_url
        self.TRADER_NICKNAME = trader_nickname

    def generate_message(self, trade_id, market, symbol_base, symbol_quote, deal_type, buy_price, tp_tip, sl_tip, current_time, trader_nickname="TAAMv1", status = "active", isClosed = False, current_profit = 0):
        MESSAGE_TEMPLATE = {
            "external_id": str(trade_id),
            "signal": {
                "_id": str(trade_id),
                "currencyPairShortName": market,
                "pips": str(current_profit),
                "currencyFrom": {
                    "symbolID": symbol_base,
                    "shortName": symbol_base
                },
                "currencyTo": {
                    "symbolID": symbol_quote,
                    "shortName": symbol_quote
                },
                "status": status,
                "orderType": "market",
                "signalType": "crypto",
                "exchange": "binance",
                "isClosed": isClosed,
                "market": market,
                "type": deal_type,
                "buyTip": {
                    "value": buy_price,
                },
                "stopTipPips": str(sl_tip),
                "targets": [],
                "takeProfits": [
                    {
                        "pips": "+" + str(tp_tip)
                    }
                ],
                "trader": {
                    "_id": helpers.get_uuid_from_key(trader_nickname),
                    "nickname": trader_nickname
                }
            },
            "created_at": current_time,
            "updated_at": current_time
        }
        return json.dumps(MESSAGE_TEMPLATE)


    def open_deal(self, market="BTCUSDT", symbol_base="BTC", symbol_quote="USDT", deal_type = "buy", buy_price=25000, tp_tip=1, sl_tip=0.5, trade_id=""):
        start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        status = "active"

        body = self.generate_message(
            trade_id,
            market,
            symbol_base,
            symbol_quote,
            deal_type,
            buy_price,
            tp_tip,
            sl_tip,
            current_time,
            trader_nickname=self.TRADER_NICKNAME,
            status=status,
            isClosed=False
        )

        # print all parameters
        logger.info(f"ENTER open_deal() = status: {status} market: {market}, symbol_base: {symbol_base}, symbol_quote: {symbol_quote}, deal_type: {deal_type}, buy_price: {buy_price}, tp_tip: {tp_tip}, sl_tip: {sl_tip}, current_time: {current_time} body: {body}")

        # Create a POST request with the webhook URL and message text
        response = requests.post(self.WEBHOOK_URL,
                    data=body.encode("utf-8"),
                    headers={
                        "Content-Type": "application/json",
                        "x-api-key": self.API_KEY
                    })

        # print response
        logger.info(f"EXIT open_deal() status_code: {response.status_code}, headers: {response.headers}, content: {response.content} execution time: {time.time() - start_time:.2f} seconds")


    def close_deal(self, market="BTCUSDT", symbol_base="BTC", symbol_quote="USDT", buy_price=25000, deal_type = "buy", tp_tip=1, sl_tip=0.5, trade_id="", profit_ratio = 0, allow_stoploss = False):
        start_time = time.time()
        current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        # determine status
        if profit_ratio > 0.001:
            status = "won"
        elif profit_ratio < -0.002 and allow_stoploss:
            status = "stop_loss"
        else:
            status = "draw"
            profit_ratio = 0

        body = self.generate_message(
            trade_id,
            market,
            symbol_base,
            symbol_quote,
            deal_type,
            buy_price,
            tp_tip,
            sl_tip,
            current_time,
            trader_nickname=self.TRADER_NICKNAME,
            status=status,
            isClosed=True,
            current_profit=profit_ratio * 100
        )

        # print all parameters
        logger.info(f"ENTER close_deal() = status: {status} market: {market}, symbol_base: {symbol_base}, symbol_quote: {symbol_quote}, deal_type: {deal_type}, buy_price: {buy_price}, tp_tip: {tp_tip}, sl_tip: {sl_tip}, current_time: {current_time} body: {body}")

        # Create a POST request with the webhook URL and message text
        response = requests.post(self.WEBHOOK_URL,
                    data=body.encode("utf-8"),
                    headers={
                        "Content-Type": "application/json",
                        "x-api-key": self.API_KEY
                    })
        # print response
        logger.info(f"EXIT close_deal() status_code: {response.status_code}, headers: {response.headers}, content: {response.content} execution time: {time.time() - start_time:.2f} seconds")