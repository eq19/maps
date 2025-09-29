import time
import logging
from decimal import Decimal, ROUND_DOWN
from freqtrade.exchange import Exchange

logger = logging.getLogger(__name__)


def patch_indodax_create_order():
    """Monkey-patch Freqtrade's Exchange.create_order for Indodax.
    - Enforces precision for BUY orders (rounding down or forcing int).
    - Simulates market SELLs with limit orders.
    - Refreshes order status after creation.
    """
    if hasattr(Exchange.create_order, '_is_patched'):
        return

    original_create_order = Exchange.create_order

    def patched_create_order(self, *args, **kwargs):
        pair = kwargs.get("pair", "unknown")
        ordertype = kwargs.get("ordertype") or kwargs.get("type")
        side = kwargs.get("side")
        amount = kwargs.get("amount")

        # 🔢 BUY amount precision handling
        if side == "buy" and amount is not None:
            try:
                market = self._api.market(pair)
                amount_precision = int(market.get("precision", {}).get("amount", 8))
                min_amount = float(market.get("limits", {}).get("amount", {}).get("min", 0) or 0)

                if amount_precision == 0:
                    # Integer-only pairs (PENGU, DOGE, SUN, etc.)
                    rounded_amount = int(amount)
                else:
                    quantize_str = "1." + "0" * amount_precision
                    rounded_amount = float(
                        Decimal(str(amount)).quantize(Decimal(quantize_str), rounding=ROUND_DOWN)
                    )
                    if min_amount == 0.0:
                        min_amount = 10 ** -amount_precision

                if rounded_amount < min_amount:
                    logger.warning(
                        f"❌ [Indodax Patch] Computed amount {rounded_amount} < min {min_amount} for {pair}. Skipping trade."
                    )
                    raise ValueError("Amount too small for exchange precision")

                kwargs["amount"] = rounded_amount
                logger.info(
                    f"🔢 [Indodax Patch] Rounded BUY {pair}: {amount} -> {rounded_amount} "
                    f"(precision={amount_precision}, min={min_amount})"
                )
            except Exception as e:
                logger.warning(f"⛔ [Indodax Patch] Error rounding BUY {pair}: {e}")

        # 📉 SELL market simulation
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

                    kwargs["ordertype"] = "limit"
                    kwargs["rate"] = simulated_price
                else:
                    logger.warning("❌ [Indodax Patch] No bids available to simulate market sell.")
            except Exception as e:
                logger.warning(f"⛔ [Indodax Patch] Error simulating market sell: {e}")

        # 🚀 Create the order
        order = original_create_order(self, *args, **kwargs)

        # ⏳ Let the exchange register the order, then refresh it
        time.sleep(20)
        for attempt in range(3):
            try:
                refreshed_order = self.fetch_order(order['id'], pair)
                order.update(refreshed_order)
                logger.info(f"✅ [Indodax Patch] Order refreshed: {order['id']} {pair} amount={order.get('amount')}")
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
