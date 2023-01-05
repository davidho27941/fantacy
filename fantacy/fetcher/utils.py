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