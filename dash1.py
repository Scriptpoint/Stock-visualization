import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px

dashboard = dash.Dash()
#plotly graph to be used in dashboard
fig = px.line(x=[0,1,2],y=[2,3,4])

dashboard.layout = html.Div([
    #dropdown
    dcc.Dropdown(id="my_dropdown",
                 options=[
                     #expecting a dictionary
                     {"label":"France", "value":"France"},
                     {"label":"England", "value":"England"},
                     {"label":"Portugal", "value":"Portugal"},
                 ],
                 multi = True,
                 placeholder="Pick ur fav nation"),


    #radio item
    dcc.RadioItems(
        id="Radio",
        options=[
                      #expecting a dictionary
                     {"label":"France", "value":"France"},
                     {"label":"England", "value":"England"},
                     {"label":"Portugal", "value":"Portugal"},
        ]
    ),
    #graph
   dcc.Graph(figure=fig)


])
dashboard.run_server(debug=True)