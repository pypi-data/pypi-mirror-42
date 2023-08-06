import uuid
import dash
import dash_resumable_upload
import dash_core_components as dcc
import dash_html_components as html

from beeflow.beelo import beelo_layout, beelo_callback
from beeflow.beevi import beevi_layout, beevi_callback
from beeflow.beeml import beeml_layout, beeml_callback
from beeflow.beeser import beeser_layout, beeser_callback
from beeflow.beeman import beeman_layout, beeman_callback

# CSS style sheet.
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Designing BeeFlow Dash framework.
app = dash.Dash('BeeFlow Dash Framework',
                external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True
# For large file upload.
upload_folder = 'uploads'
dash_resumable_upload.decorate_server(app.server, upload_folder)


def serve_layout():
    """Returns an outline of the BeeFlow layout."""

    # Random unique session ID.
    session_id = str(uuid.uuid4())

    return html.Div([
        # Title section.
        html.H2('BeeFlow', style={'font-family':  'Monaco',
                                  'font-weight':  'bold',
                                  'color': '#4488CC'}),

        # Tab component.
        dcc.Tabs(id='all_tabs', value='beelo', children=[
            # BeeLo Tab.
            beelo_layout(),
            # BeeVi Tab.
            beevi_layout(),
            # BeeML Tab.
            beeml_layout(),
            # BeeSer Tab.
            beeser_layout(),
            # BeeMan Tab.
            beeman_layout()
        ]),

        # Session ID.
        html.Div(id='session-id', children=session_id,
                 style={'display': 'none'}),

        # Absolute path to the input data file.
        html.Div(id='hidden_data', style={'display': 'none'}),

        # Placeholder for any printing.
        html.Div(id='print')
    ])


# ------------- BeeFlow Layout.
app.layout = serve_layout

# ------------- BeeFlow Callbacks.
# BeeLo callbacks.
beelo_callback(app)

# BeeVi callbacks.
beevi_callback(app)

# BeeML callbacks.
beeml_callback(app)

# BeeSer callbacks.
beeser_callback(app)

# BeeMan callbacks.
beeman_callback(app)


if __name__ == '__main__':
    app.run_server(debug=True)
