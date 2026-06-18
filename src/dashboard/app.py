from dash import Dash, html, dcc, Input, Output, State, callback_context, dash_table
import dash_bootstrap_components as dbc
import requests


app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

API_URL = "http://127.0.0.1:9000/info"


app.layout = dbc.Container(
    fluid=True,
    className="dashboard-container",
    children=[

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

        dbc.Row(
            className="main-row",
            children=[

                dbc.Col(
                    width=4,
                    className="statistics-section",
                    children=[
                        html.H2("Statistics"),

                        html.H4("What type of data is this?"),
                        html.P(
                            "This dataset contains medical records related to diabetes. "
                            "It includes glucose, blood pressure, BMI, insulin, skin thickness, "
                            "age, pregnancy history, and diabetes outcome values."
                        ),

                        html.H4("How many records are there?"),
                        html.P(
                            "There are 768 patient records in this dataset. "
                            "Each record represents one patient observation."
                        ),

                        html.H4("What are the features of the data?"),
                        html.P(
                            "The features describe patient health indicators that can be used "
                            "to explore diabetes risk and prepare predictive analysis."
                        ),

                        html.Div([
                            dbc.Button("Columns", id="btn-columns", color="success", className="check-data-btn"),
                            dbc.Button("Info", id="btn-info", color="success", className="check-data-btn"),
                            dbc.Button("Data Types", id="btn-dtypes", color="success", className="check-data-btn"),
                            dbc.Button("Head", id="btn-head", color="success", className="check-data-btn"),
                            dbc.Button("Tail", id="btn-tail", color="success", className="check-data-btn"),
                            dbc.Button("Clear",id="btn-clear",color="danger",className="check-data-btn"),
                        ]),

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
                            is_open=False
                        ),

                        html.Br(),

                        html.Div(
                            id="check-data-output",
                            children=[
                                html.P("Click a button above to explore the dataset.")
                            ]
                        ),
                    ]
                ),

                dbc.Col(
                    width=4,
                    className="visualization-section",
                    children=[
                        html.H2("Visualization"),
                        html.P(
                            "This section will allow users to select chart types "
                            "and explore numeric relationships in the data."
                        ),
                    ]
                ),

                dbc.Col(
                    width=4,
                    className="prediction-section",
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

        dbc.Row(
            className="description-row",
            children=[
                dbc.Col(
                    width=6,
                    className="statistics-help-section",
                    children=[
                        html.H5("Here you can select tools to generate descriptive statistics about the data.")
                    ]
                ),

                dbc.Col(
                    width=6,
                    className="visualization-help-section",
                    children=[
                        html.H5("Here you can select numeric variables and visualization types.")
                    ]
                ),
            ]
        ),
    ]
)


@app.callback(
    Output("head-modal", "is_open"),
    Input("btn-head", "n_clicks"),
    Input("btn-show-head", "n_clicks"),
    State("head-modal", "is_open"),
    prevent_initial_call=True
)
def toggle_head_modal(head_clicks, show_head_clicks, is_open):
    return not is_open


@app.callback(
    Output("tail-modal", "is_open"),
    Input("btn-tail", "n_clicks"),
    Input("btn-show-tail", "n_clicks"),
    State("tail-modal", "is_open"),
    prevent_initial_call=True
)
def toggle_tail_modal(tail_clicks, show_tail_clicks, is_open):
    return not is_open


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

    response = requests.get(API_URL)

    try:
        data = response.json()
    except Exception:
        return html.Pre(
            f"API did not return JSON\n\n"
            f"Status: {response.status_code}\n\n"
            f"Response:\n{response.text[:300]}"
        )

    clicked_button = callback_context.triggered[0]["prop_id"].split(".")[0]

    if clicked_button == "btn-clear":
        return html.P(
             "Click a button above to explore the dataset."
    )

    if clicked_button == "btn-columns":
        return html.Ul([
            html.Li(col)
            for col in data["column_names"]
        ])

    elif clicked_button == "btn-info":
        return html.Ul([
            html.Li(f"Total Rows: {data['total_rows']}"),
            html.Li(f"Total Columns: {data['total_columns']}")
        ])

    elif clicked_button == "btn-dtypes":
        return html.Ul([
            html.Li(f"{col}: {dtype}")
            for col, dtype in data["data_types"].items()
        ])

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


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True, port=8050)