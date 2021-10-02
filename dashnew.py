#to use dashboard
import dash
#to put html in layout
import dash_html_components as html
from dash.dependencies import Input,Output
#for preventing none conditioned situations
from dash.exceptions import PreventUpdate



#initialize dash app in variable
app = dash.Dash()

#start app
app.layout= html.Div([
    html.H1("Title"),
    html.Button("Click Me", id="my_button"),
    html.Div(id="My Output")
])

#callbacks do work of javascript,n_clicks in none by default so there will be some error
@app.callback(
    [Output("My Output", "children")],
    [Input("my_button", "n_clicks")]
)
#function
def clicked_output(v):
    if v == None:
        raise PreventUpdate
    return [f"You clicked {v}times" ]

#start server
app.run_server(debug=True)