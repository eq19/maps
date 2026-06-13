import logging

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

        logger.warning(
            f"🔍 GET_ANALYZED_DATAFRAME "
            f"pair={pair} "
            f"timeframe={timeframe}"
        )

        try:

            cache = getattr(
                self,
                "_DataProvider__cached_pairs",
                {},
            )

            logger.warning(
                f"📦 CACHE SIZE = {len(cache)}"
            )

            pair_key = (
                pair,
                timeframe,
                self._config.get(
                    "candle_type_def",
                    None,
                ),
            )

            if pair_key in cache:

                df, ts = cache[pair_key]

                logger.warning(
                    f"✅ CACHE HIT "
                    f"pair={pair} "
                    f"timeframe={timeframe} "
                    f"rows={len(df)} "
                    f"last={ts}"
                )

            else:

                logger.error(
                    f"❌ CACHE MISS "
                    f"pair={pair} "
                    f"timeframe={timeframe}"
                )

                logger.error(
                    f"📦 AVAILABLE CACHE KEYS:"
                )

                for key in cache.keys():

                    try:
                        logger.error(
                            f"    {key}"
                        )
                    except Exception:
                        pass

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

                logger.warning(
                    f"📊 RESULT "
                    f"pair={pair} "
                    f"timeframe={timeframe} "
                    f"rows={len(df)}"
                )

                if len(df) == 0:

                    logger.error(
                        f"🚨 EMPTY DATAFRAME "
                        f"pair={pair} "
                        f"timeframe={timeframe}"
                    )

            except Exception as e:

                logger.exception(
                    f"💥 RESULT ANALYSIS FAILED: {e}"
                )

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
        "🛠️ DataProvider patch applied."
  )
