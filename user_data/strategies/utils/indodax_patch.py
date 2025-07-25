import time
import logging
from freqtrade.exchange import Exchange

logger = logging.getLogger(__name__)


def patch_indodax_fetch_order():
    """Monkey-patch Exchange.fetch_order() to fix amount/filled for Indodax."""
    if hasattr(Exchange.fetch_order, '_is_patched'):
        return

    original_fetch_order = Exchange.fetch_order

    def patched_fetch_order(self, order_id, symbol=None, params={}):
        logger.info(f"🔄 [Indodax Patch] Fetching order {order_id} for {symbol}")
        try:
            result = original_fetch_order(self, order_id, symbol, params)
            logger.debug(f"📦 [Indodax Patch] Raw fetch_order result: {result}")

            if getattr(self, 'id', '') == 'indodax':
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

def patch_indodax_cancel_order():
    """Monkey-patch Exchange.cancel_order() for Indodax."""
    if hasattr(Exchange.cancel_order, '_is_patched'):
        return

    original_cancel_order = Exchange.cancel_order

    def patched_cancel_order(self, order_id, symbol=None, params={}):
        #if getattr(self, 'id', '') != 'indodax':
            #return original_cancel_order(self, order_id, symbol, params)

        logger.info(f"⚠️ [Indodax Patch] Cancelling order: {order_id}")
        try:
            result = original_cancel_order(self, order_id, symbol, params)
            logger.info(f"✅ [Indodax Patch] Order {order_id} cancelled.")
            return result
        except Exception as e:
            logger.warning(f"⛔ [Indodax Patch] Failed to cancel order {order_id}: {e}")
            raise

    Exchange.cancel_order = patched_cancel_order
    Exchange.cancel_order._is_patched = True
    logger.info("🛠️ Indodax cancel_order() patched.")

def patch_indodax_fetch_order():
    """Monkey-patch Exchange.fetch_order() for logging on Indodax."""
    if hasattr(Exchange.fetch_order, '_is_patched'):
        return

    original_fetch_order = Exchange.fetch_order

    def patched_fetch_order(self, order_id, symbol=None, params={}):
        #if getattr(self, 'id', '') != 'indodax':
            #return original_fetch_order(self, order_id, symbol, params)

        logger.info(f"🔄 [Indodax Patch] Fetching order {order_id} for {symbol}")
        try:
            result = original_fetch_order(self, order_id, symbol, params)
            logger.debug(f"📦 [Indodax Patch] Raw fetch_order result: {result}")
            return result
        except Exception as e:
            logger.warning(f"⛔ [Indodax Patch] Error fetching order {order_id}: {e}")
            raise

    Exchange.fetch_order = patched_fetch_order
    Exchange.fetch_order._is_patched = True
    logger.info("🛠️ Indodax fetch_order() patched.")
