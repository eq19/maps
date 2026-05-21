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

        # Diagnostic extraction
        amount = kwargs.get("amount") or (args[3] if len(args) > 3 else None)
        price_ = kwargs.get("price")  or (args[4] if len(args) > 4 else None)

        logger.warning(
            f"🧪 CREATE_ORDER RAW "
            f"symbol={symbol} "
            f"type={type_} "
            f"side={side} "
            f"amount={amount} ({type(amount).__name__}) "
            f"price={price_}"
        )

        if symbol:
            pair = _to_indodax_pair(symbol)

            # =========================
            # MARKET METADATA DEBUG
            # =========================
            try:
                market = self.market(symbol)

                logger.warning(
                    f"📏 MARKET PRECISION "
                    f"{symbol} "
                    f"amount_precision={market.get('precision', {}).get('amount')} "
                    f"price_precision={market.get('precision', {}).get('price')} "
                    f"limits={market.get('limits')}"
                )

            except Exception as e:
                logger.warning(
                    f"⚠️ Failed reading market metadata "
                    f"{symbol}: {e}"
                )

            # =========================
            # AMOUNT ANALYSIS DEBUG
            # =========================
            if amount is not None:
                try:
                    is_decimal = float(amount) != int(float(amount))

                    logger.warning(
                        f"🔍 AMOUNT ANALYSIS "
                        f"{symbol} "
                        f"amount={amount} "
                        f"decimal={is_decimal}"
                    )

                except Exception as e:
                    logger.warning(
                        f"⚠️ Amount analysis failed: {e}"
                    )

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

                    logger.warning(
                        f"📘 ORDERBOOK "
                        f"{symbol} "
                        f"bid={bid} "
                        f"ask={ask}"
                    )

                    if bid is None or ask is None:
                        raise Exception("Empty orderbook")

                    if side == "sell":
                        price = bid * 0.995
                    else:
                        price = ask * 1.005

                    logger.warning(
                        f"🧮 RAW LIMIT PRICE "
                        f"{symbol} "
                        f"calculated_price={price}"
                    )

                    price = float(
                        self.price_to_precision(symbol, price)
                    )

                    logger.warning(
                        f"⚡ MARKET→LIMIT "
                        f"{side.upper()} "
                        f"{symbol} "
                        f"@ {price}"
                    )

                    # ✅ FIX TYPE POSITION
                    if len(args) > 1:
                        args[1] = "limit"
                    else:
                        kwargs["type"] = "limit"

                    # ✅ FIX PRICE POSITION
                    if len(args) > 4:
                        args[4] = price
                    else:
                        kwargs["price"] = price

                except Exception as e:
                    logger.error(
                        f"❌ Market conversion failed: {e}"
                    )

                    fallback_price = 1

                    try:
                        fallback_price = float(
                            self.price_to_precision(
                                symbol,
                                fallback_price
                            )
                        )

                    except Exception as e2:
                        logger.warning(
                            f"⚠️ Fallback precision failed: {e2}"
                        )

                    logger.warning(
                        f"⚠️ Fallback LIMIT "
                        f"{symbol} "
                        f"@ {fallback_price}"
                    )

                    if len(args) > 1:
                        args[1] = "limit"
                    else:
                        kwargs["type"] = "limit"

                    if len(args) > 4:
                        args[4] = fallback_price
                    else:
                        kwargs["price"] = fallback_price

        # =========================
        # FINAL REQUEST DEBUG
        # =========================
        final_amount = (
            kwargs.get("amount")
            or (args[3] if len(args) > 3 else None)
        )

        final_price = (
            kwargs.get("price")
            or (args[4] if len(args) > 4 else None)
        )

        final_type = (
            kwargs.get("type")
            or (args[1] if len(args) > 1 else None)
        )

        logger.warning(
            f"🚀 FINAL CREATE_ORDER "
            f"symbol={symbol} "
            f"type={final_type} "
            f"side={side} "
            f"amount={final_amount} "
            f"price={final_price}"
        )

        # =========================
        # EXECUTION DEBUG
        # =========================
        try:
            return original_create(self, *args, **kwargs)

        except Exception as e:

            logger.error(
                f"💥 CREATE_ORDER FAILED "
                f"symbol={symbol} "
                f"type={type_} "
                f"side={side} "
                f"amount={amount} "
                f"price={price_} "
                f"error={e}"
            )

            # =========================
            # 🔥 INTEGER AMOUNT FALLBACK
            # =========================
            error_msg = str(e).lower()

            if (
                amount is not None
                and "amount can't be in decimal" in error_msg
            ):

                try:
                    fallback_amount = float(int(float(amount)))

                    logger.warning(
                        f"🔁 INTEGER FALLBACK "
                        f"{symbol} "
                        f"{amount} → {fallback_amount}"
                    )

                    # update args/kwargs
                    if len(args) > 3:
                        args[3] = fallback_amount
                    else:
                        kwargs["amount"] = fallback_amount

                    logger.warning(
                        f"🚀 RETRY CREATE_ORDER "
                        f"symbol={symbol} "
                        f"type={type_} "
                        f"side={side} "
                        f"amount={fallback_amount}"
                    )

                    return original_create(self, *args, **kwargs)

                except Exception as retry_error:

                    logger.error(
                        f"💥 RETRY FAILED "
                        f"symbol={symbol} "
                        f"fallback_amount={fallback_amount} "
                        f"error={retry_error}"
                    )

                    raise retry_error

            raise

    # =========================
    # FETCH ORDER
    # =========================
    original_fetch = exchange_class.fetch_order

    def fetch_order_patched(self, id, symbol=None, params=None):
        params = params or {}

        if symbol:
            params["pair"] = _to_indodax_pair(symbol)

            logger.debug(
                f"📥 FETCH ORDER "
                f"id={id} "
                f"symbol={symbol} "
                f"pair={params['pair']}"
            )

        return original_fetch(self, id, symbol, params)

    # =========================
    # CANCEL ORDER
    # =========================
    original_cancel = exchange_class.cancel_order

    def cancel_order_patched(self, id, symbol=None, params=None):
        params = params or {}

        if symbol:
            params["pair"] = _to_indodax_pair(symbol)

            logger.debug(
                f"🛑 CANCEL ORDER "
                f"id={id} "
                f"symbol={symbol} "
                f"pair={params['pair']}"
            )

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

                logger.warning(
                    f"⛔ PARSE FIX "
                    f"market={market} "
                    f"order={order}"
                )

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
