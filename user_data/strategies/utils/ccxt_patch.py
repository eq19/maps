import ccxt
import logging

logger = logging.getLogger(__name__)

# --- 🔥 Global cache ---
_invalid_pairs_cache = set()


def patch_ccxt_create_order():
    exchange_class = ccxt.indodax

    if hasattr(exchange_class.create_order, "_is_patched"):
        return

    original = exchange_class.create_order

    def patched(self, symbol, type, side, amount, price=None, params={}):
        logger.warning(f"🔥 [CCXT PATCH HIT] {symbol} {side} {type}")

        # --- ✅ 1. Block cached invalid pairs ---
        if symbol in _invalid_pairs_cache:
            raise ValueError(f"[CCXT Patch] Cached invalid pair: {symbol}")

        # --- ✅ 2. Validate symbol exists in CCXT ---
        if symbol not in self.markets:
            raise ValueError(f"[CCXT Patch] Not in CCXT markets: {symbol}")

        market = self.markets[symbol]
        indodax_id = market.get("id")

        logger.info(f"[Indodax Debug] symbol={symbol} | id={indodax_id}")

        # --- ✅ 3. Simulate market order ---
        if type == "market":
            try:
                orderbook = self.fetch_order_book(symbol)

                bids = orderbook.get("bids", [])
                asks = orderbook.get("asks", [])

                if not bids or not asks:
                    raise RuntimeError(f"No liquidity for {symbol}")

                best_bid = bids[0][0]
                best_ask = asks[0][0]
                spread = best_ask - best_bid

                if side == "sell":
                    raw_price = best_bid - (spread * 0.3)
                elif side == "buy":
                    raw_price = best_ask + (spread * 0.3)
                else:
                    raise ValueError(f"Invalid side: {side}")

                price = float(self.price_to_precision(symbol, raw_price))
                type = "limit"

                logger.warning(
                    f"⚙️ Simulated {side.upper()} market → LIMIT @ {price} ({symbol})"
                )

                # --- Minimum trade check (IDR) ---
                total = price * amount
                if total < 1000:
                    raise ValueError(
                        f"[CCXT Patch] Trade too small: {amount} × {price} = {total}"
                    )

            except Exception as e:
                logger.error(f"[CCXT Patch] Market simulation failed: {e}")
                raise

        # --- ✅ 4. Execute order ---
        try:
            return original(self, symbol, type, side, amount, price, params)

        except Exception as e:
            error_msg = str(e)

            # --- 🔥 Detect Indodax invalid pair ---
            if "Invalid pair" in error_msg:
                _invalid_pairs_cache.add(symbol)

                logger.error(f"🚫 Marking pair as invalid: {symbol}")

                # Optional: deactivate pair in runtime
                if symbol in self.markets:
                    self.markets[symbol]["active"] = False

            raise

    exchange_class.create_order = patched
    exchange_class.create_order._is_patched = True

    logger.info("🛠️ CCXT create_order patched (production mode).")
