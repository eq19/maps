import ccxt

def patch_ccxt_indodax_create_order():
    exchange_class = ccxt.indodax

    if hasattr(exchange_class.create_order, "_is_patched"):
        return

    original = exchange_class.create_order

    def patched(self, symbol, type, side, amount, price=None, params={}):
        logger.warning(f"🔥 [CCXT PATCH HIT] {symbol} {side} {type}")

        # --- Validate symbol ---
        if symbol not in self.markets:
            raise ValueError(f"[CCXT Patch] Invalid pair: {symbol}")

        # --- Simulate market order ---
        if type == "market":
            orderbook = self.fetch_order_book(symbol)

            bids = orderbook.get("bids", [])
            asks = orderbook.get("asks", [])

            if not bids or not asks:
                raise RuntimeError(f"No liquidity for {symbol}")

            best_bid = bids[0][0]
            best_ask = asks[0][0]
            spread = best_ask - best_bid

            if side == "sell":
                price = best_bid - (spread * 0.3)
            else:
                price = best_ask + (spread * 0.3)

            price = float(self.price_to_precision(symbol, price))
            type = "limit"

            logger.warning(f"⚙️ Simulated {side} market → limit @ {price}")

        return original(self, symbol, type, side, amount, price, params)

    exchange_class.create_order = patched
    exchange_class.create_order._is_patched = True

    logger.info("✅ CCXT Indodax create_order patched.")
  
