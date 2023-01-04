import os
import requests
import pandas as pd

from yarl import URL

TWSE_LISTING_STOCK_URL = 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
TPEX_LISTING_STOCK_URL = 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=4'

artifacts_root = os.getcwd()

def transform_date(data):
    year = list(data['date'].str.split('/', expand=True)[0].astype(int) + 1911)
    month = list(data['date'].str.split('/', expand=True)[1])
    day = list(data['date'].str.split('/', expand=True)[2])
    date = [f'{_year}/{_month}/{_day}' for _year, _month, _day in zip(year, month, day)]
    data['date'] = pd.to_datetime(date, format='%Y/%m/%d')

def fetchTWSEListingStock(url=TWSE_LISTING_STOCK_URL):
    if os.path.exists(artifacts_root+"/twse_listing.csv"):
        df = pd.read_csv(artifacts_root+"/twse_listing.csv")
    else:
        result = requests.get(url)
        df = pd.read_html(result.text)[0]
    return df

def fetchTPEXListingStock(url=TPEX_LISTING_STOCK_URL):
    if os.path.exists(artifacts_root+"/tpex_listing.csv"):
        df = pd.read_csv(artifacts_root+"/tpex_listing.csv")
    else:
        result = requests.get(url)
        df = pd.read_html(result.text)[0]
    return df

def getTWSEListingStock():
    TWSE_Listing_df = fetchTWSEListingStock()
    TWSE_Listing_df.columns = TWSE_Listing_df.iloc[0]
    TWSE_Listing_df = TWSE_Listing_df.iloc[2:]
    TWSE_Listing_df['代號'] = TWSE_Listing_df['有價證券代號及名稱'].str.split(expand=True)[0]
    TWSE_Listing_df['名稱'] = TWSE_Listing_df['有價證券代號及名稱'].str.split(expand=True)[1]
    return TWSE_Listing_df

def getTPEXListingStock():
    TPEX_Listing_Stock_df = fetchTPEXListingStock()
    TPEX_Listing_Stock_df.columns = TPEX_Listing_Stock_df.iloc[0]
    TPEX_Listing_Stock_df = TPEX_Listing_Stock_df.iloc[2:]
    TPEX_Listing_Stock_df['代號'] = TPEX_Listing_Stock_df['有價證券代號及名稱'].str.split(expand=True)[0]
    TPEX_Listing_Stock_df['名稱'] = TPEX_Listing_Stock_df['有價證券代號及名稱'].str.split(expand=True)[1]
    return TPEX_Listing_Stock_df