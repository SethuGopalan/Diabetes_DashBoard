# ============================================================
# IMPORTS
# Purpose:
# Build the Prediction dashboard section.
# ============================================================

from dash import html

import dash_bootstrap_components as dbc


# ============================================================
# PREDICTION LAYOUT
# Purpose:
# Build the Prediction column.
#
# Later this module will contain:
# - Patient input controls
# - Prediction button
# - Model information
# - Diabetes probability
# - Prediction results
# ============================================================

def prediction_layout():

    return dbc.Col(
        width=4,
        className="prediction-section p-0",
        children=[

            # ------------------------------------------------
            # PREDICTION HEADER
            # ------------------------------------------------

            html.H2("Prediction"),


            # ------------------------------------------------
            # PREDICTION DESCRIPTION
            # ------------------------------------------------

            html.P(
                "This section will allow users "
                "to enter patient values and "
                "view diabetes prediction results."
            ),


            # ------------------------------------------------
            # PREDICTION OUTPUT
            # Purpose:
            # Future prediction results will appear here.
            # ------------------------------------------------

            html.Div(
                id="prediction-output",
                className="prediction-output",
                children=[],
            ),
        ],
    )