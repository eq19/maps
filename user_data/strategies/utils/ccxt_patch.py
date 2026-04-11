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
    # CREATE ORDER (PAIR FIX ONLY)
    # =========================
    original_create = exchange_class.create_order

    def create_order_patched(self, *args, **kwargs):
        args = list(args)

        symbol = kwargs.get("symbol")
        if not symbol and len(args) > 0:
            symbol = args[0]

        if symbol:
            pair = _to_indodax_pair(symbol)

            # CASE 1: params in args
            if len(args) >= 6:
                params = args[5] or {}
                params["pair"] = pair
                args[5] = params
            else:
                params = kwargs.get("params", {}) or {}
                params["pair"] = pair
                kwargs["params"] = params

            logger.debug(f"PAIR PATCH → {symbol} → {pair}")

        return original_create(self, *args, **kwargs)

    # =========================
    # FETCH ORDER
    # =========================
    original_fetch = exchange_class.fetch_order

    def fetch_order_patched(self, id, symbol=None, params=None):
        params = params or {}

        if symbol:
            params["pair"] = _to_indodax_pair(symbol)

        return original_fetch(self, id, symbol, params)

    # =========================
    # CANCEL ORDER
    # =========================
    original_cancel = exchange_class.cancel_order

    def cancel_order_patched(self, id, symbol=None, params=None):
        params = params or {}

        if symbol:
            params["pair"] = _to_indodax_pair(symbol)

        return original_cancel(self, id, symbol, params)

    # =========================
    # PARSE ORDER FIX (CRITICAL)
    # =========================
    original_parse = exchange_class.parse_order

    def parse_order_patched(self, order, market=None):
        try:
            return original_parse(self, order, market)

        except TypeError as e:
            if "NoneType" in str(e):
                logger.warning(f"⛔ PARSE FIX → fallback order: {order}")

                return {
                    "id": order.get("order_id") or order.get("id"),
                    "status": "canceled",
                    "symbol": market["symbol"] if market else None,
                    "price": None,
                    "amount": 0.0,
                    "filled": 0.0,
                    "remaining": 0.0,
                    "info": order,
                }

            raise

    # APPLY PATCHES
    exchange_class.create_order = create_order_patched
    exchange_class.fetch_order = fetch_order_patched
    exchange_class.cancel_order = cancel_order_patched
    exchange_class.parse_order = parse_order_patched

    exchange_class._pair_patched = True

    logger.info("✅ CCXT Indodax patch applied (PAIR + PARSE FIX)")
