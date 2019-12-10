import json
import dash
import dash_html_components as html
from dash.dependencies import Output
from dash.exceptions import PreventUpdate
from dash_canvas import DashCanvas
from dash.dependencies import Input
from dash_table import DataTable

filename = 'https://www.publicdomainpictures.net/pictures/60000/nahled/flower-outline-coloring-page.jpg'
canvas_width = 500

columns = ['type', 'width', 'height', 'scaleX', 'strokeWidth', 'path']

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    html.H5('Press down the left mouse button and draw inside the canvas'),
    DashCanvas(
        id='canvas-color',
        width=canvas_width,
        filename=filename,
        hide_buttons=['line', 'zoom', 'pan']
    ),
    DataTable(
        id='annot-canvas-table',
        style_cell={'textAlign': 'left'},
        columns=[{"name": i, "id": i} for i in columns],
        style_table={'display': 'none'},
        export_format='xlsx',
        export_headers='display'
    )
])


@app.callback(Output('annot-canvas-table', 'data'),
              [Input('canvas-color', 'json_data')])
def update_data(string):
    if string:
        data = json.loads(string)
    else:
        raise PreventUpdate
    return data['objects'][1:]


if __name__ == '__main__':
    app.run_server(debug=True)
