#to use dashboard
import dash
#to put html in layout
import dash_html_components as html
import dash_core_components as dcc
#Download data from yahoo
import yfinance as yf
#building graph
import plotly.express as px
#adding bootstrap
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

#get data,ticker is identifier of each stock
def get_data(ticker):
    df = yf.download(ticker)
    #to put data in columns
    df.reset_index(inplace=True)
    df=df[["Date","Close"]]
    print(df)
    return df

#build graph
get_data("AAPL")
def build_graph(df):
    return px.line(x=df["Date"],y=df["Close"])

#dashboard
Dashboardapp= dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
Dashboardapp.layout = html.Div([
    dcc.Dropdown(id="dropdown",
        options=[
        {"label":"Beyond meat","value":"BYND"},
        {"label":"Moderna","value":"MRNA"},
        {"label":"Pfizer","value":"PFE"},
        ]),
    dcc.Graph(id="graph")
])
@Dashboardapp.callback(
    [Output("graph","figure")],
    [Input("dropdown","value")]
)
def my_dash(v):
    if v == None:
        raise PreventUpdate
    df = get_data(v)
    figure = build_graph(df)
    return [figure]
if __name__ == '__main__':
 Dashboardapp.run_server(debug=True)


