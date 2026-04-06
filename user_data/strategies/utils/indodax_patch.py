import time
import logging
from freqtrade.exchange import Exchange

logger = logging.getLogger(__name__)


def patch_indodax_create_order():
    """Production-grade patch for Indodax order handling."""

    if hasattr(Exchange.create_order, '_is_patched'):
        return

    original_create_order = Exchange.create_order

    def patched_create_order(self, *args, **kwargs):
        pair = kwargs.get("pair")
        side = kwargs.get("side")
        ordertype = kwargs.get("ordertype") or kwargs.get("type")
        amount = kwargs.get("amount")

        # --- ✅ 1. Validate pair ---
        if pair not in self._api.markets:
            raise ValueError(f"[Indodax Patch] Invalid pair: {pair}")

        # --- ✅ 2. Normalize order type ---
        is_market = ordertype in (None, "market")

        if is_market:
            try:
                orderbook = self._api.fetch_order_book(pair)

                bids = orderbook.get("bids", [])
                asks = orderbook.get("asks", [])

                if not bids or not asks:
                    raise RuntimeError(f"No liquidity for {pair}")

                best_bid = bids[0][0]
                best_ask = asks[0][0]
                spread = best_ask - best_bid

                # --- ✅ 3. Adaptive slippage ---
                if side == "sell":
                    raw_price = best_bid - (spread * 0.3)
                elif side == "buy":
                    raw_price = best_ask + (spread * 0.3)
                else:
                    raise ValueError(f"Invalid side: {side}")

                # --- ✅ 4. Precision-safe price ---
                price = self._api.price_to_precision(pair, raw_price)
                price = float(price)

                total = price * amount

                # --- ✅ 5. Minimum trade check ---
                if total < 1000:
                    raise ValueError(
                        f"[Indodax Patch] Trade too small: {amount} × {price} = {total} IDR"
                    )

                # --- ✅ 6. Convert to limit order ---
                kwargs["ordertype"] = "limit"
                kwargs["rate"] = price

                logger.info(
                    f"[Indodax Patch] Simulated {side.upper()} market -> LIMIT @ {price} ({pair})"
                )

            except Exception as e:
                logger.error(f"[Indodax Patch] Failed to simulate market order: {e}")
                raise  # 🔥 Fail hard (important)

        # --- ✅ 7. Place order ---
        order = original_create_order(self, *args, **kwargs)

        # --- ✅ 8. Non-blocking refresh loop ---
        for attempt in range(5):
            try:
                refreshed = self.fetch_order(order["id"], pair)
                if refreshed:
                    order.update(refreshed)

                    # Exit early if filled or closed
                    if refreshed.get("status") in ("closed", "filled"):
                        break

                time.sleep(1.5 * (attempt + 1))  # small backoff

            except Exception as e:
                logger.warning(f"[Indodax Patch] Refresh attempt {attempt+1} failed: {e}")

        return order

    Exchange.create_order = patched_create_order
    Exchange.create_order._is_patched = True
    logger.info("✅ Indodax production patch applied.")

def patch_indodax_cancel_order():
    """Monkey-patch Exchange.cancel_order() for Indodax."""
    if hasattr(Exchange.cancel_order, '_is_patched'):
        return

    original_cancel_order = Exchange.cancel_order

    def patched_cancel_order(self, order_id, symbol=None, params={}):
        #if getattr(self, 'id', '') != 'indodax':
            #return original_cancel_order(self, order_id, symbol, params)

        #logger.info(f"⚠️ [Indodax Patch] Cancelling order: {order_id}")
        try:
            # 🔍 Indodax requires 'side' param when cancelling an order
            if "side" not in params:
                try:
                    order = self.fetch_order(order_id, symbol)
                    side = order.get("side")
                    if side:
                        params = dict(params)  # clone to avoid mutating input
                        params["side"] = side
                        #logger.debug(f"📎 [Indodax Patch] Injected side='{side}' into cancel_order params.")
                    else:
                        logger.warning(f"❓ [Indodax Patch] Could not determine order side for {order_id}")
                except Exception as fetch_err:
                    logger.warning(f"🧾 [Indodax Patch] Failed to fetch order {order_id} to get side: {fetch_err}")
                    raise

            result = original_cancel_order(self, order_id, symbol, params)
            #logger.info(f"✅ [Indodax Patch] Order {order_id} cancelled.")
            return result

        except Exception as e:
            logger.warning(f"⛔ [Indodax Patch] Failed to cancel order {order_id}: {e}")
            raise

    Exchange.cancel_order = patched_cancel_order
    Exchange.cancel_order._is_patched = True
    logger.info("🛠️ Indodax cancel_order() patched.")

def patch_indodax_fetch_order():
    """Monkey-patch Exchange.fetch_order() to fix amount/filled for Indodax."""
    if hasattr(Exchange.fetch_order, '_is_patched'):
        return

    original_fetch_order = Exchange.fetch_order

    def patched_fetch_order(self, order_id, symbol=None, params={}):
        #if getattr(self, 'id', '') != 'indodax':
            #return original_fetch_order(self, order_id, symbol, params)

        #logger.info(f"🔄 [Indodax Patch] Fetching order {order_id} for {symbol}")
        try:
            result = original_fetch_order(self, order_id, symbol, params)
            #logger.debug(f"📦 [Indodax Patch] Raw fetch_order result: {result}")
            info = result.get("info", {})
            order_info = info.get("return", {}).get("order", {})

            # Handle amount from receive_eth / receive_btc / receive_... if amount is None
            if result.get("amount") is None:
                for key in order_info:
                    if key.startswith("receive_"):
                        try:
                            received = float(order_info[key])
                            result["amount"] = received
                            result["filled"] = received  # fully filled
                            break
                        except ValueError:
                            logger.warning(f"🔍 [Indodax Patch] Failed to parse {key}: {order_info[key]}")

            # Handle cost from order_rp
            if result.get("cost") is None and "order_rp" in order_info:
                try:
                    result["cost"] = float(order_info["order_rp"])
                except ValueError:
                    logger.warning(f"🔍 [Indodax Patch] Failed to parse order_rp: {order_info['order_rp']}")

            # Handle fee if available
            if result.get("fee") is None and "fee" in order_info:
                try:
                    fee_cost = float(order_info["fee"]) / 100  # assuming fee is in IDR cents
                    result["fee"] = {
                        "cost": fee_cost,
                        "currency": "IDR"
                    }
                except ValueError:
                    logger.warning(f"🔍 [Indodax Patch] Failed to parse fee: {order_info['fee']}")

            return result

        except Exception as e:
            logger.warning(f"⛔ [Indodax Patch] Error fetching order {order_id}: {e}")
            raise

    Exchange.fetch_order = patched_fetch_order
    Exchange.fetch_order._is_patched = True
    logger.info("🛠️ Indodax fetch_order() patched.")
