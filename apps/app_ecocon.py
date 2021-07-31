import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd
import numpy as np
import datetime as dt
from dateutil.rrule import *

from app import app, folder_path
import funs


def get_weekly_cgi():
    # weekly CGI
    df_weekly = funs.read_csv(folder_path+'history_weekly.csv', 'Date')
    ori_cols = df_weekly.columns
    df_weekly['Global'] = df_weekly[['USD','EUR','GBP','JPY','AUD','NZD','CAD','CHF','SEK','NOK','CZK', 'PLN', 'HUF', 'TRY', 'ZAR', 'ILS', 'RUB','BRL', 'MXN', 'CLP', 'COP','INR', 'IDR', 'KRW', 'SGD', 'MYR', 'PHP', 'THB', 'TWD', 'CNY']].mean(axis=1)
    df_weekly['DM'] = df_weekly[['USD','EUR','GBP','JPY','AUD','NZD','CAD','CHF','SEK','NOK']].mean(axis=1)
    df_weekly['EM'] = df_weekly[['CZK', 'PLN', 'HUF', 'TRY', 'ZAR', 'ILS', 'RUB','BRL', 'MXN', 'CLP', 'COP','INR', 'IDR', 'KRW', 'SGD', 'MYR', 'PHP', 'THB', 'TWD', 'CNY']].mean(axis=1)
    df_weekly['Asia'] = df_weekly[['INR', 'IDR', 'KRW', 'SGD', 'MYR', 'PHP', 'THB', 'TWD', 'CNY']].mean(axis=1)
    df_weekly['CEEMEA'] = df_weekly[['CZK', 'PLN', 'HUF', 'TRY', 'ZAR', 'ILS', 'RUB']].mean(axis=1)
    df_weekly['LatAM'] = df_weekly[['BRL', 'MXN', 'CLP', 'COP']].mean(axis=1)
    df_weekly.index.name = 'date'
    df_weekly = df_weekly[['Global','DM','EM','Asia','CEEMEA','LatAM']+list(ori_cols)]
    df_weekly_4w = df_weekly.rolling(4).mean()
    df_weekly_12w = df_weekly.rolling(12).mean()
    return df_weekly, df_weekly_4w, df_weekly_12w

def get_monthly_cgi():
    # monthly CGI
    df_monthly = funs.read_csv(folder_path+'history.csv', 'Date')
    ori_cols = df_monthly.columns
    df_monthly['Global'] = df_monthly[['USD','EUR','GBP','JPY','AUD','NZD','CAD','CHF','SEK','NOK','CZK', 'PLN', 'HUF', 'TRY', 'ZAR', 'ILS', 'RUB','BRL', 'MXN', 'CLP', 'COP','INR', 'IDR', 'KRW', 'SGD', 'MYR', 'PHP', 'THB', 'TWD', 'CNY']].mean(axis=1)
    df_monthly['DM'] = df_monthly[['USD','EUR','GBP','JPY','AUD','NZD','CAD','CHF','SEK','NOK']].mean(axis=1)
    df_monthly['EM'] = df_monthly[['CZK', 'PLN', 'HUF', 'TRY', 'ZAR', 'ILS', 'RUB','BRL', 'MXN', 'CLP', 'COP','INR', 'IDR', 'KRW', 'SGD', 'MYR', 'PHP', 'THB', 'TWD', 'CNY']].mean(axis=1)
    df_monthly['Asia'] = df_monthly[['INR', 'IDR', 'KRW', 'SGD', 'MYR', 'PHP', 'THB', 'TWD', 'CNY']].mean(axis=1)
    df_monthly['CEEMEA'] = df_monthly[['CZK', 'PLN', 'HUF', 'TRY', 'ZAR', 'ILS', 'RUB']].mean(axis=1)
    df_monthly['LatAM'] = df_monthly[['BRL', 'MXN', 'CLP', 'COP']].mean(axis=1)
    df_monthly.index.name = 'date'
    df_monthly = df_monthly[['Global','DM','EM','Asia','CEEMEA','LatAM']+list(ori_cols)]
    return df_monthly

def get_pmi():
    # PMI
    df_jpm_pmi = funs.read_pmi()
    df_jpm_pmi['New orders-inventory'] = df_jpm_pmi['Manufacturing New orders'] - df_jpm_pmi['Manufacturing Finished goods inventories']
    df_jpm_pmi['Purchase-inventory'] = df_jpm_pmi['Manufacturing Stocks of purchases'] - df_jpm_pmi['Manufacturing Finished goods inventories']
    df_jpm_pmi = df_jpm_pmi[['Manufacturing Overall','Manufacturing New orders','New orders-inventory','Purchase-inventory','Manufacturing Output prices']]
    df_jpm_pmi.index.name = 'date'
    df_jpm_pmi.columns = ['JPM Global - Overall','JPM Global - New orders','JPM Global - New orders-inventory','JPM Global - Purchase-inventory', 'JPM Global - Output prices']
    dates = list(rrule(MONTHLY, dtstart=df_jpm_pmi.index[0], until=df_jpm_pmi.index[-1] + dt.timedelta(days=35), bymonthday=-1))
    df_jpm_pmi['date'] = dates
    df_jpm_pmi.set_index('date', inplace=True)

    store = pd.HDFStore('H:\\data\\hdf\\pmi.h5', mode='r')
    df_bbg_pmi = pd.DataFrame()
    for i in store.keys():
        if i not in ['JPY1_MAN']:
            df_bbg_pmi[i.split('_')[0][1:]] = store[i]['closep']
    store.close()
    ori_cols = df_bbg_pmi.columns
    df_bbg_pmi['Global Average'] = df_bbg_pmi.mean(axis=1)
    df_bbg_pmi['DM'] = df_bbg_pmi[['USD','EUR','GBP','AUD','JPY','CAD','NOK','SEK']].mean(axis=1)
    df_bbg_pmi['EM'] = df_bbg_pmi[['CZK','PLN','HUF','BRL','MXN','TRY','ZAR','ILS','RUB','INR','IDR','KRW','SGD','MYR','PHP','THB','TWD','CNY']].mean(axis=1)
    df_bbg_pmi['Asia'] = df_bbg_pmi[['INR','IDR','KRW','SGD','MYR','PHP','THB','TWD','CNY']].mean(axis=1)
    df_bbg_pmi['CEEMEA'] = df_bbg_pmi[['CZK','PLN','HUF','TRY','ZAR','ILS','RUB']].mean(axis=1)
    df_bbg_pmi['Eurozone'] = df_bbg_pmi[['France','Germany','Italy','Spain']].mean(axis=1)
    df_bbg_pmi.index.name = 'date'
    df_bbg_pmi = df_bbg_pmi[['Global Average','DM','EM','Asia','CEEMEA']+list(ori_cols)]

    df_pmi = pd.concat([df_jpm_pmi, df_bbg_pmi], axis=1)
    return df_pmi

def get_oecd():
    # OECD
    df_oecd = funs.read_csv(folder_path + 'oecd_unrevised.csv')
    ori_cols = df_oecd.columns
    df_oecd['Global'] = df_oecd[['USD','EUR','GBP','JPY','AUD','NZD','CAD','CHF','SEK','NOK','CZK', 'PLN', 'HUF', 'TRY', 'ZAR', 'ILS', 'RUB','BRL', 'MXN', 'CLP', 'INR', 'IDR', 'KRW', 'CNY']].mean(axis=1)
    df_oecd['DM'] = df_oecd[['USD','EUR','GBP','JPY','AUD','NZD','CAD','CHF','SEK','NOK']].mean(axis=1)
    df_oecd['EM'] = df_oecd[['CZK', 'PLN', 'HUF', 'TRY', 'ZAR', 'ILS', 'RUB','BRL', 'MXN', 'CLP', 'INR', 'IDR', 'KRW', 'CNY']].mean(axis=1)
    df_oecd['Asia'] = df_oecd['Asia5']
    df_oecd['CEEMEA'] = df_oecd[['CZK', 'PLN', 'HUF', 'TRY', 'ZAR', 'ILS', 'RUB']].mean(axis=1)
    df_oecd['LatAM'] = df_oecd[['BRL', 'MXN', 'CLP']].mean(axis=1)
    df_oecd.index.name = 'date'
    df_oecd = df_oecd[['Global','DM','EM','Asia','CEEMEA','LatAM']+list(ori_cols)]
    return df_oecd


df_weekly, df_weekly_4w, df_weekly_12w = get_weekly_cgi()
df_monthly = get_monthly_cgi()
df_pmi = get_pmi()
df_oecd = get_oecd()

layout = html.Div([
    # weekly CGI
    html.Div([
        html.H3(children='Weekly Economic Growth', style={'font-size': '1.2em'}),

        html.Div(children=[
            html.Label(["Choose a region..."], style={"font-style": "italic"}),
            dcc.Dropdown(
                id='cgiw-dropdown',
                options=[
                        {'label': '{}'.format(i), 'value': i} for i in df_weekly.columns
                    ],
                value='Global'
                )],
            style={"width": "45%",'display': 'inline-block'},
            ),

        html.Div(children=[
            html.Label(["Choose start time..."], style={"font-style": "italic"}),
            dcc.RadioItems(
                id='cgiw-radio',
                options=[
                    {'label': 'Full', 'value': dt.datetime(2001,1,1)},
                    {'label': 'From 2010', 'value': dt.datetime(2010,1,1)},
                    {'label': 'Last 5 years', 'value': dt.datetime(dt.datetime.now().year - 5, 1, 1)},
                    {'label': 'Last 3 years', 'value': dt.datetime(dt.datetime.now().year-3,1,1)}
                    ],
                value=dt.datetime(dt.datetime.now().year-3,1,1),
                labelStyle={'display': 'inline-block', 'margin-right': 10}
                )],
            style={"width": "45%",'float': 'right','margin': 'auto'},
            ),

        html.Br(),
        html.Br(),
        html.Div(id='display-cgiw-performance', style={"font-weight": "bold"},),
        dcc.Graph(id='cgiw-chart'),
        ]),

    # monthly CGI
    html.Div([
        html.H3(children='Monthly Economic Growth', style={'font-size': '1.2em'}),

        html.Div(children=[
            html.Label(["Choose a region..."], style={"font-style": "italic"}),
            dcc.Dropdown(
                id='cgim-dropdown',
                options=[
                    {'label': '{}'.format(i), 'value': i} for i in df_monthly.columns
                ],
                value='Global'
            )],
            style={"width": "45%", 'display': 'inline-block'},
        ),

        html.Div(children=[
            html.Label(["Choose start time..."], style={"font-style": "italic"}),
            dcc.RadioItems(
                id='cgim-radio',
                options=[
                    {'label': 'Full', 'value': dt.datetime(2001,1,1)},
                    {'label': 'From 2010', 'value': dt.datetime(2010, 1, 1)},
                    {'label': 'Last 5 years', 'value': dt.datetime(dt.datetime.now().year - 5, 1, 1)},
                    {'label': 'Last 3 years', 'value': dt.datetime(dt.datetime.now().year - 3, 1, 1)}
                ],
                value=dt.datetime(dt.datetime.now().year - 5, 1, 1),
                labelStyle={'display': 'inline-block', 'margin-right': 10}
            )],
            style={"width": "45%", 'float': 'right', 'margin': 'auto'},
        ),

        html.Br(),
        html.Br(),
        html.Div(id='display-cgim-performance', style={"font-weight": "bold"}, ),
        dcc.Graph(id='cgim-chart'),
    ]),

    # PMI
    html.Div([
        html.H3(children='Manufacture PMI', style={'font-size': '1.2em'}),

        html.Div(children=[
            html.Label(["Choose a region..."], style={"font-style": "italic"}),
            dcc.Dropdown(
                id='pmi-dropdown',
                options=[
                    {'label': '{}'.format(i), 'value': i} for i in df_pmi.columns
                ],
                value='Global Average'
            )],
            style={"width": "45%", 'display': 'inline-block'},
        ),

        html.Div(children=[
            html.Label(["Choose start time..."], style={"font-style": "italic"}),
            dcc.RadioItems(
                id='pmi-radio',
                options=[
                    {'label': 'Full', 'value': dt.datetime(1998, 1, 1)},
                    {'label': 'From 2010', 'value': dt.datetime(2010, 1, 1)},
                    {'label': 'Last 5 years', 'value': dt.datetime(dt.datetime.now().year - 5, 1, 1)},
                    {'label': 'Last 3 years', 'value': dt.datetime(dt.datetime.now().year - 3, 1, 1)}
                ],
                value=dt.datetime(dt.datetime.now().year - 5, 1, 1),
                labelStyle={'display': 'inline-block', 'margin-right': 10}
            )],
            style={"width": "45%", 'float': 'right', 'margin': 'auto'},
        ),

        html.Br(),
        html.Br(),
        html.Div(id='display-pmi-performance', style={"font-weight": "bold"}, ),
        dcc.Graph(id='pmi-chart'),
    ]),

    # OECD
    html.Div([
        html.H3(children='OECD Leading Indicator', style={'font-size': '1.2em'}),

        html.Div(children=[
            html.Label(["Choose a region..."], style={"font-style": "italic"}),
            dcc.Dropdown(
                id='oecd-dropdown',
                options=[
                    {'label': '{}'.format(i), 'value': i} for i in df_oecd.columns
                ],
                value='Global'
            )],
            style={"width": "45%", 'display': 'inline-block'},
        ),

        html.Div(children=[
            html.Label(["Choose start time..."], style={"font-style": "italic"}),
            dcc.RadioItems(
                id='oecd-radio',
                options=[
                    {'label': 'Full', 'value': dt.datetime(2000, 1, 1)},
                    {'label': 'From 2010', 'value': dt.datetime(2010, 1, 1)},
                    {'label': 'Last 5 years', 'value': dt.datetime(dt.datetime.now().year - 5, 1, 1)},
                    {'label': 'Last 3 years', 'value': dt.datetime(dt.datetime.now().year - 3, 1, 1)}
                ],
                value=dt.datetime(dt.datetime.now().year - 5, 1, 1),
                labelStyle={'display': 'inline-block', 'margin-right': 10}
            )],
            style={"width": "45%", 'float': 'right', 'margin': 'auto'},
        ),

        html.Br(),
        html.Br(),
        html.Div(id='display-oecd-performance', style={"font-weight": "bold"}, ),
        dcc.Graph(id='oecd-chart'),
    ]),
])

# weekly CGI
@app.callback(
    Output('display-cgiw-performance', 'children'),
    Input('cgiw-dropdown', 'value'))
def display_summary(value):
    df_weekly, df_weekly_4w, df_weekly_12w = get_weekly_cgi()
    latest_index = dt.datetime.strftime(df_weekly[value].index[-1], format='%Y-%m-%d')
    last_value = df_weekly[value].iloc[-1]
    last_4w = df_weekly_4w[value].iloc[-1]
    last_12w = df_weekly_12w[value].iloc[-1]
    return """Latest update {:s}, weekly CGI: {:.2f}, 4w mva: {:.2f}, 12w mva {:.2f}.
            """.format(latest_index, last_value, last_4w, last_12w)

@app.callback(
    Output('cgiw-chart', 'figure'),
    Input('cgiw-dropdown', 'value'),
    Input('cgiw-radio', 'value'))
def display_chart(value, sdate):
    df_weekly, df_weekly_4w, df_weekly_12w = get_weekly_cgi()
    df1 = df_weekly.loc[sdate:, value]
    df2 = df_weekly_4w.loc[sdate:, value]
    df3 = df_weekly_12w.loc[sdate:, value]
    df = pd.concat([df1, df2, df3], axis=1)
    df.columns = ['weekly CGI','4w mva','12w mva']
    fig = px.line(df)
    fig.update_layout(
        title_text="Weekly Economic Growth Indicator - " + value,
        template="seaborn",
        # showlegend=False,
        # dragmode='pan',
        # xaxis=dict(rangeslider=dict(visible=True), type="date")
    )
    return fig


# monthly CGI
@app.callback(
    Output('display-cgim-performance', 'children'),
    Input('cgim-dropdown', 'value'))
def display_summary(value):
    df_monthly = get_monthly_cgi()
    latest_index = dt.datetime.strftime(df_monthly[value].index[-1], format='%Y-%m-%d')
    last_value = df_monthly[value].iloc[-1]
    return """Latest update {:s}, monthly CGI: {:.2f}, 3m change: {:.2f}.
            """.format(latest_index, last_value, df_monthly[value].iloc[-1]-df_monthly[value].iloc[-4])

@app.callback(
    Output('cgim-chart', 'figure'),
    Input('cgim-dropdown', 'value'),
    Input('cgim-radio', 'value'))
def display_chart(value, sdate):
    df_monthly = get_monthly_cgi()
    df1 = df_monthly.loc[sdate:, value]
    fig = px.line(df1)
    fig.update_layout(
        title_text="Monthly Economic Growth Indicator - " + value,
        template="seaborn",
        showlegend=True,
        # dragmode='pan',
        # xaxis=dict(rangeslider=dict(visible=True), type="date")
    )
    return fig

# PMI
@app.callback(
    Output('display-pmi-performance', 'children'),
    Input('pmi-dropdown', 'value'))
def display_summary(value):
    df_pmi = get_pmi()
    latest_index = dt.datetime.strftime(df_pmi[value].index[-1], format='%Y-%m-%d')
    last_value = df_pmi[value].iloc[-1]
    return """Latest update {:s}, Manufacture PMI: {:.2f}, 3m change: {:.2f}.
            """.format(latest_index, last_value, df_pmi[value].iloc[-1]-df_pmi[value].iloc[-4])

@app.callback(
    Output('pmi-chart', 'figure'),
    Input('pmi-dropdown', 'value'),
    Input('pmi-radio', 'value'))
def display_chart(value, sdate):
    df_pmi = get_pmi()
    df1 = df_pmi.loc[sdate:, value]
    fig = px.line(df1)
    fig.update_layout(
        title_text="Manufacture PMI - " + value,
        template="seaborn",
        showlegend=False,
        # dragmode='pan',
        # xaxis=dict(rangeslider=dict(visible=True), type="date")
    )
    return fig

# OECD
@app.callback(
    Output('display-oecd-performance', 'children'),
    Input('oecd-dropdown', 'value'))
def display_summary(value):
    df_oecd = get_oecd()
    latest_index = dt.datetime.strftime(df_oecd[value].index[-1], format='%Y-%m-%d')
    last_value = df_oecd[value].iloc[-1]
    return """Latest update {:s}, OECD CLI: {:.2f}, 3m change: {:.2f}.
            """.format(latest_index, last_value, df_oecd[value].iloc[-1]-df_oecd[value].iloc[-4])

@app.callback(
    Output('oecd-chart', 'figure'),
    Input('oecd-dropdown', 'value'),
    Input('oecd-radio', 'value'))
def display_chart(value, sdate):
    df_oecd = get_oecd()
    df1 = df_oecd.loc[sdate:, value]
    fig = px.line(df1)
    fig.update_layout(
        title_text="OECD CLI - " + value,
        template="seaborn",
        showlegend=False,
        # dragmode='pan',
        # xaxis=dict(rangeslider=dict(visible=True), type="date")
    )
    return fig