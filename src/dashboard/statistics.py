# ============================================================
# IMPORTS
# Purpose:
# Import Dash components, Bootstrap components,
# API request tools, and DataTable.
# ============================================================

from dash import (
    html,
    dcc,
    Input,
    Output,
    State,
    ctx,
    dash_table,
    no_update,
)

import dash_bootstrap_components as dbc
import requests
import plotly.express as px
import pandas as pd


# ============================================================
# API CONFIGURATION
# Purpose:
# Connect the Statistics section to FastAPI /info.
# ============================================================

API_URL = "http://127.0.0.1:9000/info"


# ============================================================
# STATISTICS LAYOUT
# Purpose:
# Build the complete Statistics dashboard column.
# ============================================================

def statistics_layout():

    return dbc.Col(
        width=4,
        className="statistics-section p-0",
        children=[

            # =================================================
            # SECTION TITLE
            # =================================================

            html.H2("Data Explorer"),


            # -------------------------------------------------
            # DATASET OVERVIEW
            # -------------------------------------------------

            html.H4("Dataset Summary"),

            html.P(
                "This dataset contains patient health observations used to examine "
                "patterns and risk factors associated with diabetes. Each record "
                "represents one patient and includes clinical and demographic "
                 "measurements together with the diabetes outcome."
            ),


            # -------------------------------------------------
            # TOTAL RECORDS
            # -------------------------------------------------

            html.H4("Key Statistics"),
              
              html.P(
                [
                    "There are ",
                    html.Span(id="total-records"),
                    " patient records in this dataset. "
                    "Each record represents one patient observation. ",

                    "The dataset currently contains ",
                    html.Span(id="total-columns"),
                    " columns containing patient health information. ",

                    "There are ",
                    html.Span(id="diabetic-patients"),
                    " patients classified as diabetic and ",
                    html.Span(id="non-diabetic-patients"),
                    " patients classified as non-diabetic. ",

                    "The overall diabetes prevalence in the dataset is ",
                    html.Span(id="diabetes-prevalence"),
                    "%.",
                ],className="key-statistics-text",
            ),
                     

                
                dcc.Location(id="url", refresh=False),

            # -------------------------------------------------
            # DATASET FEATURES
            # -------------------------------------------------

            html.H4("Dataset Features"),

            html.P(
                "The dataset combines demographic, metabolic, and clinical features, "
                 "including age, pregnancy history, glucose, blood pressure, BMI, "
                "insulin, skin thickness, and diabetes pedigree function, with "
                "diabetes as the outcome variable."
            ),

            
            # -------------------------------------------------
            # DATASET EXPLORATION
            # -------------------------------------------------

            html.H5("Dataset Exploration"),

            html.P(
                "Explore and understand the dataset before "
                "performing analysis.",
                className="exploration-text",
            ),


            # -------------------------------------------------
            # EXPLORATION BUTTONS
            # -------------------------------------------------

            html.Div(
                [
                    dbc.Button(
                        "Columns",
                        id="btn-columns",
                        color="success",
                        className="check-data-btn",
                    ),

                    dbc.Button(
                        "Info",
                        id="btn-info",
                        color="success",
                        className="check-data-btn",
                    ),

                    dbc.Button(
                        "Data Types",
                        id="btn-dtypes",
                        color="success",
                        className="check-data-btn",
                    ),

                    dbc.Button(
                        "Head",
                        id="btn-head",
                        color="success",
                        className="check-data-btn",
                    ),

                    dbc.Button(
                        "Tail",
                        id="btn-tail",
                        color="success",
                        className="check-data-btn",
                    ),

                    dbc.Button(
                        "Clear",
                        id="btn-clear",
                        color="danger",
                        className="check-data-btn",
                    ),
                ]
            ),


            # -------------------------------------------------
            # HEAD ROW SELECTOR
            # Purpose:
            # Hidden initially using Bootstrap d-none.
            # -------------------------------------------------

            html.Div(
                id="head-row-selector",
                className="d-none",
                children=[
                    dbc.Card(
                        children=[
                            html.P(
                                "How many head rows do you want to show?"
                            ),

                            dcc.Input(
                                id="head-row-input",
                                type="number",
                                value=5,
                                min=1,
                                max=20,
                            ),

                            dbc.Button(
                                "Show",
                                id="btn-show-head",
                                color="success",
                            ),
                        ],
                        className="row-selector-card",
                    )
                ],
            ),


            # -------------------------------------------------
            # TAIL ROW SELECTOR
            # -------------------------------------------------

            html.Div(
                id="tail-row-selector",
                className="d-none",
                children=[
                    dbc.Card(
                        children=[
                            html.P(
                                "How many tail rows do you want to show?"
                            ),

                            dcc.Input(
                                id="tail-row-input",
                                type="number",
                                value=5,
                                min=1,
                                max=20,
                            ),

                            dbc.Button(
                                "Show",
                                id="btn-show-tail",
                                color="success",
                            ),
                        ],
                        className="row-selector-card",
                    )
                ],
            ),

            html.Br(),
            # -------------------------------------------------
            # CORRELATION HEATMAP
            # Purpose:
            # Reserve space for the default correlation heatmap.
            # -------------------------------------------------

            html.H5("Correlation Heatmap"),

            html.Div(
                id="correlation-heatmap",
                className="correlation-heatmap",
            ),


            # -------------------------------------------------
            # DATASET OUTPUT
            # -------------------------------------------------

            html.Div(
                id="check-data-output",
                children=[],
            ),

            html.Br(),
        ],
    )


# ============================================================
# REGISTER STATISTICS CALLBACKS
# Purpose:
# Register all Statistics callbacks with the main Dash app.
# ============================================================

def register_statistics_callbacks(app):

    # ============================================================
    # KEY STATISTICS CALLBACK
    # Purpose:
    # Load current dataset summary values from the FastAPI /info
    # endpoint and display them in the Data Explorer section.
    #
    # This keeps total records, total columns, diabetic patients,
    # non-diabetic patients, and diabetes prevalence updated
    # whenever the dashboard loads.
    # ============================================================
    @app.callback(
        Output("total-records", "children"),
        Output("total-columns", "children"),
        Output("diabetic-patients", "children"),
        Output("non-diabetic-patients", "children"),
        Output("diabetes-prevalence", "children"),
        Input("url", "pathname")

    )
    def key_stats(pathname):

        try:
            response = requests.get(
                API_URL,
                timeout=10,
            )

            data = response.json()

        except Exception as error:

            return html.P(
                f"Unable to load Statistics data: {error}"
            )
        
        return (
                data["total_rows"],
                data["total_columns"],
                data["diabetic_patients"],
                data["non_diabetic_patients"],
                data["diabetes_prevalence"],
            )


    # ========================================================
    # HEAD / TAIL SELECTOR CALLBACK
    # Purpose:
    # Show or hide the Head and Tail selectors.
    # Uses Bootstrap d-none/d-block classes instead of
    # inline CSS.
    # ========================================================

    @app.callback(
        Output("head-row-selector", "className"),
        Output("tail-row-selector", "className"),
        Input("btn-head", "n_clicks"),
        Input("btn-tail", "n_clicks"),
        Input("btn-show-head", "n_clicks"),
        Input("btn-show-tail", "n_clicks"),
        prevent_initial_call=True,
        
    )
    def toggle_row_selectors(
        head_clicks,
        tail_clicks,
        show_head_clicks,
        show_tail_clicks,
    ):

        clicked_button = ctx.triggered_id

        if clicked_button == "btn-head":
            return "d-block", "d-none"

        elif clicked_button == "btn-tail":
            return "d-none", "d-block"

        elif clicked_button == "btn-show-head":
            return "d-none", "d-none"

        elif clicked_button == "btn-show-tail":
            return "d-none", "d-none"

        return no_update, no_update


    # ========================================================
    # DATASET EXPLORATION CALLBACK
    # Purpose:
    # Call FastAPI and display the selected Statistics result.
    # ========================================================

    @app.callback(
        Output("check-data-output", "children"),
        Output("correlation-heatmap", "className"),
        Input("btn-columns", "n_clicks"),
        Input("btn-info", "n_clicks"),
        Input("btn-dtypes", "n_clicks"),
        Input("btn-show-head", "n_clicks"),
        Input("btn-show-tail", "n_clicks"),
        Input("btn-clear", "n_clicks"),
        State("head-row-input", "value"),
        State("tail-row-input", "value"),
        prevent_initial_call=True,
    )
    def run_check_data(
        columns_clicks,
        info_clicks,
        dtypes_clicks,
        show_head_clicks,
        show_tail_clicks,
        clear_clicks,
        head_row_count,
        tail_row_count,
    ):

        # ----------------------------------------------------
        # CALL FASTAPI
        # ----------------------------------------------------

        try:
            response = requests.get(
                API_URL,
                timeout=10,
            )

            data = response.json()

        except Exception as error:

            return html.P(
                f"Unable to load Statistics data: {error}"
            )


        # ----------------------------------------------------
        # DETECT SELECTED BUTTON
        # Default to Columns when dashboard starts.
        # ----------------------------------------------------

        clicked_button = ctx.triggered_id or "btn-columns"


        # ----------------------------------------------------
        # CLEAR
        # ----------------------------------------------------

        if clicked_button == "btn-clear":
            return [],"correlation-heatmap"


        # ----------------------------------------------------
        # COLUMNS
        # ----------------------------------------------------

        if clicked_button == "btn-columns":

            return( html.Ul(
                [
                    html.Li(column)
                    for column in data["column_names"]
                ]
            ),
              "correlation-heatmap d-none",
            )

        # ----------------------------------------------------
        # INFO
        # ----------------------------------------------------

        elif clicked_button == "btn-info":

            return ( html.Ul(
                [
                    html.Li(
                        f"Total Rows: {data['total_rows']}"
                    ),

                    html.Li(
                        f"Total Columns: {data['total_columns']}"
                    ),
                ]
            ),"correlation-heatmap d-none",
            )

        # ----------------------------------------------------
        # DATA TYPES
        # ----------------------------------------------------

        elif clicked_button == "btn-dtypes":

            return ( html.Ul(
                [
                    html.Li(
                        f"{column}: {data_type}"
                    )
                    for column, data_type
                    in data["data_types"].items()
                ]
            ),"correlation-heatmap d-none",
        )

        # ----------------------------------------------------
        # HEAD
        # ----------------------------------------------------

        elif clicked_button == "btn-show-head":

            selected_rows = (
                data["head_rows"][:head_row_count]
            )

            table = create_data_table(
                data,
                selected_rows,
                head_row_count,
            )

            return dbc.Card(
                dbc.CardBody(
                    [
                        html.P(
                            f"Showing first {head_row_count} "
                            f"rows out of "
                            f"{data['total_rows']} total rows."
                        ),

                        table,
                    ]
                ),
                className="table-card",
            ),"correlation-heatmap d-none",


        # ----------------------------------------------------
        # TAIL
        # ----------------------------------------------------

        elif clicked_button == "btn-show-tail":

            selected_rows = (
                data["tail_rows"][:tail_row_count]
            )

            table = create_data_table(
                data,
                selected_rows,
                tail_row_count,
            )

            return dbc.Card(
                dbc.CardBody(
                    [
                        html.P(
                            f"Showing last {tail_row_count} "
                            f"rows out of "
                            f"{data['total_rows']} total rows."
                        ),

                        table,
                    ]
                ),
                
                className="table-card",
            ),"correlation-heatmap d-none",

    # ============================================================
    # CORRELATION HEATMAP CALLBACK
    # Purpose:
    # Load correlation data from the FastAPI correlation endpoint
    # when the dashboard opens.
    #
    # Create a Plotly correlation heatmap and display it in the
    # Data Exploration section.
    #
    # The heatmap helps users understand relationships between
    # numeric dataset features such as glucose, BMI, age,
    # insulin, pregnancies, and diabetes outcome.
    # ============================================================
    @app.callback(
        Output("correlation-heatmap", "children"),
        Input("url", "pathname"),
    
    )
    def core_graph(pathname):
        
        try:
            response = requests.get(
                API_URL,
                timeout=10,
            )

            data = response.json()

        except Exception as error:

            return html.P(
                f"Unable to load Statistics data: {error}"
            )
        
        figure = px.imshow(
            data["correlation_matrix"],
            x=data["correlation_columns"],
            y=data["correlation_columns"],
            text_auto=True,
            aspect="auto",
            zmin=-1,
            zmax=1,
            color_continuous_scale=[
            [0.0, "#E34B42"],
            [0.5, "#071512"],
            [0.7, "#145C4A"],
            [1.0, "#79E0BE"],
            ],
            # title="Feature Correlation Heatmap",
                    )
        figure.update_layout(
            height = 300,
            paper_bgcolor="rgba(5,18,17,0.92)",
            plot_bgcolor="rgba(5,18,17,0.92)",
            font=dict(color="#E8EEEB",size=11),
            title_font=dict(color="#79E0BE"),
             margin=dict(
                        l=95,
                        r=35,
                        t=20,
                        b=85,
            ),
            coloraxis_showscale=False,

            #     coloraxis_colorbar=dict(
            #     title="Correlation",
            #     thickness=12,
            #     len=0.75,
            # ),
        )
        figure.update_xaxes(
                tickangle=-45,
                tickfont=dict(size=10),
            )

        figure.update_yaxes(
                tickfont=dict(size=10),
            )
        figure.update_coloraxes(showscale=True)
                    
        return dcc.Graph(figure=figure)


# ============================================================
# DATA TABLE HELPER
# Purpose:
# Create the reusable Head/Tail DataTable.
#
# All visual appearance is controlled from style.css.
# ============================================================

def create_data_table(
    data,
    selected_rows,
    page_size,
):

    return dash_table.DataTable(

        columns=[
            {
                "name": column,
                "id": column,
            }
            for column in data["column_names"]
        ],

        data=[
            dict(
                zip(
                    data["column_names"],
                    row,
                )
            )
            for row in selected_rows
        ],

        page_size=page_size,
    )
    
        
        