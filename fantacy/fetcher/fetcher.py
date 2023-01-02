import requests
import pandas as pd

from yarl import URL
from base import BaseFetcher

class TWSEFetcher(BaseFetcher):
    def __init__(self):
        self.url = (
            URL("https://www.twse.com.tw")
            .with_path(
                "/exchangeReport/STOCK_DAY"
            )
        )
    
    def transform(self, result):
        _data = result.json()['data']
        _column_name = result.json()['fields']
        return pd.DataFrame(_data, columns=_column_name)

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
        self.url = (
            URL(
                "http://www.tpex.org.tw"
            ).with_path(
                "/web/stock/aftertrading/daily_trading_info/st43_print.php"
            )
        )
    
    def transform(self, result):
        DataFrame = pd.read_html(result.text)[0]
        DataFrame.columns = [
            '日期',
            '成交仟股',
            '成交仟元',
            '開盤',
            '最高',
            '最低',
            '收盤',
            '漲跌',
            '筆數'
        ]
        DataFrame = DataFrame.iloc[:-1]
        return DataFrame
    
    def fetch(
        self,
        sid: str,
        year: str,
        month: str,
        date: str,
    ):
        date_format = "{0}/{1:2}".format(str(year)-1911, month)
        self.url = self.url.with_query(
            {
                "l": "zh-tw",
                "d": date_format,
                "stkno": sid,
                "s": "0,asc,0",
            }
        )
        self.result = requests.get(self.url)
        return self.result