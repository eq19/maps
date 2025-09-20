import time
import logging
from freqtrade.exchange import Exchange

logger = logging.getLogger(__name__)


def patch_indodax_create_order():
    """Monkey-patch Freqtrade's Exchange.create_order for Indodax to simulate market sell."""
    if hasattr(Exchange.create_order, '_is_patched'):
        return

    original_create_order = Exchange.create_order

    def patched_create_order(self, *args, **kwargs):
        pair = kwargs.get("pair", "unknown")
        ordertype = kwargs.get("ordertype") or kwargs.get("type")
        side = kwargs.get("side")
        amount = kwargs.get("amount")

        #logger.info(f"⏳ [Indodax Patch] Creating order for: {pair} (type={ordertype}, side={side})")

        # 🔥 Force rounding for pairs like PENG/IDR (no decimals allowed)
        if side == 'buy' and amount is not None:
            kwargs["amount"] = int(amount)  # round down to integer
            logger.info(f"🔢 [Indodax Patch] Rounded amount for {pair}: {amount} -> {kwargs['amount']}")

        if side == 'sell' and (ordertype is None or ordertype == 'market'):
            try:
                orderbook = self._api.fetch_order_book(pair)
                best_bid = orderbook['bids'][0][0] if orderbook['bids'] else None

                if best_bid:
                    simulated_price = round(best_bid * 0.99, -2)
                    total = simulated_price * amount

                    if total < 1000:
                        logger.warning(f"❌ [Indodax Patch] Sell amount too small: {amount} × {simulated_price} = {total} IDR")
                        raise ValueError("Simulated sell order below 1000 IDR")

                    #logger.warning(f"⚠️ [Indodax Patch] Simulating market sell with limit price {simulated_price} IDR")

                    kwargs["ordertype"] = "limit"
                    kwargs["rate"] = simulated_price
                else:
                    logger.warning("❌ [Indodax Patch] No bids available to simulate market sell.")
            except Exception as e:
                logger.warning(f"⛔ [Indodax Patch] Error simulating market sell: {e}")

        order = original_create_order(self, *args, **kwargs)

        time.sleep(20)  # Let the exchange register the order

        for attempt in range(3):
            try:
                refreshed_order = self.fetch_order(order['id'], pair)
                order.update(refreshed_order)
                #logger.info(f"✅ [Indodax Patch] Order refreshed: {order['id']}")
                break
            except Exception as e:
                logger.warning(f"⛔ [Indodax Patch] Fetch attempt {attempt+1} failed: {e}")
                time.sleep(2 ** attempt)

        return order

    Exchange.create_order = patched_create_order
    Exchange.create_order._is_patched = True
    logger.info("🛠️ Indodax create_order() patched.")

def patch_indodax_cancel_order():
    """Monkey-patch Exchange.cancel_order() for Indodax."""
    if hasattr(Exchange.cancel_order, '_is_patched'):
        return

    original_cancel_order = Exchange.cancel_order

    def patched_cancel_order(self, order_id, symbol=None, params={}):
        #if getattr(self, 'id', '') != 'indodax':
            #return original_cancel_order(self, order_id, symbol, params)

        #logger.info(f"⚠️ [Indodax Patch] Cancelling order: {order_id}")
        try:
            # 🔍 Indodax requires 'side' param when cancelling an order
            if "side" not in params:
                try:
                    order = self.fetch_order(order_id, symbol)
                    side = order.get("side")
                    if side:
                        params = dict(params)  # clone to avoid mutating input
                        params["side"] = side
                        #logger.debug(f"📎 [Indodax Patch] Injected side='{side}' into cancel_order params.")
                    else:
                        logger.warning(f"❓ [Indodax Patch] Could not determine order side for {order_id}")
                except Exception as fetch_err:
                    logger.warning(f"🧾 [Indodax Patch] Failed to fetch order {order_id} to get side: {fetch_err}")
                    raise

            result = original_cancel_order(self, order_id, symbol, params)
            #logger.info(f"✅ [Indodax Patch] Order {order_id} cancelled.")
            return result

        except Exception as e:
            logger.warning(f"⛔ [Indodax Patch] Failed to cancel order {order_id}: {e}")
            raise

    Exchange.cancel_order = patched_cancel_order
    Exchange.cancel_order._is_patched = True
    logger.info("🛠️ Indodax cancel_order() patched.")

def patch_indodax_fetch_order():
    """Monkey-patch Exchange.fetch_order() to fix amount/filled for Indodax."""
    if hasattr(Exchange.fetch_order, '_is_patched'):
        return

    original_fetch_order = Exchange.fetch_order

    def patched_fetch_order(self, order_id, symbol=None, params={}):
        #if getattr(self, 'id', '') != 'indodax':
            #return original_fetch_order(self, order_id, symbol, params)

        #logger.info(f"🔄 [Indodax Patch] Fetching order {order_id} for {symbol}")
        try:
            result = original_fetch_order(self, order_id, symbol, params)
            #logger.debug(f"📦 [Indodax Patch] Raw fetch_order result: {result}")
            info = result.get("info", {})
            order_info = info.get("return", {}).get("order", {})

            # Handle amount from receive_eth / receive_btc / receive_... if amount is None
            if result.get("amount") is None:
                for key in order_info:
                    if key.startswith("receive_"):
                        try:
                            received = float(order_info[key])
                            result["amount"] = received
                            result["filled"] = received  # fully filled
                            break
                        except ValueError:
                            logger.warning(f"🔍 [Indodax Patch] Failed to parse {key}: {order_info[key]}")

            # Handle cost from order_rp
            if result.get("cost") is None and "order_rp" in order_info:
                try:
                    result["cost"] = float(order_info["order_rp"])
                except ValueError:
                    logger.warning(f"🔍 [Indodax Patch] Failed to parse order_rp: {order_info['order_rp']}")

            # Handle fee if available
            if result.get("fee") is None and "fee" in order_info:
                try:
                    fee_cost = float(order_info["fee"]) / 100  # assuming fee is in IDR cents
                    result["fee"] = {
                        "cost": fee_cost,
                        "currency": "IDR"
                    }
                except ValueError:
                    logger.warning(f"🔍 [Indodax Patch] Failed to parse fee: {order_info['fee']}")

            return result

        except Exception as e:
            logger.warning(f"⛔ [Indodax Patch] Error fetching order {order_id}: {e}")
            raise

    Exchange.fetch_order = patched_fetch_order
    Exchange.fetch_order._is_patched = True
    logger.info("🛠️ Indodax fetch_order() patched.")
