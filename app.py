
import dash
import dash_bootstrap_components as dbc

folder_path = "H:\\_CODE\\dashchart_demo\\data\\"
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server
