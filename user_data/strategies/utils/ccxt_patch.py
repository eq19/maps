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
    # CREATE ORDER (PAIR + MARKET FIX)
    # =========================
    original_create = exchange_class.create_order

    def create_order_patched(self, *args, **kwargs):
        args = list(args)

        # Correct extraction
        symbol = kwargs.get("symbol") or (args[0] if len(args) > 0 else None)
        type_  = kwargs.get("type")  or (args[1] if len(args) > 1 else None)
        side   = kwargs.get("side")  or (args[2] if len(args) > 2 else None)

        if symbol:
            pair = _to_indodax_pair(symbol)

            # Ensure params exists
            if len(args) >= 6:
                params = args[5] or {}
                args[5] = params
            else:
                params = kwargs.get("params", {}) or {}
                kwargs["params"] = params

            params["pair"] = pair

            logger.debug(f"PAIR PATCH → {symbol} → {pair}")

            # =========================
            # 🔥 MARKET → SAFE LIMIT
            # =========================
            if type_ == "market":
                try:
                    orderbook = self.fetch_order_book(symbol)

                    bid = orderbook["bids"][0][0] if orderbook["bids"] else None
                    ask = orderbook["asks"][0][0] if orderbook["asks"] else None

                    if bid is None or ask is None:
                        raise Exception("Empty orderbook")

                    if side == "sell":
                        price = bid * 0.995
                    else:
                        price = ask * 1.005

                    price = float(self.price_to_precision(symbol, price))

                    logger.warning(
                        f"⚡ MARKET→LIMIT {side.upper()} {symbol} @ {price}"
                    )

                    # ✅ FIX TYPE POSITION
                    if len(args) > 1:
                        args[1] = "limit"
                    else:
                        kwargs["type"] = "limit"

                    # ✅ FIX PRICE POSITION (CRITICAL)
                    if len(args) > 4:
                        args[4] = price
                    else:
                        kwargs["price"] = price

                except Exception as e:
                    logger.error(f"❌ Market conversion failed: {e}")

                    fallback_price = 1
                    try:
                        fallback_price = float(
                            self.price_to_precision(symbol, fallback_price)
                        )
                    except Exception:
                        pass

                    logger.warning(f"⚠️ Fallback LIMIT @ {fallback_price}")

                    if len(args) > 1:
                        args[1] = "limit"
                    else:
                        kwargs["type"] = "limit"

                    if len(args) > 4:
                        args[4] = fallback_price
                    else:
                        kwargs["price"] = fallback_price

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
    # PARSE ORDER FIX
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

    logger.info("🛠️ CCXT Indodax patch applied.")
