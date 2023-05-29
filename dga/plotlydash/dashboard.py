import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import html, dcc
from .dash import Dash
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go

from .data import create_dataframe
from flask import current_app


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = Dash(
        server=server,
        routes_pathname_prefix="/graph/",
        external_stylesheets=[
            "/static/dist/css/styles.css",
            dbc.themes.BOOTSTRAP,
        ],
    )

    # Create Dash Layout using Bootstrap components
    dash_app.layout = dbc.Container(
        [
            dbc.Row(
                [
                    html.H1(
                        "Graph of Fault Type against Time",
                        className="text-primary text-center fs-5 fw-3",
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Label("Pick a tool", className="text-secondary fs-5 my-2"),
                    dcc.Dropdown(
                        id="fault-type-dropdown",
                        options=[
                            {"label": "DT1", "value": "dt1"},
                            {"label": "DT4", "value": "dt4"},
                            {"label": "DT5", "value": "dt5"},
                        ],
                        value="dt1",
                        clearable=False,
                        style={
                            "width": "50%",
                            "margin-bottom": "0.5rem",
                        },
                    ),
                ]
            ),
            dbc.Row(
                [
                    dcc.Graph(id="time-series-graph"),
                ]
            ),
            # dbc.Row(
            #     [
            #         html.Div(
            #             dcc.RangeSlider(
            #                 min=None,
            #                 max=None,
            #                 value=None,
            #                 id="time-series-slider",
            #             ),
            #             style={
            #                 "width": "100%",
            #                 "height": "50px",
            #                 "margin-top": "1rem",
            #                 "padding": "0rem .3rem .3rem .3rem",
            #             },
            #         ),
            #     ]
            # ),
            dbc.Row(
                [
                    dbc.Alert(
                        "Drag across the graph to zoom in. Drag across the timeline to jump back/ahead. Double click to reset.",
                        color="info",
                        className="mt-2 text-center",
                        style={
                            "display": "inline-block",
                        },
                    ),
                ]
            ),
        ],
    )

    init_callbacks(dash_app)

    return dash_app.server


def init_callbacks(dash_app):
    @dash_app.callback(
        Output("time-series-graph", "figure"),
        [Input("fault-type-dropdown", "value")],
    )
    def update_output(value):
        df = create_dataframe()

        # Filter the DataFrame based on the selected fault type
        filtered_df = df[["Timestamp", "Fault Type ({})".format(value)]]

        colors = {"background": "hsl(279, 100%, 97%)", "text": "#7FDBFF"}

        # Create the time series graph
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=filtered_df["Timestamp"],
                y=filtered_df["Fault Type ({})".format(value)],
                mode="markers",
                name="Fault Type",
            )
        )

        fig.update_traces(
            marker=dict(size=14, line=dict(width=2), symbol="circle"),
        )

        fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Fault Type",
            xaxis=dict(
                showline=True,
                showgrid=True,
            ),
            paper_bgcolor=colors["background"],
            font=dict(color="black", size=15),
            hovermode="closest",
        )

        return fig

    # @dash_app.callback(
    #     [
    #         Output("time-series-slider", "min"),
    #         Output("time-series-slider", "max"),
    #         Output("time-series-slider", "value"),
    #         Output("time-series-slider", "marks"),
    #     ],
    #     [Input("fault-type-dropdown", "value")],
    # )
    # def update_slider_properties(value):
    #     df = create_dataframe()

    #     min_value = df["Timestamp"].min()
    #     max_value = df["Timestamp"].max()
    #     value_range = [min_value, max_value]
    #     marks = {str(timestamp): timestamp for timestamp in df["Timestamp"].unique()}

    #     return min_value, max_value, value_range, marks

    # @dash_app.callback(
    #     Output("time-series-graph", "figure"),
    #     [Input("fault-type-dropdown", "value"), Input("time-series-slider", "value")],
    # )
    # def update_output(fault_type, time_range):
    #     df = create_dataframe()

    #     # Filter the DataFrame based on the selected fault type and time range
    #     filtered_df = df[
    #         (df["Timestamp"] >= time_range[0]) & (df["Timestamp"] <= time_range[1])
    #     ]
    #     filtered_df = filtered_df[["Timestamp", "Fault Type ({})".format(fault_type)]]

    #     # Create the time series graph
    #     # ... (rest of the code remains the same)
