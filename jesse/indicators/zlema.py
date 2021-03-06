from typing import Union

import numpy as np
import tulipy as ti

from jesse.helpers import get_candle_source
from jesse.helpers import get_config


def zlema(candles: np.ndarray, period: int = 20, source_type: str = "close", sequential: bool = False) -> Union[
    float, np.ndarray]:
    """
    Zero-Lag Exponential Moving Average

    :param candles: np.ndarray
    :param period: int - default: 20
    :param source_type: str - default: "close"
    :param sequential: bool - default=False

    :return: float | np.ndarray
    """
    warmup_candles_num = get_config('env.data.warmup_candles_num', 240)
    if not sequential and len(candles) > warmup_candles_num:
        candles = candles[-warmup_candles_num:]

    source = get_candle_source(candles, source_type=source_type)
    res = ti.zlema(np.ascontiguousarray(source), period=period)

    return np.concatenate((np.full((candles.shape[0] - res.shape[0]), np.nan), res), axis=0) if sequential else res[-1]
