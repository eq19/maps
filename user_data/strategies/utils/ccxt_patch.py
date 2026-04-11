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

    original_create = exchange_class.create_order

    def create_order_patched(self, *args, **kwargs):
        args = list(args)

        # =========================
        # Extract symbol safely
        # =========================
        symbol = kwargs.get("symbol")
        if not symbol and len(args) > 0:
            symbol = args[0]

        if symbol:
            pair = _to_indodax_pair(symbol)

            # =========================
            # CASE 1: params in args
            # =========================
            if len(args) >= 6:
                params = args[5] or {}
                params["pair"] = pair
                args[5] = params

            # =========================
            # CASE 2: params in kwargs
            # =========================
            else:
                params = kwargs.get("params", {}) or {}
                params["pair"] = pair
                kwargs["params"] = params

            logger.warning(f"🔥 PAIR PATCH → {symbol} → {pair}")

        return original_create(self, *args, **kwargs)

    # =========================
    # FETCH ORDER
    # =========================
    original_fetch = exchange_class.fetch_order

    def fetch_order_patched(self, id, symbol=None, params=None):
        if params is None:
            params = {}

        if symbol:
            params["pair"] = _to_indodax_pair(symbol)

        return original_fetch(self, id, symbol, params)

    # =========================
    # CANCEL ORDER
    # =========================
    original_cancel = exchange_class.cancel_order

    def cancel_order_patched(self, id, symbol=None, params=None):
        if params is None:
            params = {}

        if symbol:
            params["pair"] = _to_indodax_pair(symbol)

        return original_cancel(self, id, symbol, params)

    # APPLY
    exchange_class.create_order = create_order_patched
    exchange_class.fetch_order = fetch_order_patched
    exchange_class.cancel_order = cancel_order_patched

    exchange_class._pair_patched = True

    logger.info("🛠️ CCXT PAIR PATCH APPLIED (FIXED PARAMS)")
