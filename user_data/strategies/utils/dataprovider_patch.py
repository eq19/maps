import logging
import traceback
from pandas import DataFrame

from freqtrade.data.dataprovider import DataProvider

logger = logging.getLogger(__name__)

# Keep original method
_original_get_pair_dataframe = DataProvider.get_pair_dataframe

# Prevent log spam
_ALREADY_REPORTED = set()


def patched_get_pair_dataframe(
    self,
    pair: str,
    timeframe: str | None = None,
    candle_type: str = ""
):
    """
    Debug patch for DataProvider.get_pair_dataframe()

    Captures:
      - missing pair
      - runmode
      - whitelist
      - exchange info
      - caller stack
      - dataframe metadata
    """

    try:
        result = _original_get_pair_dataframe(
            self,
            pair,
            timeframe,
            candle_type
        )

        rows = 0

        try:
            if result is not None:
                rows = len(result)
        except Exception:
            pass

        if rows == 0:

            key = (pair, timeframe, candle_type)

            # report once only
            if key not in _ALREADY_REPORTED:

                _ALREADY_REPORTED.add(key)

                logger.error("")
                logger.error("=" * 120)
                logger.error("🚨 NO DATA FOUND DETECTED")
                logger.error("=" * 120)

                logger.error("pair=%s", pair)
                logger.error("timeframe=%s", timeframe)
                logger.error("candle_type=%s", candle_type)

                # runmode
                try:
                    logger.error("runmode=%s", self.runmode)
                except Exception:
                    logger.exception("runmode lookup failed")

                # whitelist
                try:
                    whitelist = self.current_whitelist()

                    logger.error(
                        "whitelist_size=%s",
                        len(whitelist)
                    )

                    logger.error(
                        "pair_in_whitelist=%s",
                        pair in whitelist
                    )

                    logger.error(
                        "whitelist_sample=%s",
                        whitelist[:20]
                    )

                except Exception:
                    logger.exception("whitelist lookup failed")

                # exchange
                try:
                    logger.error(
                        "exchange=%s",
                        getattr(self._exchange, "name", None)
                    )
                except Exception:
                    pass

                # dataframe metadata
                try:
                    logger.error(
                        "result_type=%s",
                        type(result)
                    )

                    if isinstance(result, DataFrame):
                        logger.error(
                            "df_shape=%s",
                            result.shape
                        )
                        logger.error(
                            "df_columns=%s",
                            list(result.columns)
                        )
                except Exception:
                    logger.exception("dataframe inspection failed")

                # caller frames only
                try:
                    logger.error("")
                    logger.error("CALLER FRAMES:")

                    stack = traceback.extract_stack()

                    # remove patch frames
                    filtered = []

                    for frame in stack:
                        filename = frame.filename

                        if "dataprovider_patch.py" in filename:
                            continue

                        filtered.append(frame)

                    for frame in filtered[-25:]:

                        logger.error(
                            "%s:%s :: %s",
                            frame.filename,
                            frame.lineno,
                            frame.name
                        )

                        if frame.line:
                            logger.error(
                                "    %s",
                                frame.line.strip()
                            )

                except Exception:
                    logger.exception("stack inspection failed")

                # full raw stack
                try:
                    logger.error("")
                    logger.error("FULL STACK:")
                    logger.error(
                        "".join(traceback.format_stack())
                    )
                except Exception:
                    logger.exception("full stack failed")

                logger.error("=" * 120)
                logger.error("")

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
        "🛠️ DataProvider get_pair_dataframe DEBUG patch applied."
    )
