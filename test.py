import pandas as pd

def test_excel():
    df_fri = pd.read_excel('H:\\_CODE\\dashchart_demo\\data\\JPM_Global_PMI_Historica_2021-07-06_3793624.xlsx','Global PMI', skiprows=[0, 1, 2, 3, 5])
    print(df_fri.tail())

if __name__ == '__main__':
    test_excel()