
from typing import Dict, List
from freqtrade.exchange.exchange import timeframe_to_minutes
from freqtrade.optimize.hyperopt_interface import IHyperOpt
from pandas import DataFrame
from freqtrade.optimize.space import Categorical, Dimension, Integer, SKDecimal, Real  # noqa
import logging
import math
from abc import ABC
from typing import Any, Callable, Dict, List

from skopt.space import Categorical, Dimension, Integer

from freqtrade.exceptions import OperationalException
from freqtrade.exchange import timeframe_to_minutes
from freqtrade.misc import round_dict
from freqtrade.optimize.space import SKDecimal
from freqtrade.strategy import IStrategy

logger = logging.getLogger(__name__)


class HyperoptMcDuck(IHyperOpt):


    
    def roi_space(self) -> List[Dimension]:
        """
        Create a ROI space.

        Defines values to search for each ROI steps.

        This method implements adaptive roi hyperspace with varied
        ranges for parameters which automatically adapts to the
        timeframe used.

        It's used by Freqtrade by default, if no custom roi_space method is defined.
        """

        # Default scaling coefficients for the roi hyperspace. Can be changed
        # to adjust resulting ranges of the ROI tables.
        # Increase if you need wider ranges in the roi hyperspace, decrease if shorter
        # ranges are needed.
        roi_t_alpha = 1.0
        roi_p_alpha = 1.0
        timeframe_min = timeframe_to_minutes(self.strategy.timeframe_main)

        # We define here limits for the ROI space parameters automagically adapted to the
        # timeframe used by the bot:
        #
        # * 'roi_t' (limits for the time intervals in the ROI tables) components
        #   are scaled linearly.
        # * 'roi_p' (limits for the ROI value steps) components are scaled logarithmically.
        #
        # The scaling is designed so that it maps exactly to the legacy Freqtrade roi_space()
        # method for the 5m timeframe.
        roi_t_scale = timeframe_min / 5
        roi_p_scale = math.log1p(timeframe_min) / math.log1p(5)
        roi_limits = {
            'roi_t1_min': int(10 * roi_t_scale * roi_t_alpha),
            'roi_t1_max': int(120 * roi_t_scale * roi_t_alpha),
            'roi_t2_min': int(10 * roi_t_scale * roi_t_alpha),
            'roi_t2_max': int(60 * roi_t_scale * roi_t_alpha),
            'roi_t3_min': int(10 * roi_t_scale * roi_t_alpha),
            'roi_t3_max': int(40 * roi_t_scale * roi_t_alpha),
            'roi_p1_min': 0.01 * roi_p_scale * roi_p_alpha,
            'roi_p1_max': 0.04 * roi_p_scale * roi_p_alpha,
            'roi_p2_min': 0.01 * roi_p_scale * roi_p_alpha,
            'roi_p2_max': 0.07 * roi_p_scale * roi_p_alpha,
            'roi_p3_min': 0.01 * roi_p_scale * roi_p_alpha,
            'roi_p3_max': 0.20 * roi_p_scale * roi_p_alpha,
        }
        #logger.debug(f"Using roi space limits: {roi_limits}")
        p = {
            'roi_t1': roi_limits['roi_t1_min'],
            'roi_t2': roi_limits['roi_t2_min'],
            'roi_t3': roi_limits['roi_t3_min'],
            'roi_p1': roi_limits['roi_p1_min'],
            'roi_p2': roi_limits['roi_p2_min'],
            'roi_p3': roi_limits['roi_p3_min'],
        }
        #logger.info(f"Min roi table: {round_dict(self.generate_roi_table(p), 3)}")
        p = {
            'roi_t1': roi_limits['roi_t1_max'],
            'roi_t2': roi_limits['roi_t2_max'],
            'roi_t3': roi_limits['roi_t3_max'],
            'roi_p1': roi_limits['roi_p1_max'],
            'roi_p2': roi_limits['roi_p2_max'],
            'roi_p3': roi_limits['roi_p3_max'],
        }
        #logger.info(f"Max roi table: {round_dict(self.generate_roi_table(p), 3)}")

        return [
            Integer(roi_limits['roi_t1_min'], roi_limits['roi_t1_max'], name='roi_t1'),
            Integer(roi_limits['roi_t2_min'], roi_limits['roi_t2_max'], name='roi_t2'),
            Integer(roi_limits['roi_t3_min'], roi_limits['roi_t3_max'], name='roi_t3'),
            SKDecimal(roi_limits['roi_p1_min'], roi_limits['roi_p1_max'], decimals=3,
                      name='roi_p1'),
            SKDecimal(roi_limits['roi_p2_min'], roi_limits['roi_p2_max'], decimals=3,
                      name='roi_p2'),
            SKDecimal(roi_limits['roi_p3_min'], roi_limits['roi_p3_max'], decimals=3,
                      name='roi_p3'),
        ]