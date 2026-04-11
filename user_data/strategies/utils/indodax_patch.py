import time
import logging
from freqtrade.exchange import Exchange

logger = logging.getLogger(__name__)


# =========================
# FETCH ORDER (CRITICAL FIX)
# =========================
def patch_indodax_fetch_order():
    if hasattr(Exchange.fetch_order, '_is_patched'):
        return

    original_fetch_order = Exchange.fetch_order

    def patched_fetch_order(self, order_id, symbol=None, params=None):
        if params is None:
            params = {}

        max_retries = 5

        for attempt in range(max_retries):
            try:
                result = original_fetch_order(self, order_id, symbol, params)

                info = result.get("info", {})
                order_info = info.get("return", {}).get("order", {})

                # =========================
                # FIX amount / filled
                # =========================
                amount = result.get("amount")

                if not amount or amount == 0:
                    for key in order_info:
                        if key.startswith("receive_"):
                            try:
                                received = float(order_info[key])
                                if received > 0:
                                    result["amount"] = received
                                    result["filled"] = received
                                    logger.warning(
                                        f"🔧 FIXED amount via {key}: {received}"
                                    )
                                    break
                            except ValueError:
                                pass

                # =========================
                # FIX cost
                # =========================
                if result.get("cost") is None and "order_rp" in order_info:
                    try:
                        result["cost"] = float(order_info["order_rp"])
                    except ValueError:
                        pass

                # =========================
                # SUCCESS CONDITION
                # =========================
                if result.get("amount") and result["amount"] > 0:
                    return result

                # =========================
                # RETRY (Indodax delay)
                # =========================
                logger.warning(
                    f"⏳ Waiting order data ({attempt+1}/{max_retries}) → {order_id}"
                )
                time.sleep(2)

            except Exception as e:
                logger.warning(f"⛔ Fetch attempt {attempt+1} failed: {e}")
                time.sleep(2)

        logger.warning(f"⚠️ Returning incomplete order → {order_id}")
        return result

    Exchange.fetch_order = patched_fetch_order
    Exchange.fetch_order._is_patched = True

    logger.info("🛠️ Indodax fetch_order patched (SAFE).")


# =========================
# CANCEL ORDER (OPTIONAL)
# =========================
def patch_indodax_cancel_order():
    if hasattr(Exchange.cancel_order, '_is_patched'):
        return

    original_cancel_order = Exchange.cancel_order

    def patched_cancel_order(self, order_id, symbol=None, params=None):
        if params is None:
            params = {}

        try:
            if "side" not in params:
                try:
                    order = self.fetch_order(order_id, symbol)
                    side = order.get("side")

                    if side:
                        params = dict(params)
                        params["side"] = side
                    else:
                        logger.warning(f"❓ Cannot determine side for {order_id}")

                except Exception as e:
                    logger.warning(f"⚠️ Failed to fetch order for cancel: {e}")

            return original_cancel_order(self, order_id, symbol, params)

        except Exception as e:
            logger.warning(f"⛔ Cancel failed {order_id}: {e}")
            raise

    Exchange.cancel_order = patched_cancel_order
    Exchange.cancel_order._is_patched = True

    logger.info("🛠️ Indodax cancel_order patched.")
