from dash import Dash, html, dcc
import dash_bootstrap_components as dbc


app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)


app.layout = dbc.Container(
    fluid=True,
    className="dashboard-container",

    children=[

        # Header Row
        dbc.Row(
            children=[
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
            ]
        ),

        # Main Row
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

        # Description Row
        dbc.Row(
            className="description-row",
            children=[
                dbc.Col(
                    width=6,
                    className="statistics-help-section",
                    children=[
                        html.H5(
                            "Here you can select tools to generate descriptive statistics about the data."
                        )
                    ]
                ),

                dbc.Col(
                    width=6,
                    className="visualization-help-section",
                    children=[
                        html.H5(
                            "Here you can select numeric variables and visualization types."
                        )
                    ]
                ),
            ]
        ),

    ]
)


if __name__ == "__main__":
    app.run(debug=True, port=8050)