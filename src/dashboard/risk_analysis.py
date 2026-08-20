# ============================================================
# IMPORTS
# Purpose:
# Build the Analysis section, call FastAPI,
# and display analysis results.
# ============================================================

from dash import (
    html,
    dcc,
    Input,
    Output,
)

import dash_bootstrap_components as dbc
import requests


# ============================================================
# API CONFIGURATION
# Purpose:
# Connect the dashboard Analysis section to FastAPI.
# ============================================================

ANALYSIS_API_URL = "http://127.0.0.1:9000/analysis"


# ============================================================
# ANALYSIS LAYOUT
# Purpose:
# Build the Analysis dropdown and output area.
# ============================================================

def analysis_layout():

    return html.Div(
        className="analysis-container",
        children=[

            # ------------------------------------------------
            # ANALYSIS HEADER
            # ------------------------------------------------

            html.H4(
                "Analysis",
                className="analysis-title",
            ),

            html.P(
                "Perform statistical and risk-based "
                "analysis on the selected data.",
                className="analysis-text",
            ),


            # ------------------------------------------------
            # ANALYSIS DROPDOWN
            # ------------------------------------------------

            dcc.Dropdown(
                id="analysis-dropdown",

                options=[
                    {
                        "label": "Age Risk Analysis",
                        "value": "age",
                    },

                    {
                        "label": "Pregnancy Analysis",
                        "value": "pregnancy",
                    },

                    {
                        "label": "BMI / Obesity Analysis",
                        "value": "bmi",
                    },

                    {
                        "label": "Glucose Analysis",
                        "value": "glucose",
                    },

                    {
                        "label": "Combined Risk Analysis",
                        "value": "combined",
                    },
                ],

                value="age",

                placeholder="Select analysis type",

                className="analysis-dropdown",
            ),


            # ------------------------------------------------
            # ANALYSIS OUTPUT
            # ------------------------------------------------

            html.Div(
                id="analysis-output",
                className="analysis-output",
                children=[],
            ),
        ],
    )


# ============================================================
# STANDARD ANALYSIS CARD
# Purpose:
# Build one reusable result card.
#
# Age, BMI, Glucose, Pregnancy, and Combined Risk
# can all use the same card structure.
# ============================================================

def create_analysis_card(
    title,
    group_heading,
    group_value,
    group,
):

    return dbc.Card(
        dbc.CardBody(
            [

                # ------------------------------------------------
                # ANALYSIS TYPE
                # ------------------------------------------------

                html.H5(
                    title,
                    className="age-analysis-title",
                ),


                # ------------------------------------------------
                # RESULT HEADINGS
                # ------------------------------------------------

                dbc.Row(
                    [
                        dbc.Col(
                            html.Strong(group_heading)
                        ),

                        dbc.Col(
                            html.Strong("Total Patients")
                        ),

                        dbc.Col(
                            html.Strong("Diabetic Patients")
                        ),

                        dbc.Col(
                            html.Strong(
                                "Diabetic Percentage"
                            )
                        ),
                    ],
                    className="age-analysis-header",
                ),


                # ------------------------------------------------
                # RESULT VALUES
                # ------------------------------------------------

                dbc.Row(
                    [
                        dbc.Col(
                            group_value
                        ),

                        dbc.Col(
                            group["total_patients"]
                        ),

                        dbc.Col(
                            group["diabetic_patients"]
                        ),

                        dbc.Col(
                            f"{group['diabetes_percentage']}%"
                        ),
                    ],
                    className="age-analysis-row",
                ),
            ],

            className="age-analysis-body",
        ),

        className="age-analysis-card",
    )


# ============================================================
# REGISTER ANALYSIS CALLBACKS
# Purpose:
# Connect the dropdown to FastAPI and display results.
# ============================================================

def register_analysis_callbacks(app):

    @app.callback(
        Output(
            "analysis-output",
            "children",
        ),

        Input(
            "analysis-dropdown",
            "value",
        ),
    )
    def run_analysis(selected_analysis):

        cards = []

        if selected_analysis is None:
            return cards


        # ====================================================
        # CALL FASTAPI
        # ====================================================

        analysis_url = (
            f"{ANALYSIS_API_URL}/{selected_analysis}"
        )

        try:

            response = requests.get(
                analysis_url,
                timeout=10,
            )

            data = response.json()

        except Exception as error:

            return [
                html.P(
                    f"Unable to load analysis: {error}"
                )
            ]


        # ====================================================
        # AGE ANALYSIS
        # ====================================================

        if selected_analysis == "age":

            for group in data["data"]:

                cards.append(
                    create_analysis_card(
                        title="Analysis Type: Age",
                        group_heading="Age Group",
                        group_value=group["age_group"],
                        group=group,
                    )
                )


        # ====================================================
        # BMI ANALYSIS
        # ====================================================

        elif selected_analysis == "bmi":

            for group in data["data"]:

                cards.append(
                    create_analysis_card(
                        title="Analysis Type: BMI",
                        group_heading="BMI Group",
                        group_value=group["bmi_group"],
                        group=group,
                    )
                )


        # ====================================================
        # GLUCOSE ANALYSIS
        # ====================================================

        elif selected_analysis == "glucose":

            for group in data["data"]:

                cards.append(
                    create_analysis_card(
                        title="Analysis Type: Glucose",
                        group_heading="Glucose Group",
                        group_value=group[
                            "glucose_group"
                        ],
                        group=group,
                    )
                )


        # ====================================================
        # PREGNANCY ANALYSIS
        # ====================================================

        elif selected_analysis == "pregnancy":

            for group in data["data"]:

                cards.append(
                    create_analysis_card(
                        title="Analysis Type: Pregnancy",
                        group_heading="Pregnancy Group",
                        group_value=group[
                            "pregnancies_group"
                        ],
                        group=group,
                    )
                )


        # ====================================================
        # COMBINED RISK ANALYSIS
        # ====================================================

        elif selected_analysis == "combined":


            # ------------------------------------------------
            # COMBINED RISK EXPLANATION
            # ------------------------------------------------

            cards.append(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5(
                                "Combined Risk Score"
                            ),

                            html.P(
                                "Risk Factors: "
                                "Age ≥ 40 | "
                                "BMI ≥ 30 | "
                                "Glucose ≥ 140"
                            ),

                            html.P(
                                "0 = No high-risk factors"
                            ),

                            html.P(
                                "1 = One high-risk factor"
                            ),

                            html.P(
                                "2 = Two high-risk factors"
                            ),

                            html.P(
                                "3 = All three high-risk factors"
                            ),
                        ]
                    ),

                    className="combined-risk-info-card",
                )
            )


            # ------------------------------------------------
            # COMBINED RISK RESULTS
            # ------------------------------------------------

            for group in data["data"]:

                cards.append(
                    create_analysis_card(
                        title="Analysis Type: Combined Risk",
                        group_heading="Risk Count",
                        group_value=group["risk_count"],
                        group=group,
                    )
                )


        return cards