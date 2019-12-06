import dash
import dash_core_components as dcc
import dash_html_components as html
import arango
import numpy as np
# Initialize the ArangoDB client.
client = arango.ArangoClient(hosts='http://localhost:8529')

# Connect to "_system" database as root user.
# This returns an API wrapper for "_system" database.
sys_db = client.db('_system', username='root', password='')

# Connect to "test" database as root user.
# This returns an API wrapper for "test" database.
db = client.db('test', username='root', password='')

# Execute an AQL query. This returns a result cursor.
cursor = db.aql.execute('FOR doc IN ResearchBuilding RETURN doc')

# Iterate through the cursor to retrieve the documents.
rooms = [document for document in cursor]

db2plot = lambda room, var : {'x': np.array(room['temperature'])[:,0],
                              'y': np.array(room['temperature'])[:,1],
                              'type': 'scatter', 'mode': 'lines+markers',
                              'name': room['name'] + var}

# from dash plotly

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Hello Becca'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [db2plot(room, 'temperature') for room in rooms],
                #[
                # {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                # {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montreal'},
            #],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True) #hot reloading so it auto updates