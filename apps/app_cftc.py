import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd
import datetime as dt

from app import app, folder_path
import funs

fin_list = ['ES', 'DM', 'TY']
fx_list = ['USD', 'EUR', 'GBP', 'JPY', 'AUD', 'NZD', 'CAD', 'CHF', 'EM', 'Riskon']
com_list = ['OIL', 'CL', 'CO', 'HG', 'GC', 'SI', 'C', 'S', 'SM', 'BO']

def get_cftc_fin():
    # CFTC financial futures
    df_fin = pd.DataFrame()
    for name in fin_list:
        file_path = folder_path + 'cftc_{:s}.csv'.format(name)
        df_temp = funs.read_csv(file_path, 'friday')
        df_fin[name + '_net_traders'] = df_temp['net_traders']
        df_fin[name + '_net_traders_oi'] = df_temp['net_trader_oi']
    df_fin.index.name = 'date'
    return df_fin

def get_cftc_fx():
    # CFTC FX futures
    df_fx = pd.DataFrame()
    for name in fx_list:
        file_path = folder_path + 'cftc_{:s}.csv'.format(name)
        df_temp = funs.read_csv(file_path, 'friday')
        df_fx[name + '_net_position'] = df_temp['net_position']
        df_fx[name + '_net_position_oi'] = df_temp['net_position_oi']
    df_fx.index.name = 'date'
    return df_fx

def get_cftc_com():
    # CFTC commodity futures
    df_com = pd.DataFrame()
    for name in com_list:
        file_path = folder_path + 'cftc_{:s}.csv'.format(name)
        df_temp = funs.read_csv(file_path, 'friday')
        df_com[name + '_net_position'] = df_temp['net_position']
        df_com[name + '_net_position_oi'] = df_temp['net_position_oi']
    df_com.index.name = 'date'
    return df_com

df_fin = get_cftc_fin()
df_fx = get_cftc_fx()
df_com = get_cftc_com()

layout = html.Div([

    # CFTC financial futures
    html.Div([
        html.H3(children='CFTC Financial futures', style={'font-size': '1.2em'}),

        html.Div(children=[
            html.Label(["Choose a model..."], style={"font-style": "italic"}),
            dcc.Dropdown(
                id='cftcfin-dropdown',
                options=[
                        {'label': '{}'.format(i), 'value': i} for i in fin_list
                    ],
                value='ES'
                )],
            style={"width": "45%",'display': 'inline-block'},
            ),

        html.Div(children=[
            html.Label(["Choose start time..."], style={"font-style": "italic"}),
            dcc.RadioItems(
                id='cftcfin-radio',
                options=[
                    {'label': 'Full', 'value': dt.datetime(2010, 1, 1)},
                    {'label': 'Last 5 years', 'value': dt.datetime(dt.datetime.now().year - 5, 1, 1)},
                    {'label': 'Last 3 years', 'value': dt.datetime(dt.datetime.now().year - 3, 1, 1)}
                ],
                value=dt.datetime(dt.datetime.now().year - 5, 1, 1),
                labelStyle={'display': 'inline-block', 'margin-right': 10}
                )],
            style={"width": "45%",'float': 'right','margin': 'auto'},
            ),

        html.Br(),
        html.Br(),
        html.Div(id='display-cftcfin-performance', style={"font-weight": "bold"},),
        dcc.Graph(id='cftcfin-chart'),
    ]),

    # CFTC FX futures
    html.Div([
        html.H3(children='CFTC FX futures', style={'font-size': '1.2em'}),

        html.Div(children=[
            html.Label(["Choose a model..."], style={"font-style": "italic"}),
            dcc.Dropdown(
                id='cftcfx-dropdown',
                options=[
                    {'label': '{}'.format(i), 'value': i} for i in fx_list
                ],
                value='USD'
            )],
            style={"width": "45%", 'display': 'inline-block'},
        ),

        html.Div(children=[
            html.Label(["Choose start time..."], style={"font-style": "italic"}),
            dcc.RadioItems(
                id='cftcfx-radio',
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
        html.Div(id='display-cftcfx-performance', style={"font-weight": "bold"}, ),
        dcc.Graph(id='cftcfx-chart'),
    ]),

    # CFTC commodity futures
    html.Div([
        html.H3(children='CFTC commodity futures', style={'font-size': '1.2em'}),

        html.Div(children=[
            html.Label(["Choose an asset class..."], style={"font-style": "italic"}),
            dcc.Dropdown(
                id='cftccom-dropdown',
                options=[
                    {'label': '{}'.format(i), 'value': i} for i in com_list
                ],
                value='OIL'
            )],
            style={"width": "45%", 'display': 'inline-block'},
        ),

        html.Div(children=[
            html.Label(["Choose start time..."], style={"font-style": "italic"}),
            dcc.RadioItems(
                id='cftccom-radio',
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
        html.Div(id='display-cftccom-performance', style={"font-weight": "bold"}, ),
        dcc.Graph(id='cftccom-chart'),
    ]),

])

# CFTC financial futures
@app.callback(
    Output('display-cftcfin-performance', 'children'),
    Input('cftcfin-dropdown', 'value'),
    Input('cftcfin-radio', 'value'))
def display_summary(value, sdate):
    df_fin = get_cftc_fin()
    latest_index = dt.datetime.strftime(df_fin[value + '_net_traders'].index[-1], format='%Y-%m-%d')
    last_value = df_fin[value + '_net_traders'].iloc[-1]
    last_value_rank = funs.percentilerank(df_fin.loc[sdate:df_fin[value + '_net_traders'].index[-2], value + '_net_traders'], last_value)
    last_pct = df_fin[value + '_net_traders_oi'].iloc[-1]
    last_pct_rank = funs.percentilerank(df_fin.loc[sdate:df_fin[value + '_net_traders_oi'].index[-2], value + '_net_traders_oi'], last_pct)
    return """Latest update {:s}, net traders: {:.2f}, rank: {:.2f}, net traders / total: {:.2f}, rank {:.2f}.
            """.format(latest_index, last_value, last_value_rank, last_pct, last_pct_rank)

@app.callback(
    Output('cftcfin-chart', 'figure'),
    Input('cftcfin-dropdown', 'value'),
    Input('cftcfin-radio', 'value'))
def display_chart(value, sdate):
    df_fin = get_cftc_fin()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(y=df_fin.loc[sdate:, value + '_net_traders'], x=df_fin.loc[sdate:, value + '_net_traders'].index,
                   name="Net traders"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(y=df_fin.loc[sdate:, value + '_net_traders_oi'], x=df_fin.loc[sdate:, value + '_net_traders_oi'].index,
                   name="Net traders/Total"),
        secondary_y=True,
    )

    fig.update_layout(
        title_text="CFTC financial futures AM/LM position - " + value,
        template="seaborn",
        showlegend=True,
        # dragmode='pan',
        # xaxis=dict(rangeslider=dict(visible=True), type="date")
    )

    fig.update_yaxes(title_text="<b>Net number of traders</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Percentage</b>", secondary_y=True)
    return fig

# CFTC FX futures
@app.callback(
    Output('display-cftcfx-performance', 'children'),
    Input('cftcfx-dropdown', 'value'),
    Input('cftcfx-radio', 'value'))
def display_summary(value, sdate):
    df_fx = get_cftc_fx()
    latest_index = dt.datetime.strftime(df_fx[value+'_net_position'].index[-1], format='%Y-%m-%d')
    last_value = df_fx[value+'_net_position'].iloc[-1]
    last_value_rank = funs.percentilerank(df_fx.loc[sdate:df_fx[value+'_net_position'].index[-2], value+'_net_position'], last_value)
    last_pct = df_fx[value+'_net_position_oi'].iloc[-1]
    last_pct_rank = funs.percentilerank(df_fx.loc[sdate:df_fx[value+'_net_position_oi'].index[-2], value+'_net_position_oi'], last_pct)
    return """Latest update {:s}, net traders: {:.2f}, rank: {:.2f}, net traders / total: {:.2f}, rank {:.2f}.
            """.format(latest_index, last_value, last_value_rank, last_pct, last_pct_rank)

@app.callback(
    Output('cftcfx-chart', 'figure'),
    Input('cftcfx-dropdown', 'value'),
    Input('cftcfx-radio', 'value'))
def display_chart(value, sdate):
    df_fx = get_cftc_fx()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(y=df_fx.loc[sdate:, value+'_net_position'], x=df_fx.loc[sdate:, value+'_net_position'].index, name="Net position"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(y=df_fx.loc[sdate:, value+'_net_position_oi'], x=df_fx.loc[sdate:, value+'_net_position_oi'].index, name="Net position/OI"),
        secondary_y=True,
    )

    fig.update_layout(
        title_text="CFTC FX futures non-commercial position - " + value,
        template="seaborn",
        showlegend=True,
        # dragmode='pan',
        # xaxis=dict(rangeslider=dict(visible=True), type="date")
    )

    fig.update_yaxes(title_text="<b>Net number of contracts</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Percentage</b>", secondary_y=True)
    return fig

# CFTC commodity futures
@app.callback(
    Output('display-cftccom-performance', 'children'),
    Input('cftccom-dropdown', 'value'),
    Input('cftccom-radio', 'value'))
def display_summary(value, sdate):
    df_com = get_cftc_com()
    latest_index = dt.datetime.strftime(df_com[value + '_net_position'].index[-1], format='%Y-%m-%d')
    last_value = df_com[value + '_net_position'].iloc[-1]
    last_value_rank = funs.percentilerank(df_com.loc[sdate:df_com[value + '_net_position'].index[-2], value + '_net_position'], last_value)
    last_pct = df_com[value + '_net_position_oi'].iloc[-1]
    last_pct_rank = funs.percentilerank(df_com.loc[sdate:df_com[value + '_net_position_oi'].index[-2], value + '_net_position_oi'], last_pct)
    return """Latest update {:s}, net traders: {:.2f}, rank: {:.2f}, net traders / total: {:.2f}, rank {:.2f}.
                """.format(latest_index, last_value, last_value_rank, last_pct, last_pct_rank)

@app.callback(
    Output('cftccom-chart', 'figure'),
    Input('cftccom-dropdown', 'value'),
    Input('cftccom-radio', 'value'))
def display_chart(value, sdate):
    df_com = get_cftc_com()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(y=df_com.loc[sdate:, value+'_net_position'], x=df_com.loc[sdate:, value+'_net_position'].index, name="Net position"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(y=df_com.loc[sdate:, value+'_net_position_oi'], x=df_com.loc[sdate:, value+'_net_position_oi'].index, name="Net position/OI"),
        secondary_y=True,
    )

    fig.update_layout(
        title_text="CFTC Commodity futures Managed Money position - " + value,
        template="seaborn",
        showlegend=True,
        # dragmode='pan',
        # xaxis=dict(rangeslider=dict(visible=True), type="date")
    )

    fig.update_yaxes(title_text="<b>Net number of contracts</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Percentage</b>", secondary_y=True)
    return fig


