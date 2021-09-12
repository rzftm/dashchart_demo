
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import app_cta, app_ecocon, app_cftc, app_position, app_valuecom, app_correlation

server = app.server

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H3("Analysis Dashboard", className="display-4", style={'font-size': '1.6em'}),
        html.Hr(),
        # html.P(
        #     "Please click to see the latest chart and update", className="lead"
        # ),
        dbc.Nav(
            [
                dbc.NavLink("CTA model", href="/", active="exact"),
                dbc.NavLink("CFTC", href="/page_cftc", active="exact"),
                dbc.NavLink("Positioning", href="/page_position", active="exact"),
                dbc.NavLink("Economic Condition", href="/page_ecocon", active="exact"),
                dbc.NavLink("Valuation-Commodity", href="/page_valuecom", active="exact"),
                dbc.NavLink("Correlation", href="/page_correlation", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return app_cta.layout
    elif pathname == "/page_cftc":
        return app_cftc.layout
    elif pathname == "/page_position":
        return app_position.layout
    elif pathname == "/page_ecocon":
        return app_ecocon.layout
    elif pathname == "/page_valuecom":
        return app_valuecom.layout
    elif pathname == "/page_correlation":
        return app_correlation.layout

    # html.P("Oh cool, this is page 5!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(debug=True)