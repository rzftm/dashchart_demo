import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd
import datetime as dt

from app import app, folder_path
import funs


def get_sys_equity():
    # Systematic equity
    df_voltarget = funs.read_csv(folder_path + 'sp_vol_target.csv', 'Unnamed: 0')
    df_voltarget.columns = ['Vol Target']
    df_riskpar = funs.read_csv(folder_path + 'riskpar_equity_allocation.csv', 'Date')
    df_riskpar.columns = ['Risk Parity']
    df_cta = funs.read_csv(folder_path + 'cta_equity_allocation.csv', 'Date')
    df_cta.columns = ['CTA']
    df_sysequ = pd.concat([df_voltarget, df_riskpar, df_cta], axis=1)
    df_sysequ.index.name = 'date'
    return df_sysequ

def get_equity_senti():
    # Equity sentiment
    df_sp = funs.read_csv(folder_path + 'es_senti.csv')
    df_sp.columns = ['SP_sentiment', 'SP_price']
    df_sxxp = funs.read_csv(folder_path + 'vg_senti.csv')
    df_sxxp.columns = ['SXXP_sentiment', 'SXXP_price']
    df_aaii = funs.read_csv(folder_path + 'aaii.csv', 'date')
    df_aaii.columns = ['AAII_sentiment', 'AAII_price']
    df_senti = pd.concat([df_sp, df_sxxp, df_aaii], axis=1)
    df_senti.fillna(method='ffill', inplace=True)
    df_senti.index.name = 'date'
    return df_senti

def get_etf():
    # ETF
    df_em = funs.read_csv(folder_path + 'em_etf_flow.csv')
    df_em['EM ETF + US HY'] = df_em.sum(axis=1)
    df_em_equ = funs.read_csv(folder_path + 'em_equity_flow.csv')
    df_em_fi = funs.read_csv(folder_path + 'em_bond_flow.csv')
    df_gold = funs.read_csv(folder_path + 'gold_etf.csv','date')
    df_etf = pd.concat([df_em['EM ETF + US HY'], df_em_equ['daily'], df_em_fi['daily'], df_gold['holdings in troy ounce'].diff()], axis=1)
    df_etf.columns = ['EM ETF + US HY', 'EM Equity', 'EM fixed income', 'GOLD']
    df_etf = df_etf/1000
    df_etf.index.name = 'date'
    return df_etf

df_sysequ = get_sys_equity()
df_senti = get_equity_senti()
df_etf = get_etf()

layout = html.Div([

    # Systematic equity
    html.Div([
        html.H3(children='Systematic equity allocation', style={'font-size': '1.2em'}),

        html.Div(children=[
            html.Label(["Choose a model..."], style={"font-style": "italic"}),
            dcc.Dropdown(
                id='sysequ-dropdown',
                options=[
                        {'label': 'Model - {}'.format(i), 'value': i} for i in df_sysequ.columns
                    ],
                value='Vol Target'
                )],
            style={"width": "45%",'display': 'inline-block'},
            ),

        html.Div(children=[
            html.Label(["Choose start time..."], style={"font-style": "italic"}),
            dcc.RadioItems(
                id='sysequ-radio',
                options=[
                    {'label': 'Full', 'value': dt.datetime(2010, 1, 1)},
                    {'label': 'Last 5 years', 'value': dt.datetime(dt.datetime.now().year - 5, 1, 1)},
                    {'label': 'Last 3 years', 'value': dt.datetime(dt.datetime.now().year - 3, 1, 1)}
                ],
                value=dt.datetime(2010, 1, 1),
                labelStyle={'display': 'inline-block', 'margin-right': 10}
                )],
            style={"width": "45%",'float': 'right','margin': 'auto'},
            ),

        html.Br(),
        html.Br(),
        html.Div(id='display-sysequ-performance', style={"font-weight": "bold"},),
        dcc.Graph(id='sysequ-chart'),
    ]),

    # Equity sentiment
    html.Div([
        html.H3(children='Equity sentiment', style={'font-size': '1.2em'}),

        html.Div(children=[
            html.Label(["Choose an instrument..."], style={"font-style": "italic"}),
            dcc.Dropdown(
                id='senti-dropdown',
                options=[
                    {'label': '{}'.format(i), 'value': i} for i in ['SP','SXXP','AAII']
                ],
                value='SP'
            )],
            style={"width": "45%", 'display': 'inline-block'},
        ),

        html.Div(children=[
            html.Label(["Choose start time..."], style={"font-style": "italic"}),
            dcc.RadioItems(
                id='senti-radio',
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
        html.Div(id='display-senti-performance', style={"font-weight": "bold"}, ),
        dcc.Graph(id='senti-chart'),
    ]),

    # ETF
    html.Div([
        html.H3(children='EM ETF flow', style={'font-size': '1.2em'}),

        html.Div(children=[
            html.Label(["Choose an item..."], style={"font-style": "italic"}),
            dcc.Dropdown(
                id='etf-dropdown',
                options=[
                    {'label': 'Asset class - {}'.format(i), 'value': i} for i in df_etf.columns
                ],
                value='GOLD'
            )],
            style={"width": "45%", 'display': 'inline-block'},
        ),

        html.Div(children=[
            html.Label(["Choose start time..."], style={"font-style": "italic"}),
            dcc.RadioItems(
                id='etf-radio',
                options=[
                    {'label': 'Full', 'value': dt.datetime(2010, 1, 1)},
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
        html.Div(id='display-etf-performance', style={"font-weight": "bold"}, ),
        dcc.Graph(id='etf-chart'),
    ]),

])

# Systematic equity
@app.callback(
    Output('display-sysequ-performance', 'children'),
    Input('sysequ-dropdown', 'value'),
    Input('sysequ-radio', 'value'))
def display_summary(value, sdate):
    df_sysequ = get_sys_equity()
    latest_index = dt.datetime.strftime(df_sysequ[value].index[-1], format='%Y-%m-%d')
    last_value = df_sysequ[value].iloc[-1]
    last_value_rank = funs.percentilerank(df_sysequ.loc[sdate:df_sysequ[value].index[-2], value], last_value)
    return """Latest update {:s}, score: {:.2f}, rank: {:.2f}.
            """.format(latest_index, last_value, last_value_rank)

@app.callback(
    Output('sysequ-chart', 'figure'),
    Input('sysequ-dropdown', 'value'),
    Input('sysequ-radio', 'value'))
def display_chart(value, sdate):
    df_sysequ = get_sys_equity()
    df1 = df_sysequ.loc[sdate:, value]
    fig = px.line(df1)
    fig.update_layout(
        title_text="Systematic Equity Allocation - " + value,
        template="seaborn",
        showlegend=False,
        # dragmode='pan',
        # xaxis=dict(rangeslider=dict(visible=True), type="date")
    )
    return fig

# Equity sentiment
@app.callback(
    Output('display-senti-performance', 'children'),
    Input('senti-dropdown', 'value'),
    Input('senti-radio', 'value'))
def display_summary(value, sdate):
    df_senti = get_equity_senti()
    latest_index = dt.datetime.strftime(df_senti[value + '_sentiment'].index[-1], format='%Y-%m-%d')
    last_value = df_senti[value + '_sentiment'].iloc[-1]
    last_value_rank = funs.percentilerank(df_senti.loc[sdate:df_senti[value + '_sentiment'].index[-2], value + '_sentiment'], last_value)
    return """Latest update {:s}, sentiment: {:.2f}, rank: {:.2f}.
            """.format(latest_index, last_value, last_value_rank)

@app.callback(
    Output('senti-chart', 'figure'),
    Input('senti-dropdown', 'value'),
    Input('senti-radio', 'value'))
def display_chart(value, sdate):
    df_senti = get_equity_senti()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(y=df_senti.loc[sdate:, value+'_price'], x=df_senti.loc[sdate:, value+'_price'].index, name="Price"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(y=df_senti.loc[sdate:, value+'_sentiment'], x=df_senti.loc[sdate:, value+'_price'].index, name="Sentiment"),
        secondary_y=True,
    )

    fig.update_layout(
        title_text="Equity Sentiment - " + value,
        template="seaborn",
        showlegend=True,
        # dragmode='pan',
        # xaxis=dict(rangeslider=dict(visible=True), type="date")
    )

    fig.update_yaxes(title_text="<b>Price</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Sentiment</b>", secondary_y=True)
    return fig

# ETF
@app.callback(
    Output('display-etf-performance', 'children'),
    Input('etf-dropdown', 'value'),
    Input('etf-radio', 'value'))
def display_summary(value, sdate):
    df_etf = get_etf()
    latest_index = dt.datetime.strftime(df_etf[value].index[-1], format='%Y-%m-%d')
    flow_30d = df_etf[value].rolling(30).sum()
    flow_3m = df_etf[value].rolling(65).sum()
    flow_6m = df_etf[value].rolling(130).sum()
    last_value_30d = flow_30d.iloc[-1]
    last_value_rank_30d = funs.percentilerank(flow_30d.loc[sdate:flow_30d.index[-2]], last_value_30d)
    last_value_3m = flow_3m.iloc[-1]
    last_value_rank_3m = funs.percentilerank(flow_3m.loc[sdate:flow_3m.index[-2]], last_value_3m)
    last_value_6m = flow_6m.iloc[-1]
    last_value_rank_6m = funs.percentilerank(flow_6m.loc[sdate:flow_6m.index[-2]], last_value_6m)
    if value.lower() == 'gold':
        return """Latest update {:s}, 30d flow: {:.1f}k troy ounce, rank: {:.2f}; 3m flow: {:.1f}k troy ounce, rank: {:.2f}; 3m flow: {:.1f}k troy ounce, rank: {:.2f}.
                        """.format(latest_index, last_value_30d, last_value_rank_30d, last_value_3m, last_value_rank_3m,
                                   last_value_6m, last_value_rank_6m)
    else:
        return """Latest update {:s}, 30d flow: ${:.1f}b, rank: {:.2f}; 3m flow: ${:.1f}b, rank: {:.2f}; 3m flow: ${:.1f}b, rank: {:.2f}.
                """.format(latest_index, last_value_30d, last_value_rank_30d, last_value_3m, last_value_rank_3m, last_value_6m, last_value_rank_6m)

@app.callback(
    Output('etf-chart', 'figure'),
    Input('etf-dropdown', 'value'),
    Input('etf-radio', 'value'))
def display_chart(value, sdate):
    df_etf = get_etf()
    flow_30d = df_etf[value].rolling(30).sum()
    flow_3m = df_etf[value].rolling(65).sum()
    flow_6m = df_etf[value].rolling(130).sum()
    flow = pd.concat([flow_30d, flow_3m, flow_6m], axis=1)
    flow.columns = ['30d', '3m', '6m']
    df1 = flow.loc[sdate:, :]
    fig = px.line(df1)
    fig.update_layout(
        title_text=value + " flow",
        template="seaborn",
        showlegend=True,
        # dragmode='pan',
        # xaxis=dict(rangeslider=dict(visible=True), type="date")
    )
    return fig


