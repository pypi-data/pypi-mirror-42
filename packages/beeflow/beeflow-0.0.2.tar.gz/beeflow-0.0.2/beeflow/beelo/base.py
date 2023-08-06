import io
import base64

import pandas as pd

import dash_table
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output


def get_layout():
    """Returns a BeeLo tab instance."""

    layout = dcc.Tab(label='BeeLo', value='beelo', children=[
        html.Div([
            # Column separation control.
            dcc.Markdown('##### Column Separation'),
            dcc.RadioItems(
                id='beelo_column_separation',
                options=[
                    {'label': 'Comma ","', 'value': 'comma'},
                    {'label': 'Space', 'value': 'space'},
                    {'label': 'Tab', 'value': 'tab'},
                    {'label': 'Regular Expression', 'value': 'reg'}],
                value='comma',
                labelStyle={'display': 'inline-block'},
                style={'width': '60%', 'display': 'inline-block'}
            ),
            dcc.Input(
                id='beelo_column_separation_reg',
                type='text', value='\\s+',
                style={'width': '40%', 'display': 'inline-block'}
            ),

            # File upload.
            dcc.Markdown('##### File Selection'),
            dcc.Upload(
                id='beelo_upload',
                children=html.Div([
                    'Drag & Drop or ', html.A('Select a File')
                ]),
                style={
                    'width': '95%', 'height': '80px',
                    'align': 'center', 'lineHeight': '80px',
                    'borderWidth': '1px', 'borderStyle': 'solid',
                    'borderRadius': '5px', 'margin': '20px',
                    'textAlign': 'center', 'font-size': '20px'},
                # Disallow multiple file selection.
                multiple=False),

            # Row control.
            dcc.Markdown('##### Row Selection'),
            dcc.RadioItems(
                id='beelo_file_reading',
                options=[
                    {'label': 'Top N Rows', 'value': 'top'},
                    {'label': 'All Rows', 'value': 'all'}],
                value='top',
                labelStyle={'display': 'inline-block'},
                style={'width': '60%', 'display': 'inline-block'}
            ),
            dcc.Input(
                id='beelo_n_rows',
                type='text', value='10',
                style={'width': '40%', 'display': 'inline-block'}
            ),

            # Table.
            html.Div(id='beelo_data_table'),

            # Error log.
            html.Div(id='beelo_log')
        ])
    ])

    return layout


def get_callback(app):
    """Defines BeeLo callbacks."""

    # Load a file.
    @app.callback(Output('hidden_data', 'children'),
                  [Input('beelo_upload', 'contents'),
                   Input('beelo_upload', 'filename'),
                   Input('beelo_column_separation', 'value'),
                   Input('beelo_column_separation_reg', 'value')])
    def beelo_load_file(contents, filename, column_separation, reg):
        # Only if file is ready.
        if contents is None:
            return

        _, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        # Delimiter.
        sep = ''
        if column_separation == 'comma':
            sep = ','
        elif column_separation == 'space':
            sep = '\s+'
        elif column_separation == 'tab':
            sep = '\t+'
        elif column_separation == 'reg':
            sep = reg

        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), sep=sep)

        return df.to_json()

    # Update the data table.
    @app.callback(Output('beelo_data_table', 'children'),
                  [Input('hidden_data', 'children'),
                   Input('beelo_file_reading', 'value'),
                   Input('beelo_n_rows', 'value')])
    def beelo_update_table(hidden_data, file_reading, n_rows):
        # If data exists.
        if hidden_data is None or n_rows is None:
            return

        df = pd.read_json(hidden_data)

        # Show a part of file.
        if file_reading == 'top':
            n_rows = int(n_rows)
        else:
            n_rows = len(df.index)

        df_show = df[:n_rows]

        # Table.
        data_table = html.Div(children=[
            dcc.Markdown('##### Data Table'),
            dash_table.DataTable(
                columns=[{'name': i, 'id': i} for i in df_show.columns],
                data=df_show.to_dict('rows'),
                sorting=True,
                style_as_list_view=True,
                style_cell_conditional=[{
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'}],
                virtualization=False
            )
        ])

        return data_table
