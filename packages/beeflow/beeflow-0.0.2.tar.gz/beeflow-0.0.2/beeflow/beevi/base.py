import pandas as pd

import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State


def get_layout():
    """Returns a BeeVi tab instance."""

    layout = dcc.Tab(label='BeeVi', value='beevi', children=[
        html.Div(children=[
            # Input part.
            html.Div(children=[
                # Graph type.
                html.Div(children=[
                    dcc.Markdown('##### Plot Type'),
                    dcc.Dropdown(id='beevi_graph_type', options=[
                        {'label': '2D Scatter', 'value': '2d_scatter'},
                        {'label': 'Histogram', 'value': 'hist'},
                    ], value='', clearable=False)
                ]),

                # Axis
                html.Div(children=[
                    dcc.Markdown('##### Axis Selection'),
                    html.Div(id='beevi_axis_selection')
                ]),
            ], style={'width': '30%', 'display': 'inline-block'}),

            # Graph part.
            html.Div(children=[
                dcc.Markdown('##### Graph'),
                html.Div(id='beevi_graph')],
                style={'width': '70%', 'height': '100%',
                       'display': 'inline-block'}
            )
        ])
    ])

    return layout


def get_callback(app):
    """Defines BeeVi callbacks."""

    # Change axis types according to the selects a graph type.
    @app.callback(Output('beevi_axis_selection', 'children'),
                  [Input('beevi_graph_type', 'value')],
                  [State('hidden_data', 'children')])
    def change_axis(graph_type, hidden_data):
        # Read data.
        if hidden_data is None:
            return

        df = pd.read_json(hidden_data)

        axis_layout = None
        # 2D scatter.
        if graph_type == '2d_scatter':
            axis_layout = html.Div(children=[
                # X-axis.
                html.Div(dcc.Markdown('X-axis')),
                html.Div(
                    dcc.Dropdown(id='beevi_x_axis', options=[
                        {'label': i, 'value': i} for i in df.columns
                        ], value='', clearable=False
                    )
                ),

                # Y-axis.
                html.Div(dcc.Markdown('Y-axis')),
                html.Div(
                    dcc.Dropdown(id='beevi_y_axis', options=[
                        {'label': i, 'value': i} for i in df.columns
                        ], value='', clearable=False
                    )
                ),

                # Hidden Z-axis.
                html.Div(id='beevi_z_axis', style={'display': 'none'})
            ])

        return axis_layout

    # Updates a graph.
    @app.callback(Output('beevi_graph', 'children'),
                  [Input('beevi_x_axis', 'value'),
                   Input('beevi_y_axis', 'value'),
                   Input('beevi_z_axis', 'value')],
                  [State('beevi_graph_type', 'value'),
                   State('hidden_data', 'children')])
    def update_graph(x_axis, y_axis, z_axis, graph_type, hidden_data):
        # Sanity check.
        if hidden_data is None:
            return
        if graph_type == '' or x_axis == '' or y_axis == '':
            return

        df = pd.read_json(hidden_data)

        graph = html.Div()
        if graph_type == '2d_scatter':
            graph = dcc.Graph(
                figure={
                    'data': [
                        go.Scatter(
                            x=df[x_axis],
                            y=df[y_axis],
                            mode='markers',
                            opacity=0.7,
                            marker={
                                'size': 3,
                                'line': {'width': 0.1, 'color': 'black'}
                            },
                        )
                    ],
                    'layout': go.Layout(
                        xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                        yaxis={'title': 'Life Expectancy'},
                        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                        legend={'x': 0, 'y': 1},
                        hovermode='closest'
                    )
                }
            )

        return graph
