import ccxt
import time
import logging

logger = logging.getLogger(__name__)

# --- Debug flags ---
DEBUG_MODE = True

# --- Global caches (keep minimal for now) ---
_invalid_pairs_cache = set()
BLACKLISTED_PAIRS = set()

_spread_blocked_pairs = {}
_temp_blocked_pairs = _spread_blocked_pairs


def patch_ccxt_create_order():
    exchange_class = ccxt.indodax

    if hasattr(exchange_class.create_order, "_is_patched"):
        return

    original = exchange_class.create_order

    def patched(self, symbol, type, side, amount, price=None, params=None):
        if params is None:
            params = {}

        now = time.time()

        # --- 🔍 1. Print CCXT version once ---
        if DEBUG_MODE and not hasattr(self, "_debug_ccxt_printed"):
            logger.error(f"🧪 CCXT VERSION: {ccxt.__version__}")
            self._debug_ccxt_printed = True

        logger.warning(f"🔥 [PATCH HIT] {symbol} {side} {type}")

        # --- 🔍 2. Market mapping debug ---
        if symbol not in self.markets:
            logger.error(f"❌ Symbol not in markets: {symbol}")
            raise ccxt.ExchangeError(f"Symbol not found: {symbol}")

        market = self.markets[symbol]
        pair_id = market.get("id")
        base = market.get("base")
        quote = market.get("quote")

        logger.error(
            f"🧪 MARKET DEBUG → symbol={symbol} | id={pair_id} | base={base} | quote={quote}"
        )

        # --- 🔍 3. Show ALL possible pair formats ---
        try:
            base_raw, quote_raw = symbol.split("/")
        except Exception:
            base_raw, quote_raw = base, quote

        normalized_pair = f"{base_raw.lower()}_{quote_raw.lower()}"
        alt_pair = f"{base_raw.lower()}{quote_raw.lower()}"

        logger.error(
            f"🧪 PAIR FORMATS → ccxt_id={pair_id} | normalized={normalized_pair} | alt={alt_pair}"
        )

        # --- 🔍 4. Orderbook check ---
        try:
            orderbook = self.fetch_order_book(symbol)
            best_bid = orderbook["bids"][0][0] if orderbook["bids"] else None
            best_ask = orderbook["asks"][0][0] if orderbook["asks"] else None

            logger.error(
                f"🧪 ORDERBOOK → bid={best_bid} | ask={best_ask}"
            )
        except Exception as e:
            logger.error(f"❌ ORDERBOOK ERROR: {e}")

        # --- 🔍 5. Final params BEFORE sending ---
        logger.error(
            f"🧪 BEFORE ORDER → symbol={symbol} | type={type} | side={side} | amount={amount} | price={price} | params={params}"
        )

        # --- 🚀 6. Execute order ---
        try:
            result = original(self, symbol, type, side, amount, price, params)

            logger.error(f"✅ ORDER SUCCESS: {result}")
            return result

        except Exception as e:
            logger.error(f"🔥 RAW ERROR: {e}")

            # --- 🔍 7. Try manual pair injection test ---
            try:
                logger.error("🧪 RETRY WITH MANUAL PAIR FORMAT...")

                test_params = params.copy()
                test_params["pair"] = normalized_pair

                logger.error(f"🧪 RETRY PARAMS: {test_params}")

                result = original(self, symbol, type, side, amount, price, test_params)

                logger.error(f"✅ RETRY SUCCESS: {result}")
                return result

            except Exception as e2:
                logger.error(f"❌ RETRY FAILED: {e2}")

            raise

    exchange_class.create_order = patched
    exchange_class.create_order._is_patched = True
    logger.info("🧪 CCXT create_order patched (DEBUG MODE).")
