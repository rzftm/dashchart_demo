import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd
import datetime as dt

from app import app, folder_path
import funs


def get_senti_reg():
    # ES sentiment price regression
    file_path = folder_path + 'es_senti_kernal.csv'
    df_fin = funs.read_csv(file_path)
    df_fin.index.name = 'date'
    return df_fin

df_fin = get_senti_reg()

layout = html.Div([

    # CFTC financial futures
    html.Div([
        html.H3(children='Sentiment vs price', style={'font-size': '1.2em'}),

        html.Div(children=[
            html.Label(["Choose an instrument..."], style={"font-style": "italic"}),
            dcc.Dropdown(
                id='coressenti-dropdown',
                options=[
                        {'label': '{}'.format(i), 'value': i} for i in ['ES',]
                    ],
                value='ES'
                )],
            style={"width": "45%",'display': 'inline-block'},
            ),

        html.Div(children=[
            html.Label(["Choose start time..."], style={"font-style": "italic"}),
            dcc.RadioItems(
                id='coressenti-radio',
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
        html.Div(id='display-coressenti-performance', style={"font-weight": "bold"},),
        dcc.Graph(id='coressenti-chart'),
    ]),

])

# CFTC financial futures
@app.callback(
    Output('display-coressenti-performance', 'children'),
    Input('coressenti-dropdown', 'value'),
    Input('coressenti-radio', 'value'))
def display_summary(value, sdate):
    df_fin = get_senti_reg()
    latest_index = dt.datetime.strftime(df_fin.index[-1], format='%Y-%m-%d')
    last_value = df_fin['fit'].iloc[-1]
    last_senti = df_fin['senti'].iloc[-1]
    return """Latest update {:s}, sentiment: {:.2f}, expected return: {:.1%}.
            """.format(latest_index, last_senti, last_value)

@app.callback(
    Output('coressenti-chart', 'figure'),
    Input('coressenti-dropdown', 'value'),
    Input('coressenti-radio', 'value'))
def display_chart(value, sdate):
    df_fin = get_senti_reg()
    fig = make_subplots()
    fig.add_trace(
        go.Scatter(y=df_fin.loc[sdate:, 'price_change'], x=df_fin.loc[sdate:, 'senti'],
                   name="Actual", mode='markers'),
    )

    fig.add_trace(
        go.Scatter(y=df_fin.loc[sdate:, 'fit'], x=df_fin.loc[sdate:, 'senti'],
                   name="Fitted", mode='markers'),
    )

    fig.update_layout(
        title_text="Sentiment vs price - " + value,
        template="seaborn",
        showlegend=True,
        # dragmode='pan',
        # xaxis=dict(rangeslider=dict(visible=True), type="date")
    )

    fig.update_yaxes(title_text="<b>3weeks return in %</b>")
    fig.update_xaxes(title_text="<b>Sentiment</b>")
    return fig

