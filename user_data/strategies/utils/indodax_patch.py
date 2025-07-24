import time
import logging
from ccxt.base.exchange import Exchange

logger = logging.getLogger(__name__)


def patch_indodax_create_order():
    """Monkey-patch Exchange.create_order() for Indodax with delay and post-fill fetch."""
    if hasattr(Exchange.create_order, '_is_patched'):
        return

    original_create_order = Exchange.create_order

    def patched_create_order(self, *args, **kwargs):
        if getattr(self, 'id', '') != 'indodax':
            return original_create_order(self, *args, **kwargs)

        pair = args[0] if args else kwargs.get("pair", "unknown")
        logger.info(f"⏳ [Indodax Patch] Creating order for: {pair}")

        order = original_create_order(self, *args, **kwargs)

        # 💤 Delay to let the order settle in Indodax
        time.sleep(30)

        # 🔁 Retry fetch_order up to 3 times with exponential backoff
        for attempt in range(3):
            try:
                refreshed_order = self.fetch_order(order['id'], pair)
                order.update(refreshed_order)
                logger.info(f"✅ [Indodax Patch] Order refreshed: {order['id']}")
                break
            except Exception as e:
                logger.warning(f"⚠️ [Indodax Patch] Fetch attempt {attempt+1} failed: {e}")
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
        if getattr(self, 'id', '') != 'indodax':
            return original_cancel_order(self, order_id, symbol, params)

        logger.info(f"⛔ [Indodax Patch] Cancelling order: {order_id}")
        try:
            result = original_cancel_order(self, order_id, symbol, params)
            logger.info(f"✅ [Indodax Patch] Order {order_id} cancelled.")
            return result
        except Exception as e:
            logger.warning(f"⚠️ [Indodax Patch] Failed to cancel order {order_id}: {e}")
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
        if getattr(self, 'id', '') != 'indodax':
            return original_fetch_order(self, order_id, symbol, params)

        logger.info(f"🔄 [Indodax Patch] Fetching order {order_id} for {symbol}")
        try:
            result = original_fetch_order(self, order_id, symbol, params)
            logger.debug(f"📦 [Indodax Patch] Raw fetch_order result: {result}")
            return result
        except Exception as e:
            logger.warning(f"⚠️ [Indodax Patch] Error fetching order {order_id}: {e}")
            raise

    Exchange.fetch_order = patched_fetch_order
    Exchange.fetch_order._is_patched = True
    logger.info("🛠️ Indodax fetch_order() patched.")
