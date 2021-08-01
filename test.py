import pandas as pd
import os

def test_excel():
    df_fri = pd.read_excel('H:\\_CODE\\dashchart_demo\\data\\JPM_Global_PMI_Historica_2021-07-06_3793624.xlsx','Global PMI', skiprows=[0, 1, 2, 3, 5])
    print(df_fri.tail())

def test_path():
    rootpath = os.path.abspath(__file__)
    directory = os.path.split(rootpath)[0]

if __name__ == '__main__':
    test_path()