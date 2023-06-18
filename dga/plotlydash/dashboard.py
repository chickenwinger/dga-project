import calendar

import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import html, dcc
from .dash import Dash
import plotly.graph_objs as go

from .data import create_dataframe


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = Dash(
        server=server,
        routes_pathname_prefix="/graph/",
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
        ],
    )

    # def init_dynamic_list():
    #     # TODO (enhance): Dynamic dropdown list
    #     df = create_dataframe()
    #     tf_dropdown = []
    #     for tf in df["transformerList"]:
    #         tf_dropdown.append({"label": tf, "value": tf})
    #     return tf_dropdown

    def init_month_list():
        month_dropdown = []
        mth = 1
        while mth < 13:
            monthName = calendar.month_name[mth]
            month_dropdown.append({"label": monthName, "value": mth})
            mth += 1
        return month_dropdown

    # Create Dash Layout using Bootstrap components
    dash_app.layout = dbc.Container([
        dbc.Row([
            html.H1(
                "Graph of Fault Type against Time",
                className="text-primary text-center fs-5 fw-3"
            )
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Label("Pick Transformer", className="text-secondary fs-5 my-1"),
                dcc.Dropdown(
                    id="transformer-dropdown",
                    options=[
                        {"label": "TX1", "value": "TX1"},
                        {"label": "TX2", "value": "TX2"},
                        {"label": "TX3", "value": "TX3"},
                        {"label": "TX4", "value": "TX4"},
                        {"label": "TX5", "value": "TX5"}
                    ],
                    # options=init_dynamic_list(),
                    value="TX1",
                    clearable=False,
                    style={
                        "width": "50%",
                    }
                )
            ]),
            dbc.Col([
                dbc.Label("Pick Month", className="text-secondary fs-5 my-1"),
                dcc.Dropdown(
                    id="month-dropdown",
                    # options=[
                    #     {"label": "January", "value": "1"},
                    #     {"label": "February", "value": "2"},
                    #     {"label": "March", "value": "3"},
                    #     {"label": "April", "value": "4"},
                    #     {"label": "May", "value": "5"},
                    #     {"label": "June", "value": "6"},
                    #     {"label": "July", "value": "7"},
                    #     {"label": "August", "value": "8"},
                    #     {"label": "September", "value": "9"},
                    #     {"label": "October", "value": "10"},
                    #     {"label": "November", "value": "11"},
                    #     {"label": "December", "value": "12"},
                    # ],
                    options=init_month_list(),
                    value=init_month_list()[0],
                    clearable=False,
                    style={
                        "width": "50%",
                    }
                )
            ]),
            dbc.Col([
                dbc.Label("Pick Gas", className="text-secondary fs-5 my-1"),
                dcc.Dropdown(
                    id="gas-dropdown",
                    options=[
                        {"label": "Acetylene", "value": "acetylene"},
                        {"label": "Carbon Dioxide", "value": "cdioxide"},
                        {"label": "Carbon Monoxide", "value": "cmonoxide"},
                        {"label": "Ethane", "value": "ethane"},
                        {"label": "Ethylene", "value": "ethylene"},
                        {"label": "Hydrogen", "value": "hydrogen"},
                        {"label": "Methane", "value": "methane"},
                    ],
                    value="acetylene",
                    clearable=False,
                    style={
                        "width": "50%",
                    }
                )
            ])
        ]),
        dbc.Row([
            html.H2(
                "Transformer TX1",
                className="text-primary text-center fs-5 fw-3 mt-10",
                id="tfHeader"
            )
        ]),
        dbc.Row([
            dcc.Graph(id="time-series-graph"),
        ]),
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
        dbc.Row([
            dbc.Alert(
                "Drag across the graph to zoom in. Drag across the timeline to jump back/ahead. Double click to reset.",
                color="info",
                className="mt-2 text-center",
            )
        ]),
    ])
    dash_app.scripts.append_script("""
        document.addEventListener('DOMContentLoaded', function() {
            var tfDropdown = document.querySelector('#transformer-dropdown');
            var tfHeader = document.querySelector('#tfHeader');
            tfDropdown.addEventListener('change', function(event) {
                tfHeader.textContent = 'Transformer ' + tfDropdown.value;
            });
        });
    """)

    init_callbacks(dash_app)

    return dash_app.server


def init_callbacks(dash_app):
    @dash_app.callback(
        Output("time-series-graph", "figure"),
        [Input("transformer-dropdown", "value"), Input("month-dropdown", "value"), Input("gas-dropdown", "value")]
    )
    def update_output(value):
        print(str(value))
        df = create_dataframe()

        # Filter the DataFrame based on the selected fault type
        filtered_graph = df[value[2], "Date"]

        colors = {"background": "hsl(279, 100%, 97%)", "text": "#7FDBFF"}

        # Create the time series graph
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=filtered_graph["Date"],
                y=filtered_graph["Fault Type ({})".format(value)],
                mode="markers",
                name="Fault Type",
                # hovertemplate="Record: %{customdata[0]}<br>"
                # + "Acetylene: %{customdata[1]}%<br>"
                # + "Hydrogen: %{customdata[2]}%<br>"
                # + "Methane: %{customdata[3]}%<br>"
                # + "Ethylene: %{customdata[4]}%<br>"
                # + "Ethane: %{customdata[5]}%<br>"
                # + "Carbon dioxide: %{customdata[6]}%<br>"
                # + "Carbon monoxide: %{customdata[7]}%<br>",
                # customdata=df[
                #     [
                #         "Record",
                #         "Acetylene",
                #         "Hydrogen",
                #         "Methane",
                #         "Ethylene",
                #         "Ethane",
                #         "Carbon dioxide",
                #         "Carbon monoxide",
                #     ]
                # ].values,
            )
        )

        fig.update_traces(
            marker=dict(size=14, line=dict(width=2), symbol="circle"),
        )

        fig.update_layout(
            xaxis_title="Date ({})".format(value),
            yaxis_title="Gas Concentration ()",
            xaxis=dict(
                showline=True,
                showgrid=True,
            ),
            paper_bgcolor=colors["background"],
            font=dict(color="black", size=14),
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
