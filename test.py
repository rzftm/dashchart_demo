import pandas as pd
import os
import funs
import app
import io
import requests

def test_excel():
    df_fri = pd.read_excel('H:\\_CODE\\dashchart_demo\\data\\JPM_Global_PMI_Historica_2021-07-06_3793624.xlsx','Global PMI', skiprows=[0, 1, 2, 3, 5])
    print(df_fri.tail())

def test_path():
    rootpath = os.path.abspath(__file__)
    directory = os.path.split(rootpath)[0]

def test_csv():
    # user = 'rzhao30@gmail.com'
    # pao = 'RLpass10209'
    # github_session = requests.Session()
    # github_session.auth = (user, pao)

    data_path = app.folder_path + "trend_performance.csv"
    df = funs.read_csv(data_path)

    # download = github_session.get(data_path).content
    # downloaded_csv = pd.read_csv(io.StringIO(download.decode('utf-8')), error_bad_lines=False)

    # CONFIRMED_CONTENT = requests.get(data_path).content
    # CONFIRMED = pd.read_csv(io.StringIO(CONFIRMED_CONTENT.decode('utf-8')))
    print(df)

if __name__ == '__main__':
    test_csv()