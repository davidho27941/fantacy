import os
import requests
import pandas as pd

from yarl import URL

artifacts_root = os.getcwd()

def transform_date(data):
    year = list(data['date'].str.split('/', expand=True)[0].astype(int) + 1911)
    month = list(data['date'].str.split('/', expand=True)[1])
    day = list(data['date'].str.split('/', expand=True)[2])
    date = [f'{_year}/{_month}/{_day}' for _year, _month, _day in zip(year, month, day)]
    data['date'] = pd.to_datetime(date, format='%Y/%m/%d')

def fetchListing(target='TWSE'):
    url = URL("http://isin.twse.com.tw/isin/C_public.jsp")
    match target:
        case 'TWSE':
            result = requests.get(url.with_query({"strMode": 2}))
        case 'TPEX':
            result = requests.get(url.with_query({"strMode": 4}))
    df = pd.read_html(result.text)[0]
    df.columns = df.iloc[0]
    df = df.iloc[2:]
    df['代號'] = df['有價證券代號及名稱'].str.split(expand=True)[0]
    df['名稱'] = df['有價證券代號及名稱'].str.split(expand=True)[1]
    df = df.drop(columns=["有價證券代號及名稱"])
    df.to_csv(os.path.join(artifacts_root, f"{target}.csv"))
    return df

def getListing(target='TWSE'):
    record_path = os.path.join(artifacts_root, f"{target}.csv")
    if os.path.exists(record_path):
        df = pd.read_csv(record_path)
    else:
        df = fetchListing(target=target)
    return df


# Deprecated
# def fetchTWSEListingStock(url=TWSE_LISTING_STOCK_URL):
#     if os.path.exists(artifacts_root+"/twse_listing.csv"):
#         df = pd.read_csv(artifacts_root+"/twse_listing.csv")
#     else:
#         result = requests.get(url)
#         df = pd.read_html(result.text)[0]
#     return df

# def fetchTPEXListingStock(url=TPEX_LISTING_STOCK_URL):
#     if os.path.exists(artifacts_root+"/tpex_listing.csv"):
#         df = pd.read_csv(artifacts_root+"/tpex_listing.csv")
#     else:
#         result = requests.get(url)
#         df = pd.read_html(result.text)[0]
#     return df

# def getTWSEListingStock():
#     if os.path.exists(os.path.join(artifacts_root, "TWSE.csv")):
#         TWSE_Listing_df = pd.read_csv()
#     TWSE_Listing_df = fetchListing(target='TWSE')
#     TWSE_Listing_df.columns = TWSE_Listing_df.iloc[0]
#     TWSE_Listing_df = TWSE_Listing_df.iloc[2:]
#     TWSE_Listing_df['代號'] = TWSE_Listing_df['有價證券代號及名稱'].str.split(expand=True)[0]
#     TWSE_Listing_df['名稱'] = TWSE_Listing_df['有價證券代號及名稱'].str.split(expand=True)[1]
#     return TWSE_Listing_df

# def getTPEXListingStock():
#     TPEX_Listing_Stock_df = fetchListing(target='TPEX')
#     TPEX_Listing_Stock_df.columns = TPEX_Listing_Stock_df.iloc[0]
#     TPEX_Listing_Stock_df = TPEX_Listing_Stock_df.iloc[2:]
#     TPEX_Listing_Stock_df['代號'] = TPEX_Listing_Stock_df['有價證券代號及名稱'].str.split(expand=True)[0]
#     TPEX_Listing_Stock_df['名稱'] = TPEX_Listing_Stock_df['有價證券代號及名稱'].str.split(expand=True)[1]
#     return TPEX_Listing_Stock_df