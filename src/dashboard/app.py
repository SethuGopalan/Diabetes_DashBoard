# ============================================================
# IMPORTS
# Purpose:
# Import Dash, Bootstrap components, API request tools,
# and table components needed for the dashboard.
# ============================================================

from dash import Dash, html, dcc, Input, Output, State, callback_context, dash_table
import dash_bootstrap_components as dbc
import requests


# ============================================================
# DASH APP CONFIGURATION
# Purpose:
# Create the Dash app and connect it to Bootstrap styling.
# The requests_pathname_prefix is needed because the app runs
# through the Coder proxy.
# ============================================================

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    requests_pathname_prefix="/@sethugopalan/diabetes-dashboard.main/apps/code-server/proxy/8050/"
)


# ============================================================
# API CONFIGURATION
# Purpose:
# This URL connects the Dash app to the FastAPI backend.
# FastAPI must be running on port 9000.
# ============================================================

API_URL = "http://127.0.0.1:9000/info"


# ============================================================
# MAIN DASHBOARD LAYOUT
# Purpose:
# Build the full dashboard page layout.
# The page has three main columns:
# 1. Statistics
# 2. Visualization
# 3. Prediction
# ============================================================

app.layout = dbc.Container(
    fluid=True,
    className="dashboard-container",
    children=[

        # ====================================================
        # HEADER SECTION
        # Purpose:
        # Display the dashboard title with ECG design elements.
        # ====================================================

        dbc.Row([
            dbc.Col(
                width=12,
                children=[
                    html.Div(
                        className="dashboard-header",
                        children=[
                            html.Div(className="ecg-left"),
                            html.H1(
                                "Diabetic Prediction Dashboard",
                                className="dashboard-title"
                            ),
                            html.Div(className="ecg-right"),
                        ]
                    )
                ]
            )
        ]),

        # ====================================================
        # MAIN CONTENT ROW
        # Purpose:
        # Hold the three dashboard sections side by side.
        # ====================================================

        dbc.Row(
            className="main-row g-0",
            children=[

                # ============================================
                # STATISTICS SECTION
                # Purpose:
                # Explain the dataset, allow dataset exploration,
                # and prepare space for analysis tools.
                # ============================================

                dbc.Col(
                    width=4,
                    className="statistics-section p-0",
                    children=[

                        # Section title
                        html.H2("Statistics"),

                        # ------------------------------------
                        # DATASET OVERVIEW
                        # Purpose:
                        # Explain what the dataset contains.
                        # ------------------------------------

                        html.H4("Dataset Overview"),
                        html.P(
                            "This dataset contains medical records related to diabetes. "
                            "It includes glucose, blood pressure, BMI, insulin, skin thickness, "
                            "age, pregnancy history, and diabetes outcome values."
                        ),

                        html.H4("Total Records"),
                        html.P(
                            "There are 768 patient records in this dataset. "
                            "Each record represents one patient observation."
                        ),

                        html.H4("Dataset Features"),
                        html.P(
                            "The dataset features include patient health indicators such as glucose, blood pressure, BMI, insulin,"
                            " skin thickness, age, pregnancy history, and diabetes outcome values."
                        ),

                        # ------------------------------------
                        # DATASET EXPLORATION SECTION
                        # Purpose:
                        # Help users inspect the dataset before
                        # performing deeper analysis.
                        # ------------------------------------

                        html.H5("Dataset Exploration"),

                        html.P(
                            "Explore and understand the dataset before performing analysis.",
                            className="exploration-text"
                        ),

                        # Dataset exploration buttons
                        html.Div([
                            dbc.Button("Columns", id="btn-columns", color="success", className="check-data-btn"),
                            dbc.Button("Info", id="btn-info", color="success", className="check-data-btn"),
                            dbc.Button("Data Types", id="btn-dtypes", color="success", className="check-data-btn"),
                            dbc.Button("Head", id="btn-head", color="success", className="check-data-btn"),
                            dbc.Button("Tail", id="btn-tail", color="success", className="check-data-btn"),
                            dbc.Button("Clear", id="btn-clear", color="danger", className="check-data-btn"),
                        ]),

                        # ------------------------------------
                        # HEAD ROW MODAL
                        # Purpose:
                        # Ask user how many first rows to show.
                        # ------------------------------------

                        dbc.Modal(
                            [
                                dbc.ModalHeader("Select Head Rows"),
                                dbc.ModalBody([
                                    html.P("How many head rows do you want to show?"),
                                    dcc.Input(
                                        id="head-row-input",
                                        type="number",
                                        value=5,
                                        min=1,
                                        max=20
                                    )
                                ]),
                                dbc.ModalFooter(
                                    dbc.Button("Show", id="btn-show-head", color="success")
                                )
                            ],
                            id="head-modal",
                            is_open=False,
                            size="sm",
                            centered=False,
                        ),

                        # ------------------------------------
                        # TAIL ROW MODAL
                        # Purpose:
                        # Ask user how many last rows to show.
                        # ------------------------------------

                        dbc.Modal(
                            [
                                dbc.ModalHeader("Select Tail Rows"),
                                dbc.ModalBody([
                                    html.P("How many tail rows do you want to show?"),
                                    dcc.Input(
                                        id="tail-row-input",
                                        type="number",
                                        value=5,
                                        min=1,
                                        max=20
                                    )
                                ]),
                                dbc.ModalFooter(
                                    dbc.Button("Show", id="btn-show-tail", color="success")
                                )
                            ],
                            id="tail-modal",
                            is_open=False,
                            size="sm",
                            centered=False,
                        ),

                        html.Br(),

                        # ------------------------------------
                        # DATASET OUTPUT AREA
                        # Purpose:
                        # Show columns, info, data types,
                        # head table, or tail table.
                        # ------------------------------------

                        html.Div(
                            id="check-data-output",
                            children=[]
                        ),

                        html.Br(),

                        
                    ]
                ),

                # ============================================
                # VISUALIZATION SECTION
                # Purpose:
                # Placeholder for future charts and graphs.
                # ============================================

                dbc.Col(
                    width=4,
                    className="visualization-section p-0",
                    children=[
                        html.H2("Analysis & Visualization"),
                        html.P(
                            "This section will allow users to select chart types "
                            "and explore numeric relationships in the data."
                        ),
                        # ------------------------------------
                        # ANALYSIS SECTION
                        # Purpose:
                        # Let users choose a diabetes risk
                        # analysis type.
                        # ------------------------------------

                        html.H4("Analysis", className="analysis-title"),

                        html.P(
                            "Perform statistical and risk-based analysis on the selected data.",
                            className="analysis-text"
                        ),

                        # Analysis dropdown selector
                        dcc.Dropdown(
                            id="analysis-dropdown",
                            options=[
                                {"label": "Age Risk Analysis", "value": "age"},
                                {"label": "Pregnancy Analysis", "value": "pregnancies"},
                                {"label": "BMI / Obesity Analysis", "value": "bmi"},
                                {"label": "Glucose Analysis", "value": "glucose"},
                                {"label": "Combined Risk Analysis", "value": "combined"},
                            ],
                            placeholder="Select analysis type",
                            className="analysis-dropdown"
                        ),
                        html.Div(
                            id="analysis-output",
                            children=[
                                html.P("Select an analysis type to view results.")
                            ]
                        )
                                            ] 

                ),


                # ============================================
                # PREDICTION SECTION
                # Purpose:
                # Placeholder for future model prediction form.
                # ============================================

                dbc.Col(
                    width=4,
                    className="prediction-section p-0",
                    children=[
                        html.H2("Prediction"),
                        html.P(
                            "This section will allow users to enter patient values "
                            "and view diabetes prediction results."
                        ),
                    ]
                ),
            ]
            
        ),
         # ====================================================
        # FOOTER
        # Purpose:
        # Display dashboard information at the bottom.
        # ====================================================

        html.Footer(
            className="dashboard-footer",
            children=[
                html.P("Diabetic Prediction Dashboard"),
                html.P(
                    "Data Analysis • Visualization • Machine Learning Prediction"
                ),
                html.P("© 2026 Terrafox AI")
            ]
        ),
    ])
       

# ============================================================
# HEAD MODAL CALLBACK
# Purpose:
# Open and close the Head modal when user clicks Head or Show.
# ============================================================

@app.callback(
    Output("head-modal", "is_open"),
    Input("btn-head", "n_clicks"),
    Input("btn-show-head", "n_clicks"),
    State("head-modal", "is_open"),
    prevent_initial_call=True
)
def toggle_head_modal(head_clicks, show_head_clicks, is_open):
    return not is_open


# ============================================================
# TAIL MODAL CALLBACK
# Purpose:
# Open and close the Tail modal when user clicks Tail or Show.
# ============================================================

@app.callback(
    Output("tail-modal", "is_open"),
    Input("btn-tail", "n_clicks"),
    Input("btn-show-tail", "n_clicks"),
    State("tail-modal", "is_open"),
    prevent_initial_call=True
)
def toggle_tail_modal(tail_clicks, show_tail_clicks, is_open):
    return not is_open


# ============================================================
# DATASET EXPLORATION CALLBACK
# Purpose:
# Detect which exploration button was clicked,
# call the FastAPI endpoint, and return the correct output.
# ============================================================

@app.callback(
    Output("check-data-output", "children"),

    Input("btn-columns", "n_clicks"),
    Input("btn-info", "n_clicks"),
    Input("btn-dtypes", "n_clicks"),
    Input("btn-show-head", "n_clicks"),
    Input("btn-show-tail", "n_clicks"),
    Input("btn-clear", "n_clicks"),

    State("head-row-input", "value"),
    State("tail-row-input", "value"),

    prevent_initial_call=True
)
def run_check_data(
    columns_clicks,
    info_clicks,
    dtypes_clicks,
    show_head_clicks,
    show_tail_clicks,
    clear_clicks,
    head_row_count,
    tail_row_count
):

    # Call FastAPI backend
    response = requests.get(API_URL)

    # Convert API response into JSON
    try:
        data = response.json()

    # Show readable error if API fails
    except Exception:
        return html.Pre(
            f"API did not return JSON\n\n"
            f"Status: {response.status_code}\n\n"
            f"Response:\n{response.text[:300]}"
        )

    # Find which button triggered the callback
    clicked_button = callback_context.triggered[0]["prop_id"].split(".")[0]

    # Clear output area
    if clicked_button == "btn-clear":
        return []

    # Show column names
    if clicked_button == "btn-columns":
        return html.Ul([
            html.Li(col)
            for col in data["column_names"]
        ])

    # Show total rows and total columns
    elif clicked_button == "btn-info":
        return html.Ul([
            html.Li(f"Total Rows: {data['total_rows']}"),
            html.Li(f"Total Columns: {data['total_columns']}")
        ])

    # Show column data types
    elif clicked_button == "btn-dtypes":
        return html.Ul([
            html.Li(f"{col}: {dtype}")
            for col, dtype in data["data_types"].items()
        ])

    # Show first selected number of rows
    elif clicked_button == "btn-show-head":
        selected_rows = data["head_rows"][:head_row_count]

        table = dash_table.DataTable(
            columns=[
                {"name": col, "id": col}
                for col in data["column_names"]
            ],
            data=[
                dict(zip(data["column_names"], row))
                for row in selected_rows
            ],
            page_size=head_row_count,
            style_table={"overflowX": "auto"},
            style_cell={
                "minWidth": "100px",
                "width": "100px",
                "maxWidth": "100px",
                "textAlign": "center",
            },
            css=[
                {
                    "selector": ".dash-spreadsheet-container",
                    "rule": "border-radius: 10px; overflow: hidden;"
                }
            ]
        )

        return dbc.Card(
            dbc.CardBody([
                html.P(
                    f"Showing first {head_row_count} rows out of {data['total_rows']} total rows."
                ),
                table
            ]),
            className="table-card"
        )

    # Show last selected number of rows
    elif clicked_button == "btn-show-tail":
        selected_rows = data["tail_rows"][:tail_row_count]

        table = dash_table.DataTable(
            columns=[
                {"name": col, "id": col}
                for col in data["column_names"]
            ],
            data=[
                dict(zip(data["column_names"], row))
                for row in selected_rows
            ],
            page_size=tail_row_count,
            style_table={"overflowX": "auto"},
            style_cell={
                "minWidth": "100px",
                "width": "100px",
                "maxWidth": "100px",
                "textAlign": "center",
            },
            css=[
                {
                    "selector": ".dash-spreadsheet-container",
                    "rule": "border-radius: 10px; overflow: hidden;"
                }
            ]
        )

        return dbc.Card(
            dbc.CardBody([
                html.P(
                    f"Showing last {tail_row_count} rows out of {data['total_rows']} total rows."
                ),
                table
            ]),
            className="table-card"
        )
# ============================================================
# ANALYSIS DROPDOWN CALLBACK
# Purpose:
# Detect which analysis option was selected,
# call the FastAPI analysis endpoint,
# and return the selected analysis output.
# ============================================================
@app.callback(
Output("analysis-output","children"),
Input("analysis-dropdown","value"),
prevent_initial_call=True
)
def run_analysis(selected_analysis):
    if selected_analysis is None:
        return ""
    return html.P(f"selected analysis:{selected_analysis}")
# ============================================================
# APP RUNNER
# Purpose:
# Start the Dash dashboard server.
# ============================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8050)