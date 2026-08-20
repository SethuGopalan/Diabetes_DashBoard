# ============================================================
# IMPORTS
# Purpose:
# Build the Visualization section.
#
# Plotly chart callbacks will also be added to this file.
# ============================================================

from dash import (
    html,
    dcc,
    Input,Output
)
import requests
import plotly.express as px
# ============================================================
# API CONFIGURATION
# Purpose:
# Connect the dashboard Analysis section to FastAPI.
# ============================================================

ANALYSIS_API_URL = "http://127.0.0.1:9000/analysis"

# ============================================================
# VISUALIZATION LAYOUT
# Purpose:
# Build the Visualization controls and chart output area.
# ============================================================

def visualization_layout():

    return html.Div(
        className="visualization-container",
        children=[

            # ------------------------------------------------
            # VISUALIZATION HEADER
            # ------------------------------------------------

            html.H4(
                "Visualization",
                className="visualization-title",
            ),

            html.P(
                "Visualize the selected analysis "
                "using interactive Plotly charts.",
                className="visualization-text",
            ),


            # ------------------------------------------------
            # VISUALIZATION DROPDOWN
            # Purpose:
            # Allow visualization selection independently
            # from the Analysis dropdown.
            # ------------------------------------------------

            dcc.Dropdown(
                id="visualization-dropdown",

                options=[
                    {
                        "label": "Age Risk Visualization",
                        "value": "age",
                    },

                    {
                        "label": "Pregnancy Visualization",
                        "value": "pregnancy",
                    },

                    {
                        "label": "BMI / Obesity Visualization",
                        "value": "bmi",
                    },

                    {
                        "label": "Glucose Visualization",
                        "value": "glucose",
                    },

                    {
                        "label": "Combined Risk Visualization",
                        "value": "combined",
                    },
                ],

                value="age",

                placeholder="Select visualization type",

                className="visualization-dropdown",
            ),


            # ------------------------------------------------
            # VISUALIZATION OUTPUT
            # Purpose:
            # dcc.Graph components will appear here.
            # ------------------------------------------------

            html.Div(
                id="visualization-output",
                className="visualization-output",
                children=[
                    html.P(
                        "Visualization chart will appear here."
                    )
                ],
            ),
        ],
    )
def register_visualization_callbacks(app):
    @app.callback(
        Output(
            "visualization-output",
            "children",
        ),
        Input(
            "visualization-dropdown",
            "value"
        ),

    )
    def run_graphs(selected_graph):
        graphs=[]

        if selected_graph is None:
            return graphs
        
        # ====================================================
        # CALL FASTAPI
        # ====================================================

        analysis_url = (
            f"{ANALYSIS_API_URL}/{selected_graph}"
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

        if selected_graph == "age":
            x_values =[]
            y_values=[]
            for group in data["data"]:
                x_values.append(group["age_group"])
                y_values.append(group["diabetes_percentage"])
            figure = px.bar(
                     x=x_values,
                     y=y_values,
                     
                labels={
                        "x": "Age Group",
                        "y": "Diabetes Percentage",
                },
                title="Diabetes Risk by Age Group",
            )
            figure.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#E8EEEB"),
                title_font=dict(color="#79E0BE"),
)

            figure.update_traces(
                marker_color="#79E0BE"
            )
            return dcc.Graph(
                figure=figure
            )
        if selected_graph == "bmi":
            x_values =[]
            y_values=[]
            for group in data["data"]:
                x_values.append(group["bmi_group"])
                y_values.append(group["diabetes_percentage"])
            figure = px.bar(
                     x=x_values,
                     y=y_values,
                     
                labels={
                        "x": "Bmi Group",
                        "y": "Diabetes Percentage",
                },
                title="Diabetes Risk by Bmi Group",
            )
            figure.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#E8EEEB"),
                title_font=dict(color="#79E0BE"),
)

            figure.update_traces(
                marker_color="#79E0BE"
            )
            return dcc.Graph(
                figure=figure
            ) 
        if selected_graph == "glucose":
            x_values =[]
            y_values=[]
            for group in data["data"]:
                x_values.append(group["glucose_group"])
                y_values.append(group["diabetes_percentage"])
            figure = px.bar(
                     x=x_values,
                     y=y_values,
                     
                labels={
                        "x": "Glucose Group",
                        "y": "Diabetes Percentage",
                },
                title="Diabetes Risk by Glucose Group",
            )
            figure.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#E8EEEB"),
                title_font=dict(color="#79E0BE"),
)

            figure.update_traces(
                marker_color="#79E0BE"
            )
            return dcc.Graph(
                figure=figure
            )   
        if selected_graph == "pregnancy":
            x_values =[]
            y_values=[]
            for group in data["data"]:
                x_values.append(group["pregnancies_group"])
                y_values.append(group["diabetes_percentage"])
            figure = px.bar(
                     x=x_values,
                     y=y_values,
                     
                labels={
                        "x": "Pregnancy Group",
                        "y": "Diabetes Percentage",
                },
                title="Diabetes Risk by Pregnancy Group",
            )
            figure.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#E8EEEB"),
                title_font=dict(color="#79E0BE"),
)

            figure.update_traces(
                marker_color="#79E0BE"
            )
            return dcc.Graph(
                figure=figure
            ) 
        if selected_graph == "combined":
            x_values =[]
            y_values=[]
            risk_meanings = [
                    "No high-risk factors",
                    "One high-risk factor",
                    "Two high-risk factors",
                    "All three high-risk factors",
                ]
            for group in data["data"]:
                x_values.append(group["risk_count"])
                y_values.append(group["diabetes_percentage"])
            figure = px.bar(
                     x=x_values,
                     y=y_values,
                    hover_data={
                        "Meaning": risk_meanings,
                    },
                     
                labels={
                        "x": "Risk Count",
                        "y": "Diabetes Percentage",
                },
                title="Diabetes Risk by Risk Count ",
            )
            
            
            figure.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#E8EEEB"),
                title_font=dict(color="#79E0BE"),
)

            figure.update_traces(
                marker_color="#79E0BE"
            )
            return dcc.Graph(
                figure=figure
            )   