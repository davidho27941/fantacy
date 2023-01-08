import numpy as np
import pandas as pd

from decimal import (
    Decimal,
    getcontext,
)


class BasicAnalyzer:
    @staticmethod
    def SMA(
        dataframe: pd.DataFrame,
        interval: int = 5,
        target_col: str = "Close",
    ):
        dataframe[f"MA_{interval}"] = (
            dataframe[target_col]
            .rolling(interval)
            .apply(lambda x: x.sum() / x.shape[0])
        )
        return dataframe

    @staticmethod
    def EMA(
        dataframe: pd.DataFrame,
        interval: int = 5,
        target_col: str = "Close",
        is_EMA_of_EMA: bool = False,
    ):
        alpha = 1 / (interval + 1)

        if is_EMA_of_EMA:
            str_obj = dataframe.columns.str
            if str_obj.contains(pat="^EMA_[A-z]", regex=True).sum() == 0:
                dataframe[f"EMA_of_EMA_{interval}"] = (
                    dataframe[target_col].ewm(alpha=alpha, min_periods=5).mean()
                )
            elif str_obj.contains(pat="^EMA_[A-z]", regex=True).sum() == 1:
                dataframe[f"Tri_EMA_{interval}"] = (
                    dataframe[target_col].ewm(alpha=alpha, min_periods=5).mean()
                )
        else:
            dataframe[f"EMA_{interval}"] = (
                dataframe[target_col].ewm(alpha=alpha, min_periods=5).mean()
            )
        return dataframe

    @staticmethod
    def WMA(
        dataframe: pd.DataFrame,
        interval: int = 5,
        target_col: str = "Close",
    ):
        weights = np.arange(1, interval + 1, 1)
        dataframe[f"WMA_{interval}"] = (
            dataframe[target_col]
            .rolling(interval)
            .apply(lambda x: np.sum(weights * x) / np.sum(weights))
        )
        return dataframe
