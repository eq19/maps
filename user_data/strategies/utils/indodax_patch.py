import time
import logging
from freqtrade.exchange import Exchange

logger = logging.getLogger(__name__)


# =========================
# FETCH ORDER FIX
# =========================
def patch_indodax_fetch_order():
    if hasattr(Exchange.fetch_order, "_is_patched"):
        return

    original_fetch = Exchange.fetch_order

    def patched_fetch(self, order_id, symbol=None, params=None):
        params = params or {}

        result = original_fetch(self, order_id, symbol, params)

        info = result.get("info", {})
        order_info = info.get("return", {}).get("order", {})

        # Fix missing amount
        if result.get("amount") is None:
            for key in order_info:
                if key.startswith("receive_"):
                    try:
                        received = float(order_info[key])
                        result["amount"] = received
                        result["filled"] = received
                        break
                    except Exception:
                        pass

        # fallback safety
        if result.get("amount") is None:
            result["amount"] = 0.0
        if result.get("filled") is None:
            result["filled"] = 0.0

        # Fix cost
        if result.get("cost") is None and "order_rp" in order_info:
            try:
                result["cost"] = float(order_info["order_rp"])
            except Exception:
                pass

        return result

    Exchange.fetch_order = patched_fetch
    Exchange.fetch_order._is_patched = True

    logger.info("✅ Fetch order patched (amount fix)")


# =========================
# CANCEL ORDER FIX
# =========================
def patch_indodax_cancel_order():
    if hasattr(Exchange.cancel_order, "_is_patched"):
        return

    original_cancel = Exchange.cancel_order

    def patched_cancel(self, order_id, symbol=None, params=None):
        params = params or {}

        try:
            if "side" not in params:
                try:
                    order = self.fetch_order(order_id, symbol)
                    side = order.get("side")

                    if side:
                        params["side"] = side
                except Exception:
                    pass

            return original_cancel(self, order_id, symbol, params)

        except Exception as e:
            logger.warning(f"⛔ Cancel failed {order_id}: {e}")
            raise

    Exchange.cancel_order = patched_cancel
    Exchange.cancel_order._is_patched = True

    logger.info("✅ Cancel order patched (side fix)")


# =========================
# OPTIONAL DELAY PATCH
# =========================
def patch_indodax_create_order():
    if hasattr(Exchange.create_order, "_is_patched"):
        return

    original_create = Exchange.create_order

    def patched_create(self, *args, **kwargs):
        order = original_create(self, *args, **kwargs)

        # wait for indodax to populate data
        for i in range(5):
            time.sleep(2)

            try:
                refreshed = self.fetch_order(order["id"], kwargs.get("pair"))
                if refreshed.get("amount"):
                    order.update(refreshed)
                    return order

                logger.warning(f"⏳ Waiting order data ({i+1}/5) → {order['id']}")

            except Exception:
                pass

        logger.warning(f"⚠️ Returning incomplete order → {order['id']}")
        return order

    Exchange.create_order = patched_create
    Exchange.create_order._is_patched = True

    logger.info("✅ Create order patched (delay fix)")
