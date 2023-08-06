import io
import base64

import pandas as pd

import dash_table
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State


def get_layout():
    """Returns a BeeML tab instance."""

    layout = dcc.Tab(label='BeeML', value='beeml', children=[
        html.Div(children=[

        ]),
    ])

    return layout


def get_callback(app):
    pass
