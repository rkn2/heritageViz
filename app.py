# dash and plotting
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
# databasing
from database_utilities import MongoHandler
# utilities
import datetime


def serve_layout(mc):  # definition of app, called when refreshed page, just layout = static
    layout = html.Div(children=[
        html.H1(children='Visualize sensor data.'),
        dcc.Dropdown(
            id='sensor-name-dropdown',
            options=mc.fetch_sensor_name_and_id(),
            multi=True
        ),
        html.Div(children=[
            html.P('Start date'),
            dcc.Input(
                id='date-picker-start-date',
                type='text',
                placeholder='YYYY-MM-DD',
                value=None,
                debounce=True
            ),
            html.P('Start time'),
            dcc.Input(
                id='date-picker-start-time',
                type='text',
                placeholder='HH:MM',
                value=None,
                debounce=True
            ),
            html.P('End date'),
            dcc.Input(
                id='date-picker-end-date',
                type='text',
                placeholder='YYYY-MM-DD',
                value=None,
                debounce=True
            ),
            html.P('End time'),
            dcc.Input(
                id='date-picker-end-time',
                type='text',
                placeholder='HH:MM',
                value=None,
                debounce=True

            ),
        ]),
        dcc.Graph(
            id='sensor-data-graph',
            figure=go.Figure(data=[], layout=go.Layout(title='Sensor data'))
        ),
    ])
    return layout


db_handler = MongoHandler()  # initialize mongo connection
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)  # defines empty dash app
server = app.server
app.layout = serve_layout(db_handler)  # sets layout to come from serve_layout with mongo handler passed in to it


# associates following function with a dash app callback
@app.callback(
    dash.dependencies.Output('sensor-data-graph', 'figure'),  # using id from dcc.graph above
    [dash.dependencies.Input('sensor-name-dropdown', 'value'),
     dash.dependencies.Input('date-picker-start-date', 'value'),
     dash.dependencies.Input('date-picker-start-time', 'value'),
     dash.dependencies.Input('date-picker-end-date', 'value'),
     dash.dependencies.Input('date-picker-end-time', 'value')])
# value comes from input, can have multiple values from call back since its a list
def update_figure(dropdown_value, start_date, start_time, end_date, end_time):
    try:
        start_datetime = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    except:
        start_datetime = None
    try:
        end_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    except:
        end_datetime = None
    if dropdown_value is None:
        return go.Figure(data=[], layout=go.Layout(title='Sensor data'))
    data = []
    for selection in dropdown_value:
        this_data = db_handler.fetch_sensor_data(selection, start_datetime, end_datetime)
        data += this_data
    fig = go.Figure(data=data, layout=go.Layout(title='Sensor data'))
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
