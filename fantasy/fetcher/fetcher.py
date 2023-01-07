import requests
import pandas as pd

from yarl import URL
from fantasy.fetcher.base import BaseFetcher
from fantasy.fetcher.utils import getListing


class TWSEFetcher(BaseFetcher):
    def __init__(self):
        self.url = URL("https://www.twse.com.tw").with_path(
            "/en/exchangeReport/STOCK_DAY"
        )

    def transform(self, result):
        _data = result.json()["data"]
        _column_name = result.json()["fields"]
        DataFrame = pd.DataFrame(_data, columns=_column_name)
        DataFrame.columns = [
            "Date",
            "Trade_Volume",
            "Trade_Value",
            "Open",
            "High",
            "Low",
            "Close",
            "Change",
            "Transaction",
        ]
        DataFrame = DataFrame.assign(
            Trade_Volume=lambda df: df["Trade_Volume"].str.replace(",", ""),
            Trade_Value=lambda df: df["Trade_Value"].str.replace(",", ""),
            Transaction=lambda df: df["Transaction"].str.replace(",", ""),
            Change=lambda df: df["Change"].str.replace("X", ""),
        ).astype(
            {
                "Open": "float64",
                "High": "float64",
                "Low": "float64",
                "Close": "float64",
                "Change": "float64",
                "Transaction": int,
                "Trade_Volume": int,
                "Trade_Value": int,
            }
        )
        return DataFrame

    def fetch(
        self,
        sid: str,
        year: str,
        month: str,
        date: str,
    ):
        date_format = "{0}{1:2}{2}".format(year, month, date)
        self.url = self.url.with_query(
            {
                "response": "json",
                "date": date_format,
                "stockNo": sid,
            }
        )
        result = requests.get(self.url)
        parsedResult = self.transform(result)
        return parsedResult


class TPEXFetcher(BaseFetcher):
    def __init__(self):
        self.url = URL("http://www.tpex.org.tw").with_path(
            "/web/stock/aftertrading/daily_trading_info/st43_print.php"
        )

    def transform(self, result):
        DataFrame = pd.read_html(result.text)[0]
        DataFrame.columns = [
            "Date",
            "Trade_Volume_1000",
            "Trade_Value_1000",
            "Open",
            "High",
            "Low",
            "Close",
            "Change",
            "Transaction",
        ]
        DataFrame = DataFrame.iloc[:-1]
        DataFrame = (
            DataFrame.astype(
                {
                    "Trade_Volume_1000": int,
                    "Trade_Value_1000": int,
                    "Open": "float64",
                    "High": "float64",
                    "Low": "float64",
                    "Close": "float64",
                    "Change": "float64",
                    "Transaction": int,
                }
            )
            .assign(
                Trade_Volume=lambda df: df["Trade_Volume_1000"] * 1000,
                Trade_Value=lambda df: df["Trade_Value_1000"] * 1000,
            )
            .drop(
                columns=[
                    "Trade_Volume_1000",
                    "Trade_Value_1000",
                ]
            )
        )
        return DataFrame

    def fetch(
        self,
        sid: str,
        year: str,
        month: str,
        date: str,
    ):
        date_format = "{0}/{1:2}".format(year, month)
        self.url = self.url.with_query(
            {
                "l": "en-us",
                "d": date_format,
                "stkno": sid,
                "s": "0,asc,0",
            }
        )
        result = requests.get(self.url)
        parsedResult = self.transform(result)
        return parsedResult


class Fetcher(BaseFetcher):
    def __init__(self, sid, require_volume=False):
        self.sid = sid
        self.require_volume = require_volume
        self.col_without_volume = [
            "Date",
            "Open",
            "High",
            "Low",
            "Close",
        ]
        self.fetcher = (
            TWSEFetcher()
            if str(self.sid) in getListing(target="TWSE")["代號"].to_list()
            else TPEXFetcher()
        )

    def transform(self, result):
        if not self.require_volume:
            result = result[self.col_without_volume]

        return result

    def fetch(
        self,
        year: str,
        month: str,
        date: str,
    ):
        result = self.fetcher.fetch(
            self.sid,
            year,
            month,
            date,
        )
        parsedResult = self.transform(result)
        return parsedResult
