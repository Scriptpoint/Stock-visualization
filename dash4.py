import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas_datareader.data as web
import datetime

import yfinance as yf
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate


#time of data measurement
start= datetime.datetime(2020,1,1)
end=datetime.datetime(2021,12,31)
def get_data(ticker):
    df = yf.download(ticker)
    #to put data in columns
    df.reset_index(inplace=True)
    df=df[["Date","Close"]]
    print(df)
    return df

#build graph
get_data("AAPL")
def build_graphticker(df):
    return px.line(x=df["Date"],y=df["Close"])


#pull stock info from stooq.com
df=web.DataReader(['AMZN','GOOGL','FB','TWTR.US','MSFT.US','TTST.UK'],'stooq',start=start,end=end)
df=df.stack().reset_index()
df.to_csv("mystocks.csv",index=False)
print(df[:15])

app= dash.Dash(external_stylesheets=[dbc.themes.MINTY],
               #to make app runnable for mobile
               meta_tags=[{'name':'viewport', 'content':'width=device-width, initial-scale=1.0'}]
               )
#layoutS
app.layout=dbc.Container([
 dbc.Row(
        dbc.Col(html.H1("Stock Market Dashboard",
                        className='text-center text-primary mb-4'),
                width=12)
    ),

    dbc.Row([

        dbc.Col([
            dcc.Dropdown(id='my-dpdn', multi=False, value='AMZN',
                         options=[{'label':x, 'value':x}
                                  for x in sorted(df['Symbols'].unique())],
                         ),
            dcc.Graph(id='line-fig', figure={})
        ], width={'size':5, 'offset':1, 'order':1},
           xs=12, sm=12, md=12, lg=5, xl=5
        ),

        dbc.Col([
            dcc.Dropdown(id='my-dpdn2', multi=True, value=['PFE','BNTX'],
                         options=[{'label':x, 'value':x}
                                  for x in sorted(df['Symbols'].unique())],
                         ),
            dcc.Graph(id='line-fig2', figure={})
        ], width={'size':5, 'offset':0, 'order':2},
           xs=12, sm=12, md=12, lg=5, xl=5
        ),

    ], no_gutters=True, justify='around'),  # other prop:start,center,end,between,around

    dbc.Row([
        dbc.Col([
            html.P("Select Company Stock:",
                   style={"textDecoration": "underline"}),
            dcc.Checklist(id='my-checklist', value=['FB', 'GOOGL', 'AMZN'],
                          options=[{'label':x, 'value':x}
                                   for x in sorted(df['Symbols'].unique())],
                          labelClassName="mr-3"),
            dcc.Graph(id='my-hist', figure={}),
        ], width={'size':5, 'offset':1},
           xs=12, sm=12, md=12, lg=5, xl=5
        ),

        dbc.Col([
        dcc.Dropdown(id="dropdown",
        options=[
        {"label":"Beyond meat","value":"BYND"},
        {"label":"Moderna","value":"MRNA"},
        {"label":"Pfizer","value":"PFE"},
        ]),
           dcc.Graph(id="graph")
        ], width={'size':5, 'offset':1},
           xs=12, sm=12, md=12, lg=5, xl=5
        )
    ], no_gutters=True, justify='around',align="center")  # other prop: start, center, end

], fluid=True)


# Line chart - Single
@app.callback(
    Output('line-fig', 'figure'),
    Input('my-dpdn', 'value')
)
def build_graph(stock_select):
    dff= df[df['Symbols']==stock_select]
    figln = px.line(dff, x='Date', y='High')
    return figln


# Line chart - multiple
@app.callback(
    Output('line-fig2', 'figure'),
    Input('my-dpdn2', 'value')
)
def build_graph(stock_select):
    dff = df[df['Symbols'].isin(stock_select)]
    figln2 = px.line(dff, x='Date', y='Open', color='Symbols')
    return figln2


# Histogram
@app.callback(
    Output('my-hist', 'figure'),
    Input('my-checklist', 'value')
)
def build_graph(stock_slctd):
    dff = df[df['Symbols'].isin(stock_slctd)]
    dff = dff[dff['Date']=='2020-12-03']
    fighist = px.histogram(dff, x='Symbols', y='Close')
    return fighist
@app.callback(
    [Output("graph","figure")],
    [Input("dropdown","value")]
)
def my_dash(v):
    if v == None:
        raise PreventUpdate
    df = get_data(v)
    figure = build_graphticker(df)
    return [figure]

if __name__=='__main__':
    app.run_server(debug=True, port=8000)