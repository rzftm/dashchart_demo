import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd
import datetime as dt

from app import app, folder_path
import funs


def get_com_carry():
    # Commodity carry
    df_carry = funs.read_csv(folder_path + 'COM_CARRY.csv')
    df_carry_vol = funs.read_csv(folder_path + 'COM_CARRY_VOL.csv')
    df_carry.index.name = 'date'
    df_carry_vol.index.name = 'date'
    return df_carry, df_carry_vol

def get_com_forecast():
    # Commodity forecast
    df_forecast = funs.read_csv(folder_path + 'COM_FORECAST.csv')
    df_forecast_vol = funs.read_csv(folder_path + 'COM_FORECAST_VOL.csv')
    df_forecast.index.name = 'date'
    df_forecast_vol.index.name = 'date'
    return df_forecast, df_forecast_vol

def get_com_inv():
    # Commodity inventory
    df_inv = funs.read_csv(folder_path + 'COM_INV.csv')
    df_inv_rank = funs.read_csv(folder_path + 'COM_INV_rank.csv')
    df_inv.index.name = 'date'
    df_inv_rank.index.name = 'date'
    df_inv_base = df_inv[['HG1','ALUMINIUM','NICKEL','ZINC','LEAD']]
    df_inv_energy = df_inv[['CL1','XB1','HO1','NG1']]
    return df_inv_base, df_inv_energy, df_inv_rank

df_carry, df_carry_vol = get_com_carry()
df_forecast, df_forecast_vol = get_com_forecast()
df_inv_base, df_inv_energy, df_inv_rank = get_com_inv()

layout = html.Div([

    # Commodity carry
    html.Div([
        html.H3(children='Carry', style={'font-size': '1.2em'}),

        html.Div(children=[
            html.Label(["Choose an instrument..."], style={"font-style": "italic"}),
            dcc.Dropdown(
                id='comcarry-dropdown',
                options=[
                        {'label': '{}'.format(i), 'value': i} for i in df_carry.columns
                    ],
                value='CL1'
                )],
            style={"width": "45%",'display': 'inline-block'},
            ),

        html.Div(children=[
            html.Label(["Choose start time..."], style={"font-style": "italic"}),
            dcc.RadioItems(
                id='comcarry-radio',
                options=[
                    {'label': 'Full', 'value': dt.datetime(2000, 1, 1)},
                    {'label': 'From 2010', 'value': dt.datetime(2010, 1, 1)},
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
        html.Div(id='display-comcarry-performance', style={"font-weight": "bold"},),
        dcc.Graph(id='comcarry-chart'),
    ]),

    # Commodity forecast
    html.Div([
        html.H3(children='Forecast', style={'font-size': '1.2em'}),

        html.Div(children=[
            html.Label(["Choose an instrument..."], style={"font-style": "italic"}),
            dcc.Dropdown(
                id='comforecast-dropdown',
                options=[
                    {'label': '{}'.format(i), 'value': i} for i in df_forecast.columns
                ],
                value='CL1'
            )],
            style={"width": "45%", 'display': 'inline-block'},
        ),

        html.Div(children=[
            html.Label(["Choose start time..."], style={"font-style": "italic"}),
            dcc.RadioItems(
                id='comforecast-radio',
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
        html.Div(id='display-comforecast-performance', style={"font-weight": "bold"}, ),
        dcc.Graph(id='comforecast-chart'),
    ]),

    # Base metal inventory
    html.Div([
        html.H3(children='Base metal Inventory', style={'font-size': '1.2em'}),

        html.Div(children=[
            html.Label(["Choose an instrument..."], style={"font-style": "italic"}),
            dcc.Dropdown(
                id='inventory-dropdown',
                options=[
                    {'label': '{}'.format(i), 'value': i} for i in df_inv_base.columns
                ],
                value='HG1'
            )],
            style={"width": "45%", 'display': 'inline-block'},
        ),

        html.Div(children=[
            html.Label(["Choose start time..."], style={"font-style": "italic"}),
            dcc.RadioItems(
                id='inventory-radio',
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
        html.Div(id='display-inventory-performance', style={"font-weight": "bold"}, ),
        dcc.Graph(id='inventory-chart'),
    ]),

    # Energy inventory
    html.Div([
        html.H3(children='Energy Inventory', style={'font-size': '1.2em'}),

        html.Div(children=[
            html.Label(["Choose an instrument..."], style={"font-style": "italic"}),
            dcc.Dropdown(
                id='energy-dropdown',
                options=[
                    {'label': '{}'.format(i), 'value': i} for i in df_inv_energy.columns
                ],
                value='CL1'
            )],
            style={"width": "45%", 'display': 'inline-block'},
        ),

        html.Div(children=[
            html.Label(["Choose start time..."], style={"font-style": "italic"}),
            dcc.RadioItems(
                id='energy-radio',
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
        html.Div(id='display-energy-performance', style={"font-weight": "bold"}, ),
        dcc.Graph(id='energy-chart'),
    ]),

])

# Commodity carry
@app.callback(
    Output('display-comcarry-performance', 'children'),
    Input('comcarry-dropdown', 'value'),
    Input('comcarry-radio', 'value'))
def display_summary(value, sdate):
    df_carry, df_carry_vol = get_com_carry()
    latest_index = dt.datetime.strftime(df_carry[value].index[-1], format='%Y-%m-%d')
    last_carry = df_carry.iloc[-1, :].values
    backward = df_carry_vol.columns[last_carry.argsort()[-5:][::-1]]
    contan = df_carry_vol.columns[last_carry.argsort()[:5]]
    last_value = df_carry[value].iloc[-1]
    last_value_rank = funs.percentilerank(df_carry.loc[sdate:df_carry[value].index[-2], value], last_value)
    return dcc.Markdown("""
        Latest update {:s}, top 5 backwardation (vol adjusted): {:s}, top 5 contango {:s}.
        Current annualized carry: {:.2f}, vol adjust carry {:.2f}.
                """.format(latest_index, ','.join(backward), ','.join(contan), last_value, last_value_rank), style={"white-space": "pre", "font-weight": "bold"})

@app.callback(
    Output('comcarry-chart', 'figure'),
    Input('comcarry-dropdown', 'value'),
    Input('comcarry-radio', 'value'))
def display_chart(value, sdate):
    df_carry, df_carry_vol = get_com_carry()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(y=df_carry.loc[sdate:, value], x=df_carry.loc[sdate:, value].index, name="Carry"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(y=df_carry_vol.loc[sdate:, value], x=df_carry.loc[sdate:, value].index, name="Carry vol adj"),
        secondary_y=True,
    )

    fig.update_layout(
        title_text="Commodity front spread (front-2nd contract) - " + value,
        template="seaborn",
        showlegend=True,
        # dragmode='pan',
        # xaxis=dict(rangeslider=dict(visible=True), type="date")
    )

    fig.update_yaxes(title_text="<b>Carry</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Carry vol adj</b>", secondary_y=True)
    return fig

# Commodity forecast
@app.callback(
    Output('display-comforecast-performance', 'children'),
    Input('comforecast-dropdown', 'value'),
    Input('comforecast-radio', 'value'))
def display_summary(value, sdate):
    df_forecast, df_forecast_vol = get_com_forecast()
    latest_index = dt.datetime.strftime(df_forecast[value].index[-1], format='%Y-%m-%d')
    last_forecast = df_forecast_vol.iloc[-1, :].values
    overvalue = df_forecast_vol.columns[last_forecast.argsort()[-5:][::-1]]
    undervalue = df_forecast_vol.columns[last_forecast.argsort()[:5]]
    last_value = df_forecast[value].iloc[-1]
    last_value_rank = funs.percentilerank(df_forecast.loc[sdate:df_forecast[value].index[-2], value], last_value)
    return dcc.Markdown("""
        Latest update {:s}, top 5 overvalued (vol adjusted): {:s}, top 5 undervalued {:s}.
        Current annualized value: {:.2f}, rank {:.2f}.
            """.format(latest_index, ','.join(overvalue), ','.join(undervalue), last_value, last_value_rank), style={"white-space": "pre", "font-weight": "bold"})

@app.callback(
    Output('comforecast-chart', 'figure'),
    Input('comforecast-dropdown', 'value'),
    Input('comforecast-radio', 'value'))
def display_chart(value, sdate):
    df_forecast, df_forecast_vol = get_com_forecast()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(y=df_forecast.loc[sdate:, value], x=df_forecast.loc[sdate:, value].index, name="Value"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(y=df_forecast_vol.loc[sdate:, value], x=df_forecast_vol.loc[sdate:, value].index, name="Value vol adj"),
        secondary_y=True,
    )

    fig.update_layout(
        title_text="Commodity value (price-forecast) - " + value,
        template="seaborn",
        showlegend=True,
        # dragmode='pan',
        # xaxis=dict(rangeslider=dict(visible=True), type="date")
    )

    fig.update_yaxes(title_text="<b>Relative value</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Value vol adj</b>", secondary_y=True)
    return fig

# Base metal inventory
@app.callback(
    Output('display-inventory-performance', 'children'),
    Input('inventory-dropdown', 'value'),
    Input('inventory-radio', 'value'))
def display_summary(value, sdate):
    df_inv_base, df_inv_energy, df_inv_rank = get_com_inv()
    latest_index = dt.datetime.strftime(df_inv_base[value].index[-1], format='%Y-%m-%d')
    last_rank = df_inv_rank[df_inv_base.columns].iloc[-1].values
    highinv = df_inv_base.columns[last_rank.argsort()[-2:][::-1]]
    lowinv = df_inv_base.columns[last_rank.argsort()[:2]]
    last_value = df_inv_base[value].iloc[-1]
    last_value_rank = funs.percentilerank(df_inv_base.loc[sdate:df_inv_base[value].index[-2], value], last_value)
    return dcc.Markdown("""
        Latest update {:s}, two highest invenotry (vol adjusted): {:s}, two lowest inventory {:s}. 
        Current inventory: {:.2f}, rank {:.2f}.
                """.format(latest_index, ','.join(highinv), ','.join(lowinv), last_value, last_value_rank), style={"white-space": "pre", "font-weight": "bold"})

@app.callback(
    Output('inventory-chart', 'figure'),
    Input('inventory-dropdown', 'value'),
    Input('inventory-radio', 'value'))
def display_chart(value, sdate):
    df_inv_base, df_inv_energy, df_inv_rank = get_com_inv()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(y=df_inv_base.loc[sdate:, value], x=df_inv_base.loc[sdate:, value].index, name="Inventory"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(y=df_inv_rank.loc[sdate:, value], x=df_inv_base.loc[sdate:, value].index, name="Inventory rank"),
        secondary_y=True,
    )

    fig.update_layout(
        title_text="Base metal inventory - " + value,
        template="seaborn",
        showlegend=True,
        # dragmode='pan',
        # xaxis=dict(rangeslider=dict(visible=True), type="date")
    )

    fig.update_yaxes(title_text="<b>Inventory</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Inventory rank</b>", secondary_y=True)
    return fig


# Energy inventory
@app.callback(
    Output('display-energy-performance', 'children'),
    Input('energy-dropdown', 'value'),
    Input('energy-radio', 'value'))
def display_summary(value, sdate):
    df_inv_base, df_inv_energy, df_inv_rank = get_com_inv()
    latest_index = dt.datetime.strftime(df_inv_energy[value].index[-1], format='%Y-%m-%d')
    last_rank = df_inv_rank[df_inv_energy.columns].iloc[-1].values
    highinv = df_inv_energy.columns[last_rank.argsort()[-2:][::-1]]
    lowinv = df_inv_energy.columns[last_rank.argsort()[:2]]
    last_value = df_inv_energy[value].iloc[-1]
    last_value_rank = funs.percentilerank(df_inv_energy.loc[sdate:df_inv_energy[value].index[-2], value], last_value)
    return dcc.Markdown("""
        Latest update {:s}, two highest invenotry (vol adjusted): {:s}, two lowest inventory {:s}. 
        Current inventory: {:.2f}, rank {:.2f}.
                """.format(latest_index, ','.join(highinv), ','.join(lowinv), last_value, last_value_rank), style={"white-space": "pre", "font-weight": "bold"})

@app.callback(
    Output('energy-chart', 'figure'),
    Input('energy-dropdown', 'value'),
    Input('energy-radio', 'value'))
def display_chart(value, sdate):
    df_inv_base, df_inv_energy, df_inv_rank = get_com_inv()
    df1 = df_inv_energy.loc[sdate:, value]
    df = pd.DataFrame()
    for yr in range(df1.index[0].year, df1.index[-1].year+1):
        df_temp = df1.loc[df1.index.year == yr]
        df_temp.index = range(0, len(df_temp))
        df = pd.concat([df, df_temp], axis=1)
    df.columns = range(df1.index[0].year, df1.index[-1].year + 1)
    df.loc[:,range(df1.index[0].year, df1.index[-1].year)] = df.loc[:,range(df1.index[0].year, df1.index[-1].year)].fillna(method='ffill')
    avg = df.iloc[:, :-1].mean(axis=1)
    std = df.iloc[:, :-1].std(axis=1)
    df['average'] = avg
    df['+1 sd'] = avg + std
    df['-1 sd'] = avg - std

    fig = make_subplots(specs=[[{"secondary_y": False}]])
    fig.add_trace(
        go.Scatter(y=df[df1.index[-1].year], x=df.index, name="This year", line=dict(width=5))
    )

    fig.add_trace(
        go.Scatter(y=df[df1.index[-1].year-1], x=df.index, name="Last year")
    )

    fig.add_trace(
        go.Scatter(y=df['average'], x=df.index, name="Average", line=dict(color='black'))
    )

    fig.add_trace(
        go.Scatter(y=df['+1 sd'], x=df.index, name="+1 sd", line=dict(color='grey'))
    )

    fig.add_trace(
        go.Scatter(y=df['-1 sd'], x=df.index, name="-1 sd", line=dict(color='grey'))
    )

    fig.update_layout(
        title_text="Energy inventory - " + value,
        template="seaborn",
        showlegend=True,
        # dragmode='pan',
        # xaxis=dict(rangeslider=dict(visible=True), type="date")
    )

    fig.update_yaxes(title_text="<b>Inventory</b>", secondary_y=False)
    return fig