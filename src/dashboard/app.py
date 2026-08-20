# ============================================================
# IMPORTS
# Purpose:
# Create the main Dash application and import each
# dashboard section from its own module.
# ============================================================

from dash import Dash, html
import dash_bootstrap_components as dbc

from src.dashboard.statistics import (
    statistics_layout,
    register_statistics_callbacks,
)

from src.dashboard.risk_analysis import (
    analysis_layout,
    register_analysis_callbacks,
)
from src.dashboard.visualization import (
    visualization_layout,
    register_visualization_callbacks,
)

from src.dashboard.prediction import prediction_layout


# ============================================================
# DASH APP CONFIGURATION
# Purpose:
# Create the main Dash application.
# ============================================================

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    requests_pathname_prefix="/@sethugopalan/diabetes-dashboard.main/apps/code-server/proxy/8050/",
)


# ============================================================
# MAIN DASHBOARD LAYOUT
# Purpose:
# Assemble:
# 1. Header
# 2. Statistics
# 3. Analysis + Visualization
# 4. Prediction
# 5. Footer
# ============================================================

app.layout = dbc.Container(
    fluid=True,
    className="dashboard-container",
    children=[

        # ====================================================
        # HEADER
        # ====================================================

        dbc.Row(
            [
                dbc.Col(
                    width=12,
                    children=[
                        html.Div(
                            className="dashboard-header",
                            children=[
                                html.Div(className="ecg-left"),
                                html.H1(
                                    "Diabetic Prediction Dashboard",
                                    className="dashboard-title",
                                ),
                                html.Div(className="ecg-right"),
                            ],
                        )
                    ],
                )
            ]
        ),


        # ====================================================
        # MAIN CONTENT
        # ====================================================

        dbc.Row(
            className="main-row g-0",
            children=[

                # --------------------------------------------
                # STATISTICS COLUMN
                # --------------------------------------------

                statistics_layout(),


                # --------------------------------------------
                # ANALYSIS + VISUALIZATION COLUMN
                # --------------------------------------------

                dbc.Col(
                    width=4,
                    className="visualization-section p-0",
                    children=[

                        html.H2("Analysis & Visualization"),

                        html.P(
                            "This section allows users to perform "
                            "risk analysis and visualize numeric "
                            "relationships in the data."
                        ),

                        # Analysis module
                        analysis_layout(),

                        # Visualization module
                        visualization_layout(),
                    ],
                ),


                # --------------------------------------------
                # PREDICTION COLUMN
                # --------------------------------------------

                prediction_layout(),
            ],
        ),


        # ====================================================
        # FOOTER
        # ====================================================

        html.Footer(
            className="dashboard-footer",
            children=[
                html.P("Diabetic Prediction Dashboard"),
                html.P(
                    "Data Analysis • Visualization • "
                    "Machine Learning Prediction"
                ),
                html.P("© 2026 Terrafox AI"),
            ],
        ),
    ],
)


# ============================================================
# REGISTER CALLBACKS
# Purpose:
# Connect callbacks from the separate dashboard modules
# to the main Dash application.
# ============================================================

register_statistics_callbacks(app)

register_analysis_callbacks(app)

register_visualization_callbacks(app)

# ============================================================
# APP RUNNER
# ============================================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=True,
        port=8050,
    )