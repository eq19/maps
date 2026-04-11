import ccxt
import logging

logger = logging.getLogger(__name__)


def _to_indodax_pair(symbol: str):
    base, quote = symbol.split("/")
    return f"{base.lower()}_{quote.lower()}"


def patch_ccxt_pair_only():
    exchange_class = ccxt.indodax

    if hasattr(exchange_class, "_pair_patched"):
        return

    # =========================
    # CREATE ORDER (SAFE)
    # =========================
    original_create = exchange_class.create_order

    def create_order_patched(self, *args, **kwargs):
        symbol = kwargs.get("symbol") or (args[0] if args else None)

        if symbol:
            pair = _to_indodax_pair(symbol)
            params = kwargs.get("params", {}) or {}
            params["pair"] = pair
            kwargs["params"] = params

            logger.warning(f"🔥 PAIR PATCH → {symbol} → {pair}")

        return original_create(self, *args, **kwargs)

    # =========================
    # FETCH ORDER (SAFE)
    # =========================
    original_fetch = exchange_class.fetch_order

    def fetch_order_patched(self, id, symbol=None, params=None):
        if params is None:
            params = {}

        if symbol:
            pair = _to_indodax_pair(symbol)
            params["pair"] = pair

        return original_fetch(self, id, symbol, params)

    # =========================
    # CANCEL ORDER (SAFE)
    # =========================
    original_cancel = exchange_class.cancel_order

    def cancel_order_patched(self, id, symbol=None, params=None):
        if params is None:
            params = {}

        if symbol:
            pair = _to_indodax_pair(symbol)
            params["pair"] = pair

        return original_cancel(self, id, symbol, params)

    # APPLY
    exchange_class.create_order = create_order_patched
    exchange_class.fetch_order = fetch_order_patched
    exchange_class.cancel_order = cancel_order_patched

    exchange_class._pair_patched = True

    logger.info("🛠️ CCXT PAIR PATCH APPLIED (SAFE)")
