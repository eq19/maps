import logging
import traceback
from pandas import DataFrame

from freqtrade.data.dataprovider import DataProvider

logger = logging.getLogger(__name__)

# Keep original method
_original_get_pair_dataframe = DataProvider.get_pair_dataframe


def patched_get_pair_dataframe(
    self,
    pair: str,
    timeframe: str | None = None,
    candle_type: str = ""
):
    """
    Debug patch for:
        WARNING - No data found for (PAIR, TIMEFRAME,)

    Captures:
      - caller stack
      - runmode
      - returned dataframe size
    """

    try:
        result = _original_get_pair_dataframe(
            self,
            pair,
            timeframe,
            candle_type
        )

        rows = 0

        if result is not None:
            try:
                rows = len(result)
            except Exception:
                pass

        if rows == 0:

            logger.error("")
            logger.error("=" * 80)
            logger.error("🚨 NO DATA FOUND DETECTED")
            logger.error("=" * 80)
            logger.error("pair=%s", pair)
            logger.error("timeframe=%s", timeframe)
            logger.error("candle_type=%s", candle_type)

            try:
                logger.error("runmode=%s", self.runmode)
            except Exception:
                pass

            try:
                logger.error(
                    "whitelist_size=%s",
                    len(self._config.get("exchange", {}).get("pair_whitelist", []))
                )
            except Exception:
                pass

            logger.error("")
            logger.error("STACKTRACE:")
            logger.error(
                "%s",
                "".join(traceback.format_stack(limit=30))
            )

            logger.error("=" * 80)

        return result

    except Exception:
        logger.exception(
            "🚨 Exception inside patched_get_pair_dataframe "
            "pair=%s timeframe=%s",
            pair,
            timeframe
        )
        raise


def patch_dataprovider():
    """
    Install monkey patch
    """

    if getattr(DataProvider, "_pair_dataframe_debug_patch", False):
        return

    DataProvider.get_pair_dataframe = patched_get_pair_dataframe
    DataProvider._pair_dataframe_debug_patch = True

    logger.warning(
        "🛠️ DataProvider get_pair_dataframe STACKTRACE patch applied."
    )
