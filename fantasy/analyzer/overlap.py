import pandas as pd
import numpy as np

from .basic import BasicAnalyzer

class Overlap():
    @staticmethod
    def DEMA(
        dataframe: pd.DataFrame,
        interval: int = 5,
        target_col: str = "Close",
    ):
        str_obj = dataframe.columns.str
        if str_obj.contains(pat="^EMA", regex=True).sum() == 0:
            dataframe.pipe(
                BasicAnalyzer.EMA,
                interval=interval,
                target_col=target_col,
            )
        dataframe.pipe(
            BasicAnalyzer.EMA,
            interval=interval,
            target_col=f"EMA_{interval}",
            is_EMA_of_EMA=True,
        )

        dataframe[f"DEMA_{interval}"] = (
            2 * dataframe[f"EMA_{interval}"] - dataframe[f"EMA_of_EMA_{interval}"]
        )
        return dataframe

    @staticmethod
    def TEMA(
        dataframe: pd.DataFrame,
        interval: int = 5,
        target_col: str = "Close",
    ):
        str_obj = dataframe.columns.str
        if str_obj.contains(pat="^EMA", regex=True).sum() == 0:
            (
                dataframe.pipe(
                    BasicAnalyzer.EMA,
                    interval=interval,
                    target_col=target_col,
                ).pipe(
                    BasicAnalyzer.EMA,
                    interval=interval,
                    target_col=f"EMA_{interval}",
                    is_EMA_of_EMA=True,
                )
            )

        elif str_obj.contains(pat="^EMA_\d", regex=True).sum() == 1:
            dataframe.pipe(
                BasicAnalyzer.EMA,
                interval=interval,
                target_col=f"EMA_{interval}",
                is_EMA_of_EMA=True,
            )

        dataframe.pipe(
            BasicAnalyzer.EMA,
            interval=interval,
            target_col=f"EMA_of_EMA_{interval}",
            is_EMA_of_EMA=True,
        )

        dataframe[f"DEMA_{interval}"] = (
            3 * dataframe[f"EMA_{interval}"]
            - 3 * dataframe[f"EMA_of_EMA_{interval}"]
            - dataframe[f"EMA_{interval}"]
        )

    @staticmethod
    def TRIMA(
        dataframe: pd.DataFrame,
        interval: int = 5,
        target_col: str = "Close",
    ):
        str_obj = dataframe.columns.str
        if str_obj.contains(pat="^MA", regex=True).sum() == 0:
            dataframe.pipe(
                BasicAnalyzer.SMA,
                interval=interval,
                target_col=target_col,
            )

        dataframe[f'TRIMA_{interval}'] = (
            dataframe[f'MA_{interval}']
            .rolling(interval)
            .apply(lambda x: x.sum() / x.shape[0])
        )
    
    @staticmethod
    def KAMA(
        dataframe: pd.DataFrame,
        interval: int = 5,
        f: int = 2, 
        s: int = 30, 
    ):
        dataframe['Direction'] = (
            dataframe['Close']
            .rolling(2)
            .apply(np.diff)
        )
        dataframe['Volatility'] = (
            dataframe['Direction']
            .rolling(interval)
            .apply(lambda x: x.abs().sum())
        )
        dataframe['ER'] = (
            np.abs(dataframe['Direction'] / dataframe['Volatility'])
        )
