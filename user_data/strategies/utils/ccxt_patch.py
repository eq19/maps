import ccxt
import time
import logging

logger = logging.getLogger(__name__)

# --- 🔥 Global caches ---
_invalid_pairs_cache = set()
BLACKLISTED_PAIRS = set()  # ✅ Used by fibbo.py

# --- 🔥 Compatibility layer ---
_spread_blocked_pairs = {}  # ✅ Used by fibbo.py
_temp_blocked_pairs = _spread_blocked_pairs  # ✅ SAME object (no duplication)

# --- 🔥 Config ---
BLOCK_TTL = 300  # 5 minutes
SPREAD_LIMIT = 0.02  # 2%


def patch_ccxt_create_order():
    exchange_class = ccxt.indodax

    if hasattr(exchange_class.create_order, "_is_patched"):
        return

    original = exchange_class.create_order

    def patched(self, symbol, type, side, amount, price=None, params=None):
        if params is None:
            params = {}

        now = time.time()

        logger.warning(f"🔥 [CCXT PATCH HIT] {symbol} {side} {type}")

        # --- ✅ 1. Permanent invalid pairs ---
        if symbol in _invalid_pairs_cache:
            logger.warning(f"⛔ Permanently blocked pair: {symbol}")
            raise ccxt.ExchangeError(f"[PATCH] Invalid pair (cached): {symbol}")

        # --- ✅ 2. Temporary block (anti-spam) ---
        if symbol in _temp_blocked_pairs:
            blocked_time = _temp_blocked_pairs[symbol]

            if now - blocked_time < BLOCK_TTL:
                logger.warning(f"🔁 Temporarily blocked: {symbol}")
                raise ccxt.ExchangeError(f"[PATCH] Temporarily blocked: {symbol}")
            else:
                logger.info(f"♻️ Unblocking pair: {symbol}")
                del _temp_blocked_pairs[symbol]

        # --- ✅ 3. Validate market ---
        if symbol not in self.markets:
            raise ccxt.ExchangeError(f"[PATCH] Not in markets: {symbol}")

        market = self.markets[symbol]
        pair_id = market.get("id")

        logger.info(f"[MARKET] {symbol} → id={pair_id}")

        # --- 🚫 Skip inactive markets ---
        if not market.get("active", True):
            logger.warning(f"🚫 Inactive market: {symbol}")
            raise ccxt.ExchangeError(f"[PATCH] Inactive market: {symbol}")

        # --- 🚫 Validate pair format ---
        if not pair_id or not pair_id.endswith("idr"):
            logger.warning(f"🚫 Invalid market id: {symbol} → {pair_id}")
            raise ccxt.ExchangeError(f"[PATCH] Invalid market id: {symbol}")

        # --- ✅ 4. Fetch orderbook ---
        try:
            orderbook = self.fetch_order_book(symbol)
            bids = orderbook.get("bids", [])
            asks = orderbook.get("asks", [])
        except Exception as e:
            logger.error(f"❌ Orderbook error: {e}")
            raise ccxt.ExchangeError(f"[PATCH] Orderbook failed: {e}")

        if not bids or not asks:
            raise ccxt.ExchangeError(f"[PATCH] No liquidity: {symbol}")

        best_bid = bids[0][0]
        best_ask = asks[0][0]
        spread = best_ask - best_bid
        spread_ratio = spread / best_bid

        # --- 🚫 Spread guard ---
        if spread_ratio > SPREAD_LIMIT:
            logger.warning(f"🚫 Spread too large: {symbol} ({spread_ratio:.2%})")
            _temp_blocked_pairs[symbol] = now
            raise ccxt.ExchangeError(f"[PATCH] Spread too large: {symbol}")

        # --- ✅ 5. Simulate market order ---
        if type == "market":
            try:
                if side == "buy":
                    raw_price = best_ask + (spread * 0.3)
                elif side == "sell":
                    raw_price = best_bid - (spread * 0.3)
                else:
                    raise ccxt.ExchangeError(f"[PATCH] Invalid side: {side}")

                price = float(self.price_to_precision(symbol, raw_price))
                type = "limit"

                logger.warning(
                    f"⚙️ Simulated {side.upper()} MARKET → LIMIT @ {price} ({symbol})"
                )

                total = price * amount
                if total < 1000:
                    raise ccxt.InvalidOrder(
                        f"[PATCH] Trade too small: {amount} × {price} = {total}"
                    )

            except ccxt.BaseError:
                raise
            except Exception as e:
                logger.error(f"❌ Market simulation error: {e}")
                raise ccxt.ExchangeError(str(e))

        # --- ✅ 6. Execute order ---
        try:
            return original(self, symbol, type, side, amount, price, params)

        except Exception as e:
            error_msg = str(e)
            error_msg_lower = error_msg.lower()

            logger.error(f"🔥 RAW API ERROR for {symbol}: {error_msg}")

            # --- 💰 Insufficient funds ---
            if "insufficient" in error_msg_lower:
                raise ccxt.InsufficientFunds(error_msg)

            # --- 📉 Invalid order ---
            elif any(x in error_msg_lower for x in ["minimum", "too small", "price"]):
                raise ccxt.InvalidOrder(error_msg)

            # --- ❌ REAL invalid pair ---
            elif "symbol not found" in error_msg_lower:
                logger.error(f"⛔ Confirmed invalid pair: {symbol}")
                _invalid_pairs_cache.add(symbol)
                BLACKLISTED_PAIRS.add(symbol)
                raise ccxt.ExchangeError(f"[PATCH] Invalid pair: {symbol}")

            # --- ⚠️ Indodax API reject ---
            elif "invalid pair" in error_msg_lower:
                logger.warning(f"⚠️ API rejected pair (blocked): {symbol}")
                _temp_blocked_pairs[symbol] = now
                raise ccxt.ExchangeError(
                    f"[PATCH] API rejected pair (blocked): {symbol}"
                )

            # --- ❓ Unknown error ---
            else:
                logger.error(f"❓ Unknown error: {error_msg}")
                _temp_blocked_pairs[symbol] = now
                raise

    exchange_class.create_order = patched
    exchange_class.create_order._is_patched = True

    logger.info("🛠️ CCXT create_order patched (FINAL + FULL COMPAT MODE).")
