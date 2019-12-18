# dash and plotting
import dash
import dash_core_components as dcc
import dash_html_components as html

from app import external_stylesheets

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
        dcc.Upload(html.Button('Upload File')),
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
