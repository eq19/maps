import logging
import traceback

logger = logging.getLogger(__name__)


def patch_dataprovider():

    try:
        from freqtrade.data.dataprovider import DataProvider
    except Exception as e:
        logger.error(
            f"❌ Failed importing DataProvider: {e}"
        )
        return

    if getattr(DataProvider, "_nodata_patch_applied", False):
        logger.info(
            "🛠️ DataProvider patch already applied."
        )
        return

    original_get_analyzed_dataframe = (
        DataProvider.get_analyzed_dataframe
    )

    def get_analyzed_dataframe_patched(
        self,
        pair,
        timeframe,
    ):

        try:

            cache = getattr(
                self,
                "_DataProvider__cached_pairs",
                {},
            )

            pair_key = (
                pair,
                timeframe,
                self._config.get(
                    "candle_type_def",
                    None,
                ),
            )

            cache_hit = pair_key in cache

            if not cache_hit:

                logger.error(
                    "\n"
                    "=====================================================\n"
                    f"❌ CACHE MISS\n"
                    f"pair      = {pair}\n"
                    f"timeframe = {timeframe}\n"
                    f"cache_size= {len(cache)}\n"
                    "====================================================="
                )

                logger.error(
                    "📦 FIRST 50 CACHE KEYS:"
                )

                for i, key in enumerate(cache.keys()):

                    if i >= 50:
                        logger.error(
                            "... truncated ..."
                        )
                        break

                    logger.error(f"    {key}")

                logger.error(
                    "\n📍 CALL STACK:\n%s",
                    "".join(
                        traceback.format_stack(limit=25)
                    )
                )

        except Exception as e:

            logger.exception(
                f"💥 CACHE INSPECTION FAILED: {e}"
            )

        try:

            result = original_get_analyzed_dataframe(
                self,
                pair,
                timeframe,
            )

            try:

                df = result[0]

                if len(df) == 0:

                    logger.error(
                        "\n"
                        "=====================================================\n"
                        f"🚨 EMPTY DATAFRAME\n"
                        f"pair      = {pair}\n"
                        f"timeframe = {timeframe}\n"
                        "====================================================="
                    )

            except Exception:

                pass

            return result

        except Exception as e:

            logger.exception(
                f"💥 GET_ANALYZED_DATAFRAME FAILED "
                f"pair={pair} "
                f"timeframe={timeframe} "
                f"error={e}"
            )

            raise

    DataProvider.get_analyzed_dataframe = (
        get_analyzed_dataframe_patched
    )

    DataProvider._nodata_patch_applied = True

    logger.warning(
        "🛠️ DataProvider STACKTRACE patch applied."
    )
