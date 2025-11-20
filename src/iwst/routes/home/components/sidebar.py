import dash_mantine_components as dmc
import numpy as np

from dash import Output, Input, State
from datetime import datetime
from iwst.routes.home.utils.defaults import DEFAULT_VALUES


sidebar = dmc.Flex(
    direction="column",
    style={"width": "200px", "marginLeft": "5px", "paddingTop": "10px"},
    children=[
        dmc.Paper(
            dmc.Flex(
                direction="column",
                gap="xs",
                children=[
                    dmc.Flex(
                        justify="space-between",
                        align="center",
                        children=[
                            dmc.Tooltip(
                                label="Maximum Principal Stress",
                                position="right",
                                withArrow=True,
                                children=[dmc.Text("σ₁ [MPa]", size="md")],
                            ),
                            dmc.NumberInput(
                                id="max-principal-stress-input",
                                value=70.0,
                                step=0.1,
                                style={"width": "80px", "height": "30px"},
                                styles={
                                    "input": {"textAlign": "right", "fontSize": "14px"},  
                                },
                                debounce=True
                            ),
                        ],
                    ),
                    dmc.Flex(
                        justify="space-between",
                        align="center",
                        children=[
                            dmc.Tooltip(
                                label="Intermediate Principal Stress",
                                position="right",
                                withArrow=True,
                                children=[dmc.Text("σ₂ [MPa]", size="md")],
                            ),
                            dmc.NumberInput(
                                id="intermediate-principal-stress-input",
                                value=67.0,
                                step=0.1,
                                style={"width": "80px", "height": "30px"},
                                styles={
                                    "input": {"textAlign": "right", "fontSize": "14px"},  
                                },
                                debounce=True
                            ),
                        ],
                    ),
                    dmc.Flex(
                        justify="space-between",
                        align="center",
                        children=[
                            dmc.Tooltip(
                                label="Minimum Principal Stress",
                                position="right",
                                withArrow=True,
                                children=[dmc.Text("σ₃ [MPa]", size="md")],
                            ),
                            dmc.NumberInput(
                                id="min-principal-stress-input",
                                value=45.0,
                                step=0.1,
                                style={"width": "80px", "height": "30px"},
                                styles={
                                    "input": {"textAlign": "right", "fontSize": "14px"},  
                                },
                                debounce=True
                            ),
                        ],
                    ),
                    dmc.Flex(
                        justify="space-between",
                        align="center",
                        children=[
                            dmc.Tooltip(
                                label="Pore Pressure",
                                position="right",
                                withArrow=True,
                                children=[dmc.Text("Pₚ [MPa]", size="md")],
                            ),
                            dmc.NumberInput(
                                id="pore-pressure-input",
                                value=32.0,
                                step=0.1,
                                style={"width": "80px", "height": "30px"},
                                styles={
                                    "input": {"textAlign": "right", "fontSize": "14px"},  
                                },
                                debounce=True
                            ),
                        ],
                    ),
                    dmc.Flex(
                        justify="space-between",
                        align="center",
                        children=[
                            dmc.Tooltip(
                                label="Mud Pressure",
                                position="right",
                                withArrow=True,
                                children=[dmc.Text("Pₘ [MPa]", size="md")],
                            ),
                            dmc.NumberInput(
                                id="mud-pressure-input",
                                value=32.0,
                                step=0.1,
                                style={"width": "80px", "height": "30px"},
                                styles={
                                    "input": {"textAlign": "right", "fontSize": "14px"},  
                                },
                                debounce=True
                            ),
                        ],
                    ),
                    dmc.Flex(
                        justify="space-between",
                        align="center",
                        children=[
                            dmc.Tooltip(
                                label="Poisson Ratio",
                                position="right",
                                withArrow=True,
                                children=[dmc.Text("ν [-]", size="md")],
                            ),
                            dmc.NumberInput(
                                id="poisson-ratio-input",
                                value=0.15,
                                step=0.01,
                                style={"width": "80px", "height": "30px"},
                                styles={
                                    "input": {"textAlign": "right", "fontSize": "14px"},  
                                },
                                debounce=True
                            ),
                        ],
                    ),
                    dmc.Flex(
                        justify="space-between",
                        align="center",
                        children=[
                            dmc.Tooltip(
                                label="Azimuth",
                                position="right",
                                withArrow=True,
                                children=[dmc.Text("δ [degrees]", size="md")],
                            ),
                            dmc.NumberInput(
                                id="azimuth-input",
                                value=90.0,
                                step=1,
                                style={"width": "80px", "height": "30px"},
                                styles={
                                    "input": {"textAlign": "right", "fontSize": "14px"},  
                                },
                                debounce=True
                            ),
                        ],
                    ),
                    dmc.Flex(
                        justify="space-between",
                        align="center",
                        children=[
                            dmc.Tooltip(
                                label="Inclination Angle",
                                position="right",
                                withArrow=True,
                                children=[dmc.Text("ϕ [degrees]", size="md")],
                            ),
                            dmc.NumberInput(
                                id="inclination-angle-input",
                                value=85.0,
                                step=1,
                                style={"width": "80px", "height": "30px"},
                                styles={
                                    "input": {"textAlign": "right", "fontSize": "14px"},  
                                },
                                debounce=True
                            ),
                        ],
                    ),
                    dmc.Flex(
                        justify="space-between",
                        align="center",
                        children=[
                            dmc.Tooltip(
                                label="Friction Coefficient",
                                position="right",
                                withArrow=True,
                                children=[dmc.Text("μ [-]", size="md")],
                            ),
                            dmc.NumberInput(
                                id="friction-coefficient-input",
                                value=1.0,
                                step=0.01,
                                style={"width": "80px", "height": "30px"},
                                styles={
                                    "input": {"textAlign": "right", "fontSize": "14px"},  
                                },
                                debounce=True
                            ),
                        ],
                    ),
                    dmc.Flex(
                        justify="space-between",
                        align="center",
                        children=[
                            dmc.Tooltip(
                                label="Alpha Angle",
                                position="right",
                                withArrow=True,
                                children=[dmc.Text("α [degrees]", size="md")],
                            ),
                            dmc.NumberInput(
                                id="alpha-angle-input",
                                value=0.0,
                                step=1,
                                style={"width": "80px", "height": "30px"},
                                styles={
                                    "input": {"textAlign": "right", "fontSize": "14px"},  
                                },
                                debounce=True
                            ),
                        ],
                    ),
                    dmc.Flex(
                        justify="space-between",
                        align="center",
                        children=[
                            dmc.Tooltip(
                                label="Beta Angle",
                                position="right",
                                withArrow=True,
                                children=[dmc.Text("β [degrees]", size="md")],
                            ),
                            dmc.NumberInput(
                                id="beta-angle-input",
                                value=90.0,
                                step=1,
                                style={"width": "80px", "height": "30px"},
                                styles={
                                    "input": {"textAlign": "right", "fontSize": "14px"},  
                                },
                                debounce=True
                            ),
                        ],
                    ),
                    dmc.Flex(
                        justify="space-between",
                        align="center",
                        children=[
                            dmc.Tooltip(
                                label="Gamma Angle",
                                position="right",
                                withArrow=True,
                                children=[dmc.Text("γ [degrees]", size="md")],
                            ),
                            dmc.NumberInput(
                                id="gamma-angle-input",
                                value=0.0,
                                step=1,
                                style={"width": "80px", "height": "30px"},
                                styles={
                                    "input": {"textAlign": "right", "fontSize": "14px"},  
                                },
                                debounce=True
                            ),
                        ],
                    ),
                    dmc.Flex(
                        justify="space-between",
                        align="center",
                        children=[
                            dmc.Tooltip(
                                label="Tensile Strength",
                                position="right",
                                withArrow=True,
                                children=[dmc.Text("T₀ [MPa]", size="md")],
                            ),
                            dmc.NumberInput(
                                id="tensile-strength-input",
                                value=0.0, 
                                step=0.1,
                                style={"width": "80px", "height": "30px"},
                                styles={
                                    "input": {"textAlign": "right", "fontSize": "14px"},  
                                },
                                debounce=True,
                                disabled=True
                            ),
                        ],
                    ),
                ],
            ),
            shadow="xs",
            radius="md",
            p="xs",
            withBorder=True,
        ),
        dmc.Button(
            "Generate plots",
            id="generate-plots-button",
            variant="gradient",
            gradient={"from":"teal", "to": "blue", "deg": 60},
            style={
                "marginTop": "15px",
            },
            disabled=False,
        ),
        dmc.Button(
            "Reset values",
            id="reset-defaults-button",
            variant="outline",
            color="red",
            style={
                "marginTop": "10px",
            },
        ),
    ],
)

def register_callbacks(app):
    @app.callback(
        Output("max-principal-stress-input", "styles"),
        Output("intermediate-principal-stress-input", "styles"),
        Output("min-principal-stress-input", "styles"),
        Output("poisson-ratio-input", "styles"),
        Output("azimuth-input", "styles"),
        Output("inclination-angle-input", "styles"),
        Output("pore-pressure-input", "styles"),
        Output("mud-pressure-input", "styles"),
        Output("friction-coefficient-input", "styles"),
        Output("alpha-angle-input", "styles"),
        Output("beta-angle-input", "styles"),
        Output("gamma-angle-input", "styles"),
        Output("tensile-strength-input", "styles"),
        Output("generate-plots-button", "disabled"),
        Output("notifications-container", "children", allow_duplicate=True),
        Input("max-principal-stress-input", "value"),
        Input("intermediate-principal-stress-input", "value"),
        Input("min-principal-stress-input", "value"),
        Input("poisson-ratio-input", "value"),
        Input("azimuth-input", "value"),
        Input("inclination-angle-input", "value"),
        Input("pore-pressure-input", "value"),
        Input("mud-pressure-input", "value"),
        Input("friction-coefficient-input", "value"),
        Input("alpha-angle-input", "value"),
        Input("beta-angle-input", "value"),
        Input("gamma-angle-input", "value"),
        Input("tensile-strength-input", "value"),
        prevent_initial_call=True,
    )
    def validate_all_inputs(
        max_stress,
        intermediate_stress,
        min_stress,
        poisson_ratio,
        azimuth,
        inclination_angle,
        pore_pressure,
        mud_pressure,
        friction_coefficient,
        alpha_angle,
        beta_angle,
        gamma_angle,
        tensile_strength,
    ):
        styles = {
            "max-principal-stress-input": {"input": {"textAlign": "right", "borderColor": "lightgray"}},
            "intermediate-principal-stress-input": {"input": {"textAlign": "right", "borderColor": "lightgray"}},
            "min-principal-stress-input": {"input": {"textAlign": "right", "borderColor": "lightgray"}},
            "poisson-ratio-input": {"input": {"textAlign": "right", "borderColor": "lightgray"}},
            "azimuth-input": {"input": {"textAlign": "right", "borderColor": "lightgray"}},
            "inclination-angle-input": {"input": {"textAlign": "right", "borderColor": "lightgray"}},
            "pore-pressure-input": {"input": {"textAlign": "right", "borderColor": "lightgray"}},
            "mud-pressure-input": {"input": {"textAlign": "right", "borderColor": "lightgray"}},
            "friction-coefficient-input": {"input": {"textAlign": "right", "borderColor": "lightgray"}},
            "alpha-angle-input": {"input": {"textAlign": "right", "borderColor": "lightgray"}},
            "beta-angle-input": {"input": {"textAlign": "right", "borderColor": "lightgray"}},
            "gamma-angle-input": {"input": {"textAlign": "right", "borderColor": "lightgray"}},
            "tensile-strength-input": {"input": {"textAlign": "right", "borderColor": "lightgray"}},
        }

        notification = None
        all_valid = True

        def is_numeric(value):
            try:
                float(value)
                return value not in ("", None)
            except (TypeError, ValueError):
                return False

        if max_stress is None or str(max_stress).strip() == "":
            styles["max-principal-stress-input"]["input"]["borderColor"] = "red"
            all_valid = False
            notification = dmc.Notification(
                title="Missing parameter",
                message="Maximum Principal Stress is required.",
                color="red",
                action="show",
                autoClose=5000,
            )
        elif not is_numeric(max_stress):
            styles["max-principal-stress-input"]["input"]["borderColor"] = "red"
            all_valid = False
            notification = dmc.Notification(
                title="Invalid Input",
                message="Maximum Principal Stress must be a valid number.",
                color="red",
                action="show",
                autoClose=5000,
            )

        if intermediate_stress is None or str(intermediate_stress).strip() == "":
            styles["intermediate-principal-stress-input"]["input"]["borderColor"] = "red"
            all_valid = False
            notification = dmc.Notification(
                title="Missing parameter",
                message="Intermediate Principal Stress is required.",
                color="red",
                action="show",
                autoClose=5000,
            )
        elif not is_numeric(intermediate_stress):
            styles["intermediate-principal-stress-input"]["input"]["borderColor"] = "red"
            all_valid = False
            notification = dmc.Notification(
                title="Invalid Input",
                message="Intermediate Principal Stress must be a valid number.",
                color="red",
                action="show",
                autoClose=5000,
            )

        if min_stress is None or str(min_stress).strip() == "":
            styles["min-principal-stress-input"]["input"]["borderColor"] = "red"
            all_valid = False
            notification = dmc.Notification(
                title="Missing parameter",
                message="Minimum Principal Stress is required.",
                color="red",
                action="show",
                autoClose=5000,
            )
        elif not is_numeric(min_stress):
            styles["min-principal-stress-input"]["input"]["borderColor"] = "red"
            all_valid = False
            notification = dmc.Notification(
                title="Invalid Input",
                message="Minimum Principal Stress must be a valid number.",
                color="red",
                action="show",
                autoClose=5000,
            )

        if is_numeric(max_stress) and is_numeric(intermediate_stress) and is_numeric(min_stress):
            try:
                max_val = float(max_stress)
                inter_val = float(intermediate_stress)
                min_val = float(min_stress)
            except (ValueError, TypeError):
                pass  
            else:
                if max_val <= inter_val or max_val <= min_val:
                    styles["max-principal-stress-input"]["input"]["borderColor"] = "red"
                    all_valid = False
                    notification = dmc.Notification(
                        title="Invalid Input",
                        message="The value of Maximum Principal Stress must be greater than the value of Intermediate Principal Stress and Minimum Principal Stress.",
                        color="red",
                        action="show",
                        autoClose=5000,
                    )

                if inter_val >= max_val or inter_val <= min_val:
                    styles["intermediate-principal-stress-input"]["input"]["borderColor"] = "red"
                    all_valid = False
                    notification = dmc.Notification(
                        title="Invalid Input",
                        message="The value of Intermediate Principal Stress must be less than the value of Maximum Principal Stress and greater than the value of Minimum Principal Stress.",
                        color="red",
                        action="show",
                        autoClose=5000,
                    )

                if min_val >= inter_val or min_val >= max_val:
                    styles["min-principal-stress-input"]["input"]["borderColor"] = "red"
                    all_valid = False
                    notification = dmc.Notification(
                        title="Invalid Input",
                        message="The value of Minimum Principal Stress must be less than the value of Intermediate Principal Stress and Maximum Principal Stress.",
                        color="red",
                        action="show",
                        autoClose=5000,
                    )
        else:
            pass  

        other_fields = {
            "poisson-ratio-input": poisson_ratio,
            "azimuth-input": azimuth,
            "inclination-angle-input": inclination_angle,
            "pore-pressure-input": pore_pressure,
            "mud-pressure-input": mud_pressure,
            "friction-coefficient-input": friction_coefficient,
            "alpha-angle-input": alpha_angle,
            "beta-angle-input": beta_angle,
            "gamma-angle-input": gamma_angle,
            "tensile-strength-input": tensile_strength,
        }

        for field_id, value in other_fields.items():
            if not is_numeric(value):
                styles[field_id]["input"]["borderColor"] = "red"
                all_valid = False
                notification = dmc.Notification(
                    title="Missing or Invalid Parameters",
                    message=f"Some required fields are missing or invalid.",
                    color="red",
                    action="show",
                    autoClose=5000,
                )

        if is_numeric(poisson_ratio):
            pr = float(poisson_ratio)
            if not (-1 <= pr <= 0.5):
                styles["poisson-ratio-input"]["input"]["borderColor"] = "red"
                all_valid = False
                notification = dmc.Notification(
                    title="Invalid Input",
                    message="Poisson Ratio must be between -1 and 0.5.",
                    color="red",
                    action="show",
                    autoClose=5000,
                )

        if is_numeric(azimuth):
            az = float(azimuth)
            if not (0 <= az <= 360):
                styles["azimuth-input"]["input"]["borderColor"] = "red"
                all_valid = False
                notification = dmc.Notification(
                    title="Invalid Input",
                    message="Azimuth must be between 0 and 360.",
                    color="red",
                    action="show",
                    autoClose=5000,
                )

        if is_numeric(inclination_angle):
            inc = float(inclination_angle)
            if not (0 <= inc <= 90):
                styles["inclination-angle-input"]["input"]["borderColor"] = "red"
                all_valid = False
                notification = dmc.Notification(
                    title="Invalid Input",
                    message="Inclination Angle must be between 0 and 90.",
                    color="red",
                    action="show",
                    autoClose=5000,
                )

        return (
            styles["max-principal-stress-input"],
            styles["intermediate-principal-stress-input"],
            styles["min-principal-stress-input"],
            styles["poisson-ratio-input"],
            styles["azimuth-input"],
            styles["inclination-angle-input"],
            styles["pore-pressure-input"],
            styles["mud-pressure-input"],
            styles["friction-coefficient-input"],
            styles["alpha-angle-input"],
            styles["beta-angle-input"],
            styles["gamma-angle-input"],
            styles["tensile-strength-input"],
            not all_valid,
            notification,
        )

    @app.callback(
        Output("max-principal-stress-input", "value"),
        Output("intermediate-principal-stress-input", "value"),
        Output("min-principal-stress-input", "value"),
        Output("pore-pressure-input", "value"),
        Output("mud-pressure-input", "value"),
        Output("poisson-ratio-input", "value"),
        Output("azimuth-input", "value"),
        Output("inclination-angle-input", "value"),
        Output("friction-coefficient-input", "value"),
        Output("alpha-angle-input", "value"),
        Output("beta-angle-input", "value"),
        Output("gamma-angle-input", "value"),
        Output("tensile-strength-input", "value"),
        Output("notifications-container", "children", allow_duplicate=True),
        Input("reset-defaults-button", "n_clicks"),
        prevent_initial_call=True,
    )
    def reset_inputs(n_clicks):
        """Reset all input values to their default values."""
        if n_clicks is None:
            raise PreventUpdate
        return (
            DEFAULT_VALUES["max-principal-stress-input"],
            DEFAULT_VALUES["intermediate-principal-stress-input"],
            DEFAULT_VALUES["min-principal-stress-input"],
            DEFAULT_VALUES["pore-pressure-input"],
            DEFAULT_VALUES["mud-pressure-input"],
            DEFAULT_VALUES["poisson-ratio-input"],
            DEFAULT_VALUES["azimuth-input"],
            DEFAULT_VALUES["inclination-angle-input"],
            DEFAULT_VALUES["friction-coefficient-input"],
            DEFAULT_VALUES["alpha-angle-input"],
            DEFAULT_VALUES["beta-angle-input"],
            DEFAULT_VALUES["gamma-angle-input"],
            DEFAULT_VALUES["tensile-strength-input"],
            dmc.Notification(
                title="Success",
                message="Input values reset",
                color="green",
                action="show",
                autoClose=3000,
            )
        )

    # @app.callback(
    #     Output("generate-plots-button", "disabled"),
    #     Output("max-principal-stress-input", "styles", allow_duplicate=True),
    #     Output("intermediate-principal-stress-input", "styles", allow_duplicate=True),
    #     Output("min-principal-stress-input", "styles", allow_duplicate=True),
    #     Output("pore-pressure-input", "styles", allow_duplicate=True),
    #     Output("mud-pressure-input", "styles", allow_duplicate=True),
    #     Output("poisson-ratio-input", "styles", allow_duplicate=True),
    #     Output("azimuth-input", "styles", allow_duplicate=True),
    #     Output("inclination-angle-input", "styles", allow_duplicate=True),
    #     Output("friction-coefficient-input", "styles", allow_duplicate=True),
    #     Output("alpha-angle-input", "styles", allow_duplicate=True),
    #     Output("beta-angle-input", "styles", allow_duplicate=True),
    #     Output("gamma-angle-input", "styles", allow_duplicate=True),
    #     Output("tensile-strength-input", "styles", allow_duplicate=True),
    #     Output("notifications-container", "children", allow_duplicate=True),
    #     Input("max-principal-stress-input", "value"),
    #     Input("intermediate-principal-stress-input", "value"),
    #     Input("min-principal-stress-input", "value"),
    #     Input("pore-pressure-input", "value"),
    #     Input("mud-pressure-input", "value"),
    #     Input("poisson-ratio-input", "value"),
    #     Input("azimuth-input", "value"),
    #     Input("inclination-angle-input", "value"),
    #     Input("friction-coefficient-input", "value"),
    #     Input("alpha-angle-input", "value"),
    #     Input("beta-angle-input", "value"),
    #     Input("gamma-angle-input", "value"),
    #     Input("tensile-strength-input", "value"),
    #     prevent_initial_call=True,
    # )
    # def validate_all_inputs(
    #     max_principal_stress,
    #     intermediate_principal_stress,
    #     min_principal_stress,
    #     pore_pressure,
    #     mud_pressure,
    #     poisson_ratio,
    #     azimuth,
    #     inclination_angle,
    #     friction_coefficient,
    #     alpha_angle,
    #     beta_angle,
    #     gamma_angle,
    #     tensile_strength,
    # ):
    #     styles = {
    #         "max-principal-stress-input": {"input": {"textAlign": "right"}},
    #         "intermediate-principal-stress-input": {"input": {"textAlign": "right"}},
    #         "min-principal-stress-input": {"input": {"textAlign": "right"}},
    #         "pore-pressure-input": {"input": {"textAlign": "right"}},
    #         "mud-pressure-input": {"input": {"textAlign": "right"}},
    #         "poisson-ratio-input": {"input": {"textAlign": "right"}},
    #         "azimuth-input": {"input": {"textAlign": "right"}},
    #         "inclination-angle-input": {"input": {"textAlign": "right"}},
    #         "friction-coefficient-input": {"input": {"textAlign": "right"}},
    #         "alpha-angle-input": {"input": {"textAlign": "right"}},
    #         "beta-angle-input": {"input": {"textAlign": "right"}},
    #         "gamma-angle-input": {"input": {"textAlign": "right"}},
    #         "tensile-strength-input": {"input": {"textAlign": "right"}},
    #     }
    #     all_valid = True
    #     for key, value in {
    #         "max-principal-stress-input": max_principal_stress,
    #         "intermediate-principal-stress-input": intermediate_principal_stress,
    #         "min-principal-stress-input": min_principal_stress,
    #         "pore-pressure-input": pore_pressure,
    #         "mud-pressure-input": mud_pressure,
    #         "poisson-ratio-input": poisson_ratio,
    #         "azimuth-input": azimuth,
    #         "inclination-angle-input": inclination_angle,
    #         "friction-coefficient-input": friction_coefficient,
    #         "alpha-angle-input": alpha_angle,
    #         "beta-angle-input": beta_angle,
    #         "gamma-angle-input": gamma_angle,
    #         "tensile-strength-input": tensile_strength,
    #     }.items():
    #         if value is None or value == "":
    #             styles[key]["input"]["borderColor"] = "red"
    #             all_valid = False
    #         else:
    #             styles[key]["input"]["borderColor"] = "lightgray"
        
    #     notification = None
    #     if not all_valid:
    #         notification = dmc.Notification(
    #             title="Warning",
    #             message="Missing parameters",
    #             color="red",
    #             action="show",
    #             autoClose=5000,
    #         )
    #     return (
    #         not all_valid,
    #         styles["max-principal-stress-input"],
    #         styles["intermediate-principal-stress-input"],
    #         styles["min-principal-stress-input"],
    #         styles["pore-pressure-input"],
    #         styles["mud-pressure-input"],
    #         styles["poisson-ratio-input"],
    #         styles["azimuth-input"],
    #         styles["inclination-angle-input"],
    #         styles["friction-coefficient-input"],
    #         styles["alpha-angle-input"],
    #         styles["beta-angle-input"],
    #         styles["gamma-angle-input"],
    #         styles["tensile-strength-input"],
    #         notification  
    #     )

    return app