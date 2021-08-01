import pandas as pd
import numpy as np
import datetime as dt
import math
import os
from app import folder_path


def performance_summary(data, capital=1):
    '''
    input is daily pnl (pn.Series), calculate performance
    '''
    if len(data) >= 260:
        factor = 260
    else:
        factor = len(data)
    ann_rtn = data.mean() / capital * factor
    vol = data.std() / capital * math.sqrt(factor)
    sharpe = ann_rtn / vol
    cum_rtn = data.cumsum()
    drawdown = cum_rtn - cum_rtn.cummax()
    max_dd = drawdown.min()
    calmar = abs(ann_rtn / max_dd)
    return ann_rtn, vol, sharpe, max_dd, calmar, cum_rtn, drawdown


def read_csv(data_path, index_name='Unnamed: 0'):
    '''
    read csv and change index
    '''
    # df = pd.read_csv(data_path)
    df = pd.read_csv(data_path, sep=",")
    df.set_index(index_name, inplace=True)
    try:
        df.index = pd.to_datetime(df.index, format="%d/%m/%Y")
    except:
        df.index = pd.to_datetime(df.index, format="%Y-%m-%d")

    return df


def read_pnl(data_path):
    df = pd.read_excel(data_path, 'pnl')
    df.set_index('Unnamed: 0', inplace=True)
    try:
        df.index = pd.to_datetime(df.index, format="%d/%m/%Y")
    except:
        df.index = pd.to_datetime(df.index, format="%Y-%m-%d")
    return df[['DailyReturn']]


def read_pmi():
    '''
    read the latest JPM Global PMI to Dataframe
    '''

    fri_path = folder_path
    onlyfiles = [f for f in os.listdir(fri_path) if os.path.isfile(os.path.join(fri_path, f))]
    jpmf = [s for s in onlyfiles if "JPM_Global_PMI_Historica" in s]
    jpmds = [s.split('_')[4] for s in jpmf]
    jpmd = [dt.datetime.strptime(date, "%Y-%m-%d") for date in jpmds]
    file_name = jpmf[jpmd.index(max(jpmd))]

    df_fri = pd.read_excel(fri_path + file_name, 'Global PMI', skiprows=[0, 1, 2, 3, 5])
    df_fri.columns = ['Date', 'Manufacturing Overall','Manufacturing Output',
                      'Manufacturing New orders','Manufacturing Export orders',
                      'Manufacturing Input prices','Manufacturing Suppliers delivery times',
                      'Manufacturing Stocks of purchases','Manufacturing Finished goods inventories',
                      'Manufacturing Employment','Manufacturing Output prices',
                      'Manufacturing JPMorgan global manufacturing PMI - quantity of purchases',
                      'Manufacturing Backlogs of work','Manufacturing Future output',
                      'Services Business activity','Services New business',
                      'Services Input prices','Services Employment','Services Backlogs of work',
                      'Services Output prices','Services Future business activity',
                      'All-industry Output/business activity','All-industry New business',
                      'All-industry Input prices','All-industry Employment',
                      'All-industry Output prices','All-industry Backlogs of work']
    df_fri.set_index('Date', inplace=True)
    df_fri.index = pd.to_datetime(df_fri.index, format='%Y-%m-%d')
    for k in df_fri.columns:
        df_fri[k] = df_fri[k].apply(lambda x: np.NaN if isinstance(x, str) else x)
    df_fri = df_fri.apply(pd.to_numeric)

    return df_fri


def percentilerank(X, p):
    '''
    calculate percentile rank, return a number between 0 and 1
    '''

    if isinstance(X, pd.Series) or isinstance(X, pd.DataFrame):
        X = X.values

    # delete nan
    try:
        x = X[~np.isnan(X)]
    except:
        x = X

    # non nan value should be more than half of len
    if len(x) < 0.5 * len(X):
        prank = np.nan

    # p should not be nan
    elif math.isnan(p):
        prank = np.nan
    elif p >= max(x):
        prank = 1
    elif p <= min(x):
        prank = 0
    else:
        n = len(x)
        b = sum(float(num) < p for num in x)
        eq = sum(float(num) == p for num in x)
        r = b + eq
        s = np.sort(x)
        x1 = s[r - 1]
        x2 = s[r]
        rx1 = float(r - 1) / n
        rx2 = float(r) / n
        prank = float(b + 0.5 * eq) / n + (p - x1) / (x2 - x1) * (rx2 - rx1)

    return prank
