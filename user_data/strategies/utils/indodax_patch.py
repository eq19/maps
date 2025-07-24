import logging
from freqtrade.exchange.exchange import Exchange

logger = logging.getLogger(__name__)


def patch_indodax_create_order():
    orig_create_order = Exchange.create_order

    def custom_create_order(self, pair, order_type, side, amount, price, *args, **kwargs):
        result = orig_create_order(self, pair, order_type, side, amount, price, *args, **kwargs)

        if self.exchange.name.lower() == "indodax":
            result["filled"] = 0.0
            result["remaining"] = amount
            result["status"] = "open"
            logger.debug("🛠️ Patch: create_order - Added default filled/remaining for Indodax.")

        return result

    Exchange.create_order = custom_create_order
    logger.info("🔧 Patched Exchange.create_order for Indodax.")


def patch_indodax_cancel_order():
    orig_cancel_order = Exchange.cancel_order

    def custom_cancel_order(self, order_id, pair, *args, **kwargs):
        result = orig_cancel_order(self, order_id, pair, *args, **kwargs)

        if self.exchange.name.lower() == "indodax":
            result["status"] = "canceled"
            logger.debug(f"🛠️ Patch: cancel_order - Marked {order_id} as canceled.")

        return result

    Exchange.cancel_order = custom_cancel_order
    logger.info("🔧 Patched Exchange.cancel_order for Indodax.")


def patch_indodax_fetch_order():
    orig_fetch_order = Exchange.fetch_order

    def custom_fetch_order(self, order_id, pair, *args, **kwargs):
        result = orig_fetch_order(self, order_id, pair, *args, **kwargs)

        if self.exchange.name.lower() == "indodax":
            logger.debug(f"📦 Patch: fetch_order - Original result: {result}")

            # Apply patch only if filled = 0 and order is closed
            if result.get("filled", 0) == 0 and result.get("status") == "closed":
                amount = result.get("amount", 0)
                result["filled"] = amount
                result["remaining"] = 0.0
                logger.debug(f"✅ Patch: Corrected filled={amount} and remaining=0.0")

        return result

    Exchange.fetch_order = custom_fetch_order
    logger.info("🔧 Patched Exchange.fetch_order for Indodax.")
