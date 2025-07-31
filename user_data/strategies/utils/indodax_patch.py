import time
import logging
from freqtrade.exchange import Exchange

logger = logging.getLogger(__name__)


def patch_indodax_create_order():
    """Monkey-patch Exchange.create_order() for Indodax with market-sell fallback and post-fetch refresh."""
    if hasattr(Exchange.create_order, '_is_patched'):
        return

    original_create_order = Exchange.create_order

    def patched_create_order(self, *args, **kwargs):
        args = list(args)

        pair = args[0] if len(args) > 0 else kwargs.get("symbol") or kwargs.get("pair")
        order_type = args[1] if len(args) > 1 else kwargs.get("type") or kwargs.get("order_type")
        side = args[2] if len(args) > 2 else kwargs.get("side")
        amount = args[3] if len(args) > 3 else kwargs.get("amount")

        logger.info(f"⏳ [Indodax Patch] Creating order for: {pair} (type={order_type}, side={side})")

        if side == 'sell' and (order_type is None or order_type == 'market'):
            try:
                orderbook = self._api.fetch_order_book(pair)
                best_bid = orderbook['bids'][0][0] if orderbook['bids'] else None

                if best_bid:
                    simulated_price = round(best_bid * 0.99, -2)  # nearest 100 IDR
                    total = simulated_price * amount if simulated_price and amount else 0

                    if total < 1000:
                        logger.warning(f"❌ [Indodax Patch] Sell amount too small: {amount} × {simulated_price} = {total} IDR")
                        raise ValueError("Cannot simulate market sell: amount × price < 1000 IDR")

                    logger.warning(f"⚠️ [Indodax Patch] Simulating market sell with limit price {simulated_price} IDR")

                    # Modify args or kwargs to become a limit sell
                    if len(args) > 1:
                        args[1] = 'limit'
                    else:
                        kwargs['order_type'] = 'limit'

                    if len(args) > 4:
                        args[4] = simulated_price
                    else:
                        kwargs['price'] = simulated_price
                else:
                    logger.warning(f"❌ [Indodax Patch] No bids to simulate market sell on {pair}")
            except Exception as e:
                logger.warning(f"⛔ [Indodax Patch] Error simulating market sell: {e}")

        # Place the (possibly patched) order
        order = original_create_order(self, *args, **kwargs)

        # Allow order to settle
        time.sleep(20)

        # Refresh order info with retry
        for attempt in range(3):
            try:
                refreshed_order = self.fetch_order(order['id'], pair)
                order.update(refreshed_order)
                logger.info(f"✅ [Indodax Patch] Order refreshed: {order['id']}")
                break
            except Exception as e:
                logger.warning(f"⛔ [Indodax Patch] Fetch attempt {attempt + 1} failed: {e}")
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
