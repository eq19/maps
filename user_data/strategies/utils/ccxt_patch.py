import ccxt
import logging

logger = logging.getLogger(__name__)


def _to_indodax_pair(symbol: str):
    """
    Convert CCXT symbol → Indodax format
    ADA/IDR → ada_idr
    """
    base, quote = symbol.split("/")
    return f"{base.lower()}_{quote.lower()}"


def patch_ccxt_all():
    exchange_class = ccxt.indodax

    if hasattr(exchange_class, "_is_patched"):
        return

    # =========================
    # CREATE ORDER
    # =========================
    original_create = exchange_class.create_order

    def create_order_patched(self, symbol, type, side, amount, price=None, params=None):
        if params is None:
            params = {}

        pair = _to_indodax_pair(symbol)

        logger.warning(f"🔥 CREATE PATCH → {symbol} → {pair}")

        params["pair"] = pair

        return original_create(self, symbol, type, side, amount, price, params)

    # =========================
    # FETCH ORDER
    # =========================
    original_fetch = exchange_class.fetch_order

    def fetch_order_patched(self, id, symbol=None, params=None):
        if params is None:
            params = {}

        if symbol:
            pair = _to_indodax_pair(symbol)
            params["pair"] = pair
            logger.warning(f"🔥 FETCH PATCH → {symbol} → {pair}")

        return original_fetch(self, id, symbol, params)

    # =========================
    # CANCEL ORDER
    # =========================
    original_cancel = exchange_class.cancel_order

    def cancel_order_patched(self, id, symbol=None, params=None):
        if params is None:
            params = {}

        if symbol:
            pair = _to_indodax_pair(symbol)
            params["pair"] = pair
            logger.warning(f"🔥 CANCEL PATCH → {symbol} → {pair}")

        return original_cancel(self, id, symbol, params)

    # APPLY PATCH
    exchange_class.create_order = create_order_patched
    exchange_class.fetch_order = fetch_order_patched
    exchange_class.cancel_order = cancel_order_patched

    exchange_class._is_patched = True

    logger.info("🛠️ CCXT FULL PATCH APPLIED (PAIR FORMAT FIX)")
