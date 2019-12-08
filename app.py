# dash and plotting
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
# databasing
import pymongo
# utilities
import datetime
import json


class MongoHandler(object):
    def __init__(self):
        self.conf = json.load(open('mongoDB.conf', 'r'))
        self.client = pymongo.MongoClient(self.conf['MONGODB_URI'])
        self.db = self.client[self.conf['MONGODB_DATABASE']]
        self.col = self.db[self.conf['MONGODB_COLLECTION']]

    def fetch_sensor_name_and_id(self):
        name_and_id = [{'label': x['name'], 'value': x['name']} for x in self.col.find({}, {'name': 1})]
        return name_and_id

    def fetch_sensor_data(self, name):
        docs = [x for x in self.col.find({'name': name})]
        plot_data = []
        for doc in docs:
            label = doc['name']
            data = doc[label]
            timestamp = doc['timestamp']
            times = [datetime.datetime.strptime(x, '%c') for x in timestamp]
            plot_data.append({'x': times, 'y': data, 'name': label})
        return plot_data

    def upload(self, docs):
        self.col.insert_many(docs)


def serve_layout(mc):
    layout = html.Div(children=[
        html.H1(children='Visualize sensor data.'),
        dcc.Dropdown(
            id='sensor-name-dropdown',
            options=mc.fetch_sensor_name_and_id(),
            multi=True
        ),
        html.Div(id='dd-output-container'),
        dcc.Graph(
            id='sensor-data-graph',
            figure=go.Figure(data=[], layout=go.Layout(title='Sensor data'))
        )
    ])
    return layout


db_handler = MongoHandler()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout = serve_layout(db_handler)


@app.callback(
    dash.dependencies.Output('sensor-data-graph', 'figure'),
    [dash.dependencies.Input('sensor-name-dropdown', 'value')])
def update_figure(value):
    if value is None:
        return go.Figure(data=[], layout=go.Layout(title='Sensor data'))
    data = []
    for selection in value:
        data += db_handler.fetch_sensor_data(selection)
    fig = go.Figure(data=data, layout=go.Layout(title='Sensor data'))
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
