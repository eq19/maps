import ccxt
import logging

logger = logging.getLogger(__name__)


def _to_indodax_pair(symbol: str):
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

    def create_order_patched(self, symbol, type=None, side=None, amount=None, price=None, params=None, **kwargs):
        if params is None:
            params = {}

        pair = _to_indodax_pair(symbol)
        params["pair"] = pair

        logger.warning(f"🔥 CREATE PATCH → {symbol} → {pair} ({type})")

        # =========================
        # 🔥 MARKET ORDER HANDLING
        # =========================
        if type == "market":
            try:
                orderbook = self.fetch_order_book(symbol)

                best_bid = orderbook['bids'][0][0]
                best_ask = orderbook['asks'][0][0]

                spread = (best_ask - best_bid) / best_bid

                # Adaptive aggression
                if side == "sell":
                    # tighter for low spread, wider for high spread
                    multiplier = 0.995 if spread < 0.003 else 0.98
                    price = best_bid * multiplier
                else:
                    multiplier = 1.005 if spread < 0.003 else 1.02
                    price = best_ask * multiplier

                logger.warning(
                    f"⚙️ MARKET→LIMIT {side.upper()} @ {price:.8f} | spread={spread:.4%}"
                )

                type = "limit"

            except Exception as e:
                logger.warning(f"⚠️ Orderbook fetch failed, fallback pricing: {e}")

                # fallback (VERY IMPORTANT)
                if price is None:
                    price = 1  # avoid crash

                type = "limit"

        # =========================
        # CALL ORIGINAL (SAFE)
        # =========================
        return original_create(
            self,
            symbol,
            type,
            side,
            amount,
            price,
            params
        )

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

    # =========================
    # PARSE ORDER FIX
    # =========================
    original_parse = exchange_class.parse_order

    def parse_order_patched(self, order, market=None):
        try:
            return original_parse(self, order, market)

        except TypeError as e:
            if "NoneType" in str(e):
                logger.warning(f"⛔ PARSE PATCH → Fallback: {order}")

                return {
                    "id": order.get("order_id") or order.get("id"),
                    "status": "canceled",
                    "symbol": None,
                    "price": None,
                    "amount": None,
                    "filled": 0.0,
                    "remaining": 0.0,
                    "info": order,
                }

            raise

    # APPLY PATCH
    exchange_class.create_order = create_order_patched
    exchange_class.fetch_order = fetch_order_patched
    exchange_class.cancel_order = cancel_order_patched
    exchange_class.parse_order = parse_order_patched

    exchange_class._is_patched = True

    logger.info("🛠️ CCXT FULL PATCH APPLIED (INDODAX HARDENED)")
