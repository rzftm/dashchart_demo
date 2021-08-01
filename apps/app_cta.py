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


# CTA performance
def get_cta_data():
    data_path = folder_path + "trend_performance.csv"
    df = funs.read_csv(data_path, 'Unnamed: 0')
    df.columns = ['TFA','TFV','TFT','TCR1','TCR2','TEC','TBB','RF','RE']
    df['Total'] = df[['TFA','TFV','TFT','TCR1','TCR2','TEC','RF','RE']].sum(axis=1)
    df['FX'] = df[['TFA','TFV','TFT','RF','RE']].sum(axis=1)
    df['Commodity'] = df[['TCR1','TCR2']].sum(axis=1)
    df = df[['Total','FX','Commodity','TFA','TFV','TFT','TCR1','TCR2','TEC','TBB','RF','RE']]
    df.index.name = 'date'
    return df

def get_model_performance():
    # Trend model 3m performance
    sg_path = folder_path + 'sg_trend.csv'
    df_sg = funs.read_csv(sg_path, 'date')
    df_sg.columns = ['SG_3m_pct', 'SG_3m_sharpe']
    t1_path = folder_path + 'trend_pnl1.csv'
    df_t1 = funs.read_csv(t1_path, 'Date')
    df_t1.columns = ['T1_3m_pct', 'T1_3m_sharpe']
    t2_path = folder_path + 'trend_pnl2.csv'
    df_t2 = funs.read_csv(t2_path, 'Date')
    df_t2.columns = ['T2_3m_pct', 'T2_3m_sharpe']
    df_trend = pd.concat([df_sg, df_t1, df_t2], axis=1)
    df_trend.index.name = 'date'
    return df_trend

def get_model_exposure():
    # Trend model exposure
    exp1_path = folder_path + 'Trend_oppo_filter_exposure.csv'
    df_exp1 = funs.read_csv(exp1_path)
    df_exp1.columns = ['T1_USD', 'T1_EUR', 'T1_GBP', 'T1_JPY', 'T1_EMFX', 'T1_FI', 'T1_DMEquity', 'T1_EMEquity', 'T1_COMMODITY', 'T1_AGS']
    exp2_path = folder_path + 'Trend_no_filter_exposure.csv'
    df_exp2 = funs.read_csv(exp2_path)
    df_exp2.columns = ['T2_USD', 'T2_EUR', 'T2_GBP', 'T2_JPY', 'T2_EMFX', 'T2_FI', 'T2_DMEquity', 'T2_EMEquity', 'T2_COMMODITY', 'T2_AGS']
    df_exp = pd.concat([df_exp1, df_exp2], axis=1)
    df_exp.index.name = 'date'
    return df_exp

def get_cta_position():
    # CTA positioning
    cta_path = folder_path + 'cta_agg_position.csv'
    df_cta = funs.read_csv(cta_path)
    df_cta.index.name = 'date'
    return df_cta


df = get_cta_data()
df_trend = get_model_performance()
df_exp = get_model_exposure()
df_cta = get_cta_position()


layout = html.Div([

    # CTA performance
    html.Div([
        html.H3(children='CTA performance', style={'font-size': '1.2em'}),

        html.Div(children=[
            html.Label(["Choose a model..."], style={"font-style": "italic"}),
            dcc.Dropdown(
                id='cta-dropdown',
                options=[
                        {'label': 'Model - {}'.format(i), 'value': i} for i in df.columns
                    ],
                value='Total'
                )],
            style={"width": "45%",'display': 'inline-block'},
            ),

        html.Div(children=[
            html.Label(["Choose start time..."], style={"font-style": "italic"}),
            dcc.RadioItems(
                id='cta-radio',
                options=[
                    {'label': 'From 2000', 'value': dt.datetime(2000,1,1)},
                    {'label': 'From 2010', 'value': dt.datetime(2010,1,1)},
                    {'label': 'YTD', 'value': dt.datetime(dt.datetime.now().year,1,1)}
                    ],
                value=dt.datetime(dt.datetime.now().year,1,1),
                labelStyle={'display': 'inline-block', 'margin-right': 10}
                )],
            style={"width": "45%",'float': 'right','margin': 'auto'},
            ),

        html.Br(),
        html.Br(),
        html.Div(id='display-cta-performance', style={"font-weight": "bold"},),
        dcc.Graph(id='cta-chart'),
    ]),

    # Trend model 3m performance
    html.Div([
        html.H3(children='Trend model 3m performance', style={'font-size': '1.2em'}),

        html.Div(children=[
            html.Label(["Choose a model..."], style={"font-style": "italic"}),
            dcc.Dropdown(
                id='tpnl-dropdown',
                options=[
                    {'label': 'Model - {}'.format(i), 'value': i} for i in ['SG','T1','T2']
                ],
                value='T2'
            )],
            style={"width": "45%", 'display': 'inline-block'},
        ),

        html.Div(children=[
            html.Label(["Choose start time..."], style={"font-style": "italic"}),
            dcc.RadioItems(
                id='tpnl-radio',
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
        html.Div(id='display-tpnl-performance', style={"font-weight": "bold"}, ),
        dcc.Graph(id='tpnl-chart'),
    ]),

    # Trend model exposure
    html.Div([
        html.H3(children='Trend model exposure', style={'font-size': '1.2em'}),

        html.Div(children=[
            html.Label(["Choose an asset class..."], style={"font-style": "italic"}),
            dcc.Dropdown(
                id='texpo-dropdown',
                options=[
                    {'label': 'Asset class - {}'.format(i), 'value': i} for i in ['USD','EUR','GBP', 'JPY', 'EMFX', 'FI', 'DMEquity', 'EMEquity', 'COMMODITY', 'AGS']
                ],
                value='USD'
            )],
            style={"width": "45%", 'display': 'inline-block'},
        ),

        html.Div(children=[
            html.Label(["Choose start time..."], style={"font-style": "italic"}),
            dcc.RadioItems(
                id='texpo-radio',
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
        html.Div(id='display-texpo-performance', style={"font-weight": "bold"}, ),
        dcc.Graph(id='texpo-chart'),
    ]),

    # CTA positioning
    html.Div([
        html.H3(children='CTA positioning', style={'font-size': '1.2em'}),

        html.Div(children=[
            html.Label(["Choose an asset class..."], style={"font-style": "italic"}),
            dcc.Dropdown(
                id='ctapos-dropdown',
                options=[
                    {'label': 'Asset class - {}'.format(i), 'value': i} for i in df_cta.columns
                ],
                value='USD'
            )],
            style={"width": "45%", 'display': 'inline-block'},
        ),

        html.Div(children=[
            html.Label(["Choose start time..."], style={"font-style": "italic"}),
            dcc.RadioItems(
                id='ctapos-radio',
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
        html.Div(id='display-ctapos-performance', style={"font-weight": "bold"}, ),
        dcc.Graph(id='ctapos-chart'),
    ]),
])


# CTA performance
@app.callback(
    Output('display-cta-performance', 'children'),
    Input('cta-dropdown', 'value'),
    Input('cta-radio', 'value'))
def display_summary(model, sdate):
    df = get_cta_data()
    ann_rtn, vol, sharpe, max_dd, calmar = funs.performance_summary(df.loc[sdate:, model])[:5]
    return """Annual return {:,.0f}, Vol {:,.0f}, Sharpe ratio {:.2f}, Max drawdown {:,.0f}, Calmar {:.2f}
            """.format(ann_rtn, vol, sharpe, max_dd, calmar)

@app.callback(
    Output('cta-chart', 'figure'),
    Input('cta-dropdown', 'value'),
    Input('cta-radio', 'value'))
def display_chart(model, sdate):
    df = get_cta_data()
    cum_rtn, drawdown = funs.performance_summary(df.loc[sdate:, model])[5:]
    data = pd.concat([cum_rtn, drawdown], axis=1)
    data.columns = ['Cumulative return', 'Drawdown']

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(y=cum_rtn, x=cum_rtn.index, name="Cumulative return"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(y=drawdown, x=drawdown.index, name="Drawdown"),
        secondary_y=True,
    )

    fig.update_layout(
        title_text="Cumulative return and drawdown",
        template="seaborn",
        showlegend=False,
        # dragmode='pan',
        # xaxis=dict(rangeslider=dict(visible=True), type="date")
    )

    fig.update_yaxes(title_text="<b>Cumulative return</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Drawdown</b>", secondary_y=True)

    return fig

# Trend 3m performance
@app.callback(
    Output('display-tpnl-performance', 'children'),
    Input('tpnl-dropdown', 'value'),
    Input('tpnl-radio', 'value'))
def display_summary(value, sdate):
    df_trend = get_model_performance()
    latest_index = dt.datetime.strftime(df_trend[value+'_3m_pct'].index[-1], format='%Y-%m-%d')
    last_value = df_trend[value+'_3m_pct'].iloc[-1]
    last_value_rank = funs.percentilerank(df_trend.loc[sdate:df_trend[value+'_3m_pct'].index[-2], value+'_3m_pct'], last_value)
    last_sharpe = df_trend[value+'_3m_sharpe'].iloc[-1]
    last_sharpe_rank = funs.percentilerank(df_trend.loc[sdate:df_trend[value+'_3m_sharpe'].index[-2], value+'_3m_sharpe'], last_sharpe)
    return """Latest update {:s}, 3m pnl: {:.2f}, rank: {:.2f}, 3m sharpe: {:.2f}, rank {:.2f}.
            """.format(latest_index, last_value, last_value_rank, last_sharpe, last_sharpe_rank)

@app.callback(
    Output('tpnl-chart', 'figure'),
    Input('tpnl-dropdown', 'value'),
    Input('tpnl-radio', 'value'))
def display_chart(value, sdate):
    df_trend = get_model_performance()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(y=df_trend.loc[sdate:, value+'_3m_pct'], x=df_trend.loc[sdate:, value+'_3m_pct'].index, name="3m return"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(y=df_trend.loc[sdate:, value+'_3m_sharpe'], x=df_trend.loc[sdate:, value+'_3m_pct'].index, name="3m sharpe"),
        secondary_y=True,
    )

    fig.update_layout(
        title_text="Trend model 3m performance - " + value,
        template="seaborn",
        showlegend=True,
        # dragmode='pan',
        # xaxis=dict(rangeslider=dict(visible=True), type="date")
    )

    fig.update_yaxes(title_text="<b>Percentage return</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Sharpe ratio</b>", secondary_y=True)
    return fig

# Trend model exposure
@app.callback(
    Output('display-texpo-performance', 'children'),
    Input('texpo-dropdown', 'value'),
    Input('texpo-radio', 'value'))
def display_summary(value, sdate):
    df_exp = get_model_exposure()
    latest_index = dt.datetime.strftime(df_exp['T1_'+value].index[-1], format='%Y-%m-%d')
    last_value_t1 = df_exp['T1_' + value].iloc[-1]
    last_value_rank_t1 = funs.percentilerank(df_exp.loc[sdate:df_exp['T1_'+value].index[-2], 'T1_'+value], last_value_t1)
    last_value_t2 = df_exp['T2_' + value].iloc[-1]
    last_value_rank_t2 = funs.percentilerank(df_exp.loc[sdate:df_exp['T2_' + value].index[-2], 'T2_' + value], last_value_t2)
    return """Latest update {:s}, Trend model 1 exposure: ${:.1f}m, rank: {:.2f} Trend model 2 exposure: ${:.1f}m, rank: {:.2f}.
            """.format(latest_index, last_value_t1, last_value_rank_t1, last_value_t2, last_value_rank_t2)

@app.callback(
    Output('texpo-chart', 'figure'),
    Input('texpo-dropdown', 'value'),
    Input('texpo-radio', 'value'))
def display_chart(value, sdate):
    df_exp = get_model_exposure()
    df1 = df_exp.loc[sdate:, ['T1_'+value,'T2_'+value]]
    fig = px.line(df1)
    fig.update_layout(
        title_text="Trend model exposure to " + value,
        template="seaborn",
        showlegend=True,
        # dragmode='pan',
        # xaxis=dict(rangeslider=dict(visible=True), type="date")
    )
    return fig

# CTA position
@app.callback(
    Output('display-ctapos-performance', 'children'),
    Input('ctapos-dropdown', 'value'),
    Input('ctapos-radio', 'value'))
def display_summary(value, sdate):
    df_cta = get_cta_position()
    latest_index = dt.datetime.strftime(df_cta[value].index[-1], format='%Y-%m-%d')
    last_value = df_cta[value].iloc[-1]
    last_value_rank = funs.percentilerank(df_cta.loc[sdate:df_cta[value].index[-2], value], last_value)
    return """Latest update {:s}, CTA positioning: {:.2f}, rank: {:.2f}.
            """.format(latest_index, last_value, last_value_rank)

@app.callback(
    Output('ctapos-chart', 'figure'),
    Input('ctapos-dropdown', 'value'),
    Input('ctapos-radio', 'value'))
def display_chart(value, sdate):
    df_cta = get_cta_position()
    df1 = df_cta.loc[sdate:, value]
    fig = px.line(df1)
    fig.update_layout(
        title_text="CTA positioning - " + value,
        template="seaborn",
        showlegend=False,
        # dragmode='pan',
        # xaxis=dict(rangeslider=dict(visible=True), type="date")
    )
    return fig

