import dash_mantine_components as dmc
import numpy as np
import plotly.graph_objects as go
import dash
import base64

from dash import dcc, html, Output, Input, State
from dash.exceptions import PreventUpdate
from iwst.routes.home.utils.borehole_stress import (
    calculate_stress_matrix,
    calculate_rotation_matrix,
    calculate_rotation_matrix_azimuth_inclination,
    calculate_tangential_stress,
    plot_mohr_coulomb_failure,
    calculate_mohr_coulomb_circle,
)
from iwst.routes.home.utils.overlay import (
    info_drawer_borehole_stress_and_mohr_coulomb_plot,
    info_drawer_breakouts_polar_plot,
    info_drawer_tensile_fracture_polar_plot,
)
from iwst.routes.home.utils.polar_plot_borehole import generate_plot as generate_polar_plot_borehole
from iwst.routes.home.utils.polar_tensile import generate_plot as generate_polar_plot_tensile
from iwst.routes.home.utils.defaults import DEFAULT_VALUES 
from dash_iconify import DashIconify

borehole_stress_layout = html.Div(
    children=[
        dmc.Flex(
            justify="center",
            align="center",
            direction="column",
            style={"marginTop": "10px", "marginBottom": "10px"},
            children=[
                dmc.Text(
                    "The plot on the left shows variation of effective principal stresses, tangential stress and axial stress, around a wellbore wall as a function of azimuth and inclination. The plot on the right shows three-dimensional Mohr diagram of the principal stresses around the wellbore wall at the point of maximum stress concentration.",
                    style={"textAlign": "center", "marginBottom": "10px", "fontSize": "15px"},
                ),
                dmc.Divider(style={"width": "100%", "marginBottom": "10px"}),
            ],
        ),
        dmc.Flex(
            justify="space-between",
            align="center",
            style={"marginBottom": "5px"},
            children=[
                dmc.Button(
                    "Download plot",
                    id="download-borehole-stress-button",
                    variant="outline",
                    color="blue",
                    style={"marginLeft": "10px"},
                ),
                dmc.Button(
                    "Download plot",
                    id="download-mohr-coulomb-button",
                    variant="outline",
                    color="blue",
                    style={"marginLeft": "10px"},
                ),
            ],
        ),
        dcc.Download(id="download-borehole-stress"),
        dcc.Download(id="download-mohr-coulomb"),
        dcc.Loading(
            dmc.Flex(
                gap="lg",
                justify="space-between",
                align="flex-start",
                children=[
                    dcc.Graph(
                        id="borehole-stress-plot",
                        style={"height": "400px", "width": "100%"},
                        mathjax=True,
                        config={"modeBarButtonsToRemove": ["toImage"]},
                    ),
                    dcc.Graph(
                        id="mohr-coulomb-plot",
                        style={"height": "400px", "width": "100%"},
                        mathjax=True,
                        config={"modeBarButtonsToRemove": ["toImage"]},
                    ),
                ],
            ),
        ),
    ],
)

polar_plot_borehole_layout = html.Div(
    children=[
        dmc.Flex(
            justify="center",
            align="center",
            direction="column",
            style={"marginTop": "10px", "marginBottom": "10px"},
            children=[
                dmc.Text(
                    "This plot shows the tendency for the initiation of wellbore breakouts in wells of different orientation and inclinations. The color indicates the rock strength required to prevent failure.",
                    style={"textAlign": "center", "marginBottom": "10px", "fontSize": "15px"},
                ),
                dmc.Divider(style={"width": "100%", "marginBottom": "10px"}),
            ],
        ),
        dmc.Flex(
            justify="flex-start",
            align="center",
        ),
        dmc.Flex(
            justify="space-between",
            align="center",
            style={"marginBottom": "5px"},
            children=[
                dmc.Button(
                    "Download plot",
                    id="download-breakouts-polar-button",
                    variant="outline",
                    color="blue",
                    style={"marginLeft": "10px"},
                ),
            ],
        ),
        dcc.Download(id="download-breakouts-polar"),
        dmc.Flex(
            justify="center",
            align="center",
            children=[
                dcc.Loading(
                    children=[
                        html.Img(
                            id="breakouts-polar-plot",
                            src="",
                            style={"height": "500px", "width": "100%"},
                        ),
                    ],
                ),
            ],
        ),
    ],
)

polar_tensile_layout = html.Div(
    children=[
        dmc.Flex(
            justify="center",
            align="center",
            direction="column",
            style={"marginTop": "10px", "marginBottom": "10px"},
            children=[
                dmc.Text(
                    "This plot shows the tendency for the initiation of tensile fractures to form in wells of different orientation and inclinations. The color indicates the mud pressure required to initiate tensile failure.",
                    style={"textAlign": "center", "marginBottom": "10px", "fontSize": "15px"},
                ),
                dmc.Divider(style={"width": "100%", "marginBottom": "10px"}),
            ],
        ),
        dmc.Flex(
            justify="flex-start",
            align="center",
        ),
        dmc.Flex(
            justify="space-between",
            align="center",
            style={"marginBottom": "5px"},
            children=[
                dmc.Button(
                    "Download plot",
                    id="download-tensile-fracture-polar-button",
                    variant="outline",
                    color="blue",
                    style={"marginLeft": "10px"},
                ),
            ],
        ),
        dcc.Download(id="download-tensile-fracture-polar"),
        dmc.Flex(
            justify="center",
            align="center",
            children=[
                dcc.Loading(
                    children=[
                        html.Img(
                            id="tensile-fracture-polar-plot",
                            src="",
                            style={"height": "500px", "width": "100%"},
                        ),
                    ],
                ),
            ],
        ),
    ],
)

tabs = dmc.Flex(
    direction="column",
    gap="md",
    style={"width": "100%", "padding": "5px", "marginLeft": "25px", "marginRight": "25px"},
    children=[
        dmc.Tabs(
            [
                dmc.TabsList(
                    [
                        dmc.TabsTab(
                            dmc.Group(
                                [
                                    "Interactive Borehole Stress and Mohr-Coulomb Plot",
                                    dmc.ActionIcon(
                                        dmc.ThemeIcon(
                                            DashIconify(icon="mdi:information-outline", width=16),
                                            size="xs",
                                            variant="light",
                                            color="gray",
                                            style={"backgroundColor": "white"},
                                        ),
                                        id="info-icon-borehole-stress-and-mohr-coulomb-plot",
                                        variant="transparent",
                                    ),
                                ],
                                gap="xs",
                            ),
                            value="tab1",
                            style={"fontSize": "17px", "fontWeight": "bold"},
                        ),
                        dmc.TabsTab(
                            dmc.Group(
                                [
                                    "Breakouts Polar Plot",
                                    dmc.ActionIcon(
                                        dmc.ThemeIcon(
                                            DashIconify(icon="mdi:information-outline", width=16),
                                            size="xs",
                                            variant="light",
                                            color="gray",
                                            style={"backgroundColor": "white"},
                                        ),
                                        id="info-icon-breakouts-polar-plot",
                                        variant="transparent",
                                    ),
                                ],
                                gap="xs",
                            ),
                            value="tab2",
                            style={"fontSize": "17px", "fontWeight": "bold"},
                        ),
                        dmc.TabsTab(
                            dmc.Group(
                                [
                                    "Tensile Fracture Polar Plot",
                                    dmc.ActionIcon(
                                        dmc.ThemeIcon(
                                            DashIconify(icon="mdi:information-outline", width=16),
                                            size="xs",
                                            variant="light",
                                            color="gray",
                                            style={"backgroundColor": "white"},
                                        ),
                                        id="info-icon-tensile-fracture-polar-plot",
                                        variant="transparent",
                                    ),
                                ],
                                gap="xs",
                            ),
                            value="tab3",
                            style={"fontSize": "17px", "fontWeight": "bold"},
                        ),
                    ],
                    style={"justifyContent": "center"},
                ),
                dmc.TabsPanel(borehole_stress_layout, value="tab1"),
                dmc.TabsPanel(polar_plot_borehole_layout, value="tab2"),
                dmc.TabsPanel(polar_tensile_layout, value="tab3"),
            ],
            value="tab1",
            orientation="horizontal",
            variant="outline",
            id="tabs",
        ),
        info_drawer_borehole_stress_and_mohr_coulomb_plot,
        info_drawer_breakouts_polar_plot,
        info_drawer_tensile_fracture_polar_plot,
    ],
)

def register_callbacks(app):
    @app.callback(
        Output("borehole-stress-plot", "figure"),
        Output("mohr-coulomb-plot", "figure"),
        Output("notifications-container", "children"),
        Input("generate-plots-button", "n_clicks"),  # Callback triggered only by the button
        State("pore-pressure-input", "value"),  # Read input values without triggering the callback
        State("mud-pressure-input", "value"),
        State("max-principal-stress-input", "value"),
        State("intermediate-principal-stress-input", "value"),
        State("min-principal-stress-input", "value"),
        State("poisson-ratio-input", "value"),
        State("inclination-angle-input", "value"),
        State("azimuth-input", "value"),
        State("friction-coefficient-input", "value"),
        State("alpha-angle-input", "value"),
        State("beta-angle-input", "value"),
        State("gamma-angle-input", "value"),
        prevent_initial_call=False,  # Allows the callback to execute at startup
        running=[
            (Output("generate-plots-button", "disabled"), True, False),
        ],
    )
    def generate_borehole_stress_and_mohr_coulomb_plots(
        n_clicks, 
        pore_pressure, 
        mud_pressure, 
        max_principal_stress, 
        intermediate_principal_stress,
        min_principal_stress, 
        poisson_ratio, 
        inclination_angle, 
        azimuth, 
        friction_coefficient,
        alpha_angle, 
        beta_angle, 
        gamma_angle
    ):

        if n_clicks is None:
            pore_pressure = DEFAULT_VALUES["pore-pressure-input"]
            mud_pressure = DEFAULT_VALUES["mud-pressure-input"]
            max_principal_stress = DEFAULT_VALUES["max-principal-stress-input"]
            intermediate_principal_stress = DEFAULT_VALUES["intermediate-principal-stress-input"]
            min_principal_stress = DEFAULT_VALUES["min-principal-stress-input"]
            poisson_ratio = DEFAULT_VALUES["poisson-ratio-input"]
            inclination_angle = DEFAULT_VALUES["inclination-angle-input"]
            azimuth = DEFAULT_VALUES["azimuth-input"]
            friction_coefficient = DEFAULT_VALUES["friction-coefficient-input"]
            alpha_angle = DEFAULT_VALUES["alpha-angle-input"]
            beta_angle = DEFAULT_VALUES["beta-angle-input"]
            gamma_angle = DEFAULT_VALUES["gamma-angle-input"]

        """Update the plots when the button is clicked or at startup."""
        if n_clicks is None:  # If the button has never been pressed, use default values
            max_principal_stress = max_principal_stress - pore_pressure
            intermediate_principal_stress = intermediate_principal_stress - pore_pressure
            min_principal_stress = min_principal_stress - pore_pressure
            pressure_difference = mud_pressure - pore_pressure
            stress_matrix = calculate_stress_matrix(
                max_principal_stress, intermediate_principal_stress, min_principal_stress
            )
            rotation_matrix_global = calculate_rotation_matrix(
                alpha_angle, beta_angle, gamma_angle
            )
            transformed_stress_global = (
                rotation_matrix_global.T @ stress_matrix @ rotation_matrix_global
            )
            rotation_matrix_borehole = calculate_rotation_matrix_azimuth_inclination(
                azimuth, inclination_angle
            )
            transformed_stress_borehole = (
                rotation_matrix_borehole @ rotation_matrix_global.T @ stress_matrix
                @ rotation_matrix_global @ rotation_matrix_borehole.T
            )
            theta_angles = np.arange(0, 360, 0.1)
            max_tangential, min_tangential, normal_zz, normal_tt = calculate_tangential_stress(
                transformed_stress_borehole, theta_angles, poisson_ratio, pressure_difference
            )
            fig_stress = go.Figure()
            fig_stress.add_trace(go.Scatter(
                x=theta_angles, y=normal_zz,
                mode='lines', name='Axial Stress (σzz)',
                line=dict(color='#1f77b4', width=2)
            ))
            fig_stress.add_trace(go.Scatter(
                x=theta_angles, y=normal_tt,
                mode='lines', name='Tangential Stress (σθθ)',
                line=dict(color='#2ca02c', width=2)
            ))
            fig_stress.add_trace(go.Scatter(
                x=theta_angles, y=max_tangential,
                mode='lines', name='Max Tangential Stress',
                line=dict(color='#d62728', width=2, dash='dash')
            ))
            fig_stress.add_trace(go.Scatter(
                x=theta_angles, y=min_tangential,
                mode='lines', name='Min Tangential Stress',
                line=dict(color='black', width=2, dash='dot')
            ))
            fig_stress.update_layout(
                xaxis_title='Theta [deg]',
                yaxis_title='Stress [MPa]',
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.4,
                    xanchor="center",
                    x=0.5,
                    traceorder="normal",
                    itemsizing="constant",
                    itemwidth=40,
                    font=dict(size=12),
                ),
                template='plotly_white',
                font=dict(size=14),
                xaxis=dict(showgrid=True, gridcolor='lightgrey'),
                yaxis=dict(showgrid=True, gridcolor='lightgrey'),
                margin=dict(l=50, r=50, t=50, b=100),
            )
            unconfined_compressive_strength = plot_mohr_coulomb_failure(
                np.max(max_tangential), np.max(min_tangential), pressure_difference, friction_coefficient
            )
            fig_mohr_coulomb = go.Figure()
            x_coords_max_min, y_coords_max_min = calculate_mohr_coulomb_circle(
                np.max(max_tangential), pressure_difference
            )
            x_coords_max_intermediate, y_coords_max_intermediate = calculate_mohr_coulomb_circle(
                np.max(max_tangential), np.max(min_tangential)
            )
            x_coords_intermediate_min, y_coords_intermediate_min = calculate_mohr_coulomb_circle(
                np.max(min_tangential), pressure_difference
            )
            x_coords_max_min, y_coords_max_min = x_coords_max_min[::100], y_coords_max_min[::100]
            x_coords_max_intermediate, y_coords_max_intermediate = x_coords_max_intermediate[::100], y_coords_max_intermediate[::100]
            x_coords_intermediate_min, y_coords_intermediate_min = x_coords_intermediate_min[::100], y_coords_intermediate_min[::100]
            fig_mohr_coulomb.add_trace(go.Scatter(
                x=x_coords_max_min, y=y_coords_max_min,
                mode='lines', name=r'$\sigma_{\theta\theta} - \sigma_{rr}$',
                line=dict(color='#d62728', width=2)
            ))
            fig_mohr_coulomb.add_trace(go.Scatter(
                x=x_coords_max_intermediate, y=y_coords_max_intermediate,
                mode='lines', name=r'$\sigma_{\theta\theta} - \sigma_{zz}$',
                line=dict(color='#1f77b4', width=2)
            ))
            fig_mohr_coulomb.add_trace(go.Scatter(
                x=x_coords_intermediate_min, y=y_coords_intermediate_min,
                mode='lines', name=r'$\sigma_{zz} - \sigma_{rr}$',
                line=dict(color='#2ca02c', width=2)
            ))
            intercept = (
                (np.max(max_tangential) - pressure_difference)
                / 2 / ((friction_coefficient**2 + 1)**0.5 + friction_coefficient)
            )
            x_failure = np.linspace(0, np.max(max_tangential) * 1.5, 100)
            y_failure = x_failure * friction_coefficient + intercept
            fig_mohr_coulomb.add_trace(go.Scatter(
                x=x_failure, y=y_failure,
                mode='lines', name='Failure Envelope',
                line=dict(color='#2f2f2f', width=2)
            ))
            fig_mohr_coulomb.update_layout(
                xaxis_title=r'Effective stress [MPa]',
                yaxis_title=r'Shear stress [MPa]',
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.4,
                    xanchor="center",
                    x=0.5,
                    traceorder="normal",
                    itemsizing="constant",
                    itemwidth=40,
                    font=dict(size=12),
                ),
                xaxis_range=[0, np.max(max_tangential) * 1.5],
                yaxis_range=[0, np.max(max_tangential)],
                template='plotly_white',
                font=dict(size=14),
                xaxis=dict(showgrid=True, gridcolor='lightgrey'),
                yaxis=dict(showgrid=True, gridcolor='lightgrey'),
                margin=dict(l=50, r=50, t=50, b=100),
                yaxis_scaleanchor="x",
                yaxis_scaleratio=1,
            )
            return (
                fig_stress, 
                fig_mohr_coulomb, 
                dmc.Notification(
                    title="Success",
                    message="Graphs generated correctly",
                    color="green",
                    action="show",
                )
            )
        else:  # If the button has been pressed, generate graphs with new values
            max_principal_stress = max_principal_stress - pore_pressure
            intermediate_principal_stress = intermediate_principal_stress - pore_pressure
            min_principal_stress = min_principal_stress - pore_pressure
            pressure_difference = mud_pressure - pore_pressure
            stress_matrix = calculate_stress_matrix(
                max_principal_stress, intermediate_principal_stress, min_principal_stress
            )
            rotation_matrix_global = calculate_rotation_matrix(
                alpha_angle, beta_angle, gamma_angle
            )
            transformed_stress_global = (
                rotation_matrix_global.T @ stress_matrix @ rotation_matrix_global
            )
            rotation_matrix_borehole = calculate_rotation_matrix_azimuth_inclination(
                azimuth, inclination_angle
            )
            transformed_stress_borehole = (
                rotation_matrix_borehole @ rotation_matrix_global.T @ stress_matrix
                @ rotation_matrix_global @ rotation_matrix_borehole.T
            )
            theta_angles = np.arange(0, 360, 0.1)
            max_tangential, min_tangential, normal_zz, normal_tt = calculate_tangential_stress(
                transformed_stress_borehole, theta_angles, poisson_ratio, pressure_difference
            )
            fig_stress = go.Figure()
            fig_stress.add_trace(go.Scatter(
                x=theta_angles, y=normal_zz / max_principal_stress,
                mode='lines', name='Axial Stress (Szz)',
                line=dict(color='#1f77b4', width=2)
            ))
            fig_stress.add_trace(go.Scatter(
                x=theta_angles, y=normal_tt / max_principal_stress,
                mode='lines', name='Tangential Stress (Stt)',
                line=dict(color='#2ca02c', width=2)
            ))
            fig_stress.add_trace(go.Scatter(
                x=theta_angles, y=max_tangential / max_principal_stress,
                mode='lines', name='Max Tangential Stress (TsMax)',
                line=dict(color='#d62728', width=2, dash='dash')
            ))
            fig_stress.add_trace(go.Scatter(
                x=theta_angles, y=min_tangential / max_principal_stress,
                mode='lines', name='Min Tangential Stress (TsMin)',
                line=dict(color='black', width=2, dash='dot')
            ))
            fig_stress.update_layout(
                xaxis_title='theta [deg]',
                yaxis_title='Stress [MPa]',
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.4,
                    xanchor="center",
                    x=0.5,
                    traceorder="normal",
                    itemsizing="constant",
                    itemwidth=40,
                    font=dict(size=12),
                ),
                template='plotly_white',
                font=dict(size=14),
                xaxis=dict(showgrid=True, gridcolor='lightgrey'),
                yaxis=dict(showgrid=True, gridcolor='lightgrey'),
                margin=dict(l=50, r=50, t=50, b=100),
            )
            unconfined_compressive_strength = plot_mohr_coulomb_failure(
                np.max(max_tangential), np.max(min_tangential), pressure_difference, friction_coefficient
            )
            fig_mohr_coulomb = go.Figure()
            x_coords_max_min, y_coords_max_min = calculate_mohr_coulomb_circle(
                np.max(max_tangential), pressure_difference
            )
            x_coords_max_intermediate, y_coords_max_intermediate = calculate_mohr_coulomb_circle(
                np.max(max_tangential), np.max(min_tangential)
            )
            x_coords_intermediate_min, y_coords_intermediate_min = calculate_mohr_coulomb_circle(
                np.max(min_tangential), pressure_difference
            )
            x_coords_max_min, y_coords_max_min = x_coords_max_min[::100], y_coords_max_min[::100]
            x_coords_max_intermediate, y_coords_max_intermediate = x_coords_max_intermediate[::100], y_coords_max_intermediate[::100]
            x_coords_intermediate_min, y_coords_intermediate_min = x_coords_intermediate_min[::100], y_coords_intermediate_min[::100]
            fig_mohr_coulomb.add_trace(go.Scatter(
                x=x_coords_max_min, y=y_coords_max_min,
                mode='lines', name='Max-Min Circle',
                line=dict(color='#d62728', width=2)
            ))
            fig_mohr_coulomb.add_trace(go.Scatter(
                x=x_coords_max_intermediate, y=y_coords_max_intermediate,
                mode='lines', name='Max-Intermediate Circle',
                line=dict(color='#1f77b4', width=2)
            ))
            fig_mohr_coulomb.add_trace(go.Scatter(
                x=x_coords_intermediate_min, y=y_coords_intermediate_min,
                mode='lines', name='Intermediate-Min Circle',
                line=dict(color='#2ca02c', width=2)
            ))
            intercept = (
                (np.max(max_tangential) - pressure_difference)
                / 2 / ((friction_coefficient**2 + 1)**0.5 + friction_coefficient)
            )
            x_failure = np.linspace(0, np.max(max_tangential) * 1.5, 100)
            y_failure = x_failure * friction_coefficient + intercept
            fig_mohr_coulomb.add_trace(go.Scatter(
                x=x_failure, y=y_failure,
                mode='lines', name='Failure Envelope',
                line=dict(color='#2f2f2f', width=2)
            ))
            fig_mohr_coulomb.update_layout(
                xaxis_title=r'Effective stress [MPa]',
                yaxis_title=r'Shear stress [MPa]',
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.4,
                    xanchor="center",
                    x=0.5,
                    traceorder="normal",
                    itemsizing="constant",
                    itemwidth=40,
                    font=dict(size=12),
                ),
                xaxis_range=[0, np.max(max_tangential) * 1.5],
                yaxis_range=[0, np.max(max_tangential)],
                template='plotly_white',
                font=dict(size=14),
                xaxis=dict(showgrid=True, gridcolor='lightgrey'),
                yaxis=dict(showgrid=True, gridcolor='lightgrey'),
                margin=dict(l=50, r=50, t=50, b=100),
                yaxis_scaleanchor="x",
                yaxis_scaleratio=1,
            )
            return (
                fig_stress, 
                fig_mohr_coulomb, 
                dmc.Notification(
                    title="Success",
                    message="Graphs generated correctly",
                    color="green",
                    action="show",
                    autoClose=5000,
                )
            )

    @app.callback(
        Output("breakouts-polar-plot", "src"),
        Input("generate-plots-button", "n_clicks"),  # Callback triggered only by the button
        State("pore-pressure-input", "value"),  # Read input values without triggering the callback
        State("mud-pressure-input", "value"),
        State("max-principal-stress-input", "value"),
        State("intermediate-principal-stress-input", "value"),
        State("min-principal-stress-input", "value"),
        State("poisson-ratio-input", "value"),
        State("inclination-angle-input", "value"),
        State("azimuth-input", "value"),
        State("friction-coefficient-input", "value"),
        State("alpha-angle-input", "value"),
        State("beta-angle-input", "value"),
        State("gamma-angle-input", "value"),
        prevent_initial_call=False,  # Allows the callback to execute at startup
        running=[
            (Output("generate-plots-button", "disabled"), True, False),
        ],
    )
    def generate_breakouts_polar_plot(
        n_clicks, 
        pore_pressure, 
        mud_pressure, 
        s1, 
        s2, 
        s3,
        poisson_ratio, 
        inclination_angle, 
        azimuth, 
        friction_coefficient, 
        alpha_angle, 
        beta_angle, 
        gamma_angle
    ):
        """Update the plot when the button is clicked or at startup.
        """
        if n_clicks is None:  # If the button has never been pressed, use default values
            image_base64 = generate_polar_plot_borehole(
                pore_pressure, 
                mud_pressure, 
                s1, 
                s2, 
                s3,
                poisson_ratio, 
                friction_coefficient, 
                alpha_angle, 
                beta_angle, 
                gamma_angle, 
                specific_azimuth=azimuth, 
                specific_inclination=inclination_angle
            )
        else:  # If the button has been pressed, generate graphs with new values
            image_base64 = generate_polar_plot_borehole(
                pore_pressure, 
                mud_pressure, 
                s1, 
                s2, 
                s3,
                poisson_ratio, 
                friction_coefficient, 
                alpha_angle, 
                beta_angle, 
                gamma_angle, 
                specific_azimuth=azimuth, 
                specific_inclination=inclination_angle
            )
        return f"data:image/png;base64,{image_base64}"

    @app.callback(
        Output("tensile-fracture-polar-plot", "src"),
        Input("generate-plots-button", "n_clicks"),  # Callback triggered only by the button
        State("pore-pressure-input", "value"),  # Read input values without triggering the callback
        State("mud-pressure-input", "value"),
        State("max-principal-stress-input", "value"),
        State("intermediate-principal-stress-input", "value"),
        State("min-principal-stress-input", "value"),
        State("poisson-ratio-input", "value"),
        State("inclination-angle-input", "value"),
        State("azimuth-input", "value"),
        State("friction-coefficient-input", "value"),
        State("alpha-angle-input", "value"),
        State("beta-angle-input", "value"),
        State("gamma-angle-input", "value"),
        State("tensile-strength-input", "value"),
        prevent_initial_call=False,  # Allows the callback to execute at startup
        running=[
            (Output("generate-plots-button", "disabled"), True, False),
        ],
    )
    def generate_tensile_fracture_polar_plot(
        n_clicks, 
        pore_pressure, 
        mud_pressure, 
        s1, 
        s2, 
        s3,
        poisson_ratio, 
        inclination_angle, 
        azimuth, 
        friction_coefficient, 
        alpha_angle, 
        beta_angle, 
        gamma_angle, 
        tensile_strength
    ):
        """Update the plot when the button is clicked or at startup."""
        if n_clicks is None:  # If the button has never been pressed, use default values
            image_base64 = generate_polar_plot_tensile(
                pore_pressure, mud_pressure, s1, s2, s3,
                poisson_ratio, tensile_strength, alpha_angle, beta_angle, gamma_angle, specific_azimuth=azimuth, specific_inclination=inclination_angle
            )
        else:  # If the button has been pressed, generate graphs with new values
            image_base64 = generate_polar_plot_tensile(
                pore_pressure, mud_pressure, s1, s2, s3,
                poisson_ratio, tensile_strength, alpha_angle, beta_angle, gamma_angle, specific_azimuth=azimuth, specific_inclination=inclination_angle
            )
        return f"data:image/png;base64,{image_base64}"

    @app.callback(
        Output("tensile-strength-input", "disabled"),  
        Input("tabs", "value"),
    )
    def handle_tensile_strength_input(active_tab):
        if active_tab != "tab3":
            return True
        return False

    @app.callback(
        Output("borehole-stress-plot", "figure", allow_duplicate=True),
        Output("mohr-coulomb-plot", "figure", allow_duplicate=True),
        Output("breakouts-polar-plot", "src", allow_duplicate=True),
        Output("tensile-fracture-polar-plot", "src", allow_duplicate=True),
        Input("project-data", "data"),  # Triggered when project data is loaded
        prevent_initial_call=True,
    )
    def update_graphs_from_project_data(data):
        if not data or "inputs" not in data:
            raise PreventUpdate

        inputs = data["inputs"]
        pore_pressure = inputs.get("pore_pressure", 0)
        mud_pressure = inputs.get("mud_pressure", 0)
        max_principal_stress = inputs.get("max_principal_stress", 0)
        intermediate_principal_stress = inputs.get("intermediate_principal_stress", 0)
        min_principal_stress = inputs.get("min_principal_stress", 0)
        poisson_ratio = inputs.get("poisson_ratio", 0)
        inclination_angle = inputs.get("inclination_angle", 0)
        azimuth = inputs.get("azimuth", 0)
        friction_coefficient = inputs.get("friction_coefficient", 0)
        alpha_angle = inputs.get("alpha_angle", 0)
        beta_angle = inputs.get("beta_angle", 0)
        gamma_angle = inputs.get("gamma_angle", 0)
        tensile_strength = inputs.get("tensile_strength", 0)

        # Generate borehole stress and Mohr-Coulomb plots
        fig_stress, fig_mohr_coulomb, _ = generate_borehole_stress_and_mohr_coulomb_plots(
            None,  # Simulate no button click
            pore_pressure,
            mud_pressure,
            max_principal_stress,
            intermediate_principal_stress,
            min_principal_stress,
            poisson_ratio,
            inclination_angle,
            azimuth,
            friction_coefficient,
            alpha_angle,
            beta_angle,
            gamma_angle,
        )

        # Generate breakouts polar plot
        image_base64_breakouts = generate_polar_plot_borehole(
            pore_pressure,
            mud_pressure,
            max_principal_stress,
            intermediate_principal_stress,
            min_principal_stress,
            poisson_ratio,
            friction_coefficient,
            alpha_angle,
            beta_angle,
            gamma_angle,
            specific_azimuth=azimuth,
            specific_inclination=inclination_angle,
        )
        breakouts_src = f"data:image/png;base64,{image_base64_breakouts}"

        # Generate tensile fracture polar plot
        image_base64_tensile = generate_polar_plot_tensile(
            pore_pressure,
            mud_pressure,
            max_principal_stress,
            intermediate_principal_stress,
            min_principal_stress,
            poisson_ratio,
            tensile_strength,
            alpha_angle,
            beta_angle,
            gamma_angle,
            specific_azimuth=azimuth,
            specific_inclination=inclination_angle,
        )
        tensile_src = f"data:image/png;base64,{image_base64_tensile}"

        return fig_stress, fig_mohr_coulomb, breakouts_src, tensile_src

    @app.callback(
        Output("download-borehole-stress", "data"),
        Output("notifications-container", "children", allow_duplicate=True),
        Input("download-borehole-stress-button", "n_clicks"),
        State("borehole-stress-plot", "figure"),
        prevent_initial_call=True,
        running=[
            (Output("download-borehole-stress-button", "disabled"), True, False),
        ],
    )
    def download_borehole_stress_plot(n_clicks, figure):
        if n_clicks is None:
            raise PreventUpdate
        return (
            dcc.send_bytes(go.Figure(figure).to_image(format="png"), filename="borehole_stress_plot.png"),
            dmc.Notification(
                title="Success",
                message="Plot downloaded successfully",
                color="green",
                action="show",
                autoClose=5000,
            )
        )

    @app.callback(
        Output("download-mohr-coulomb", "data"),
        Output("notifications-container", "children", allow_duplicate=True),
        Input("download-mohr-coulomb-button", "n_clicks"),
        State("mohr-coulomb-plot", "figure"),
        prevent_initial_call=True,
        running=[
            (Output("download-mohr-coulomb-button", "disabled"), True, False),
        ],
    )
    def download_mohr_coulomb_plot(n_clicks, figure):
        if n_clicks is None:
            raise PreventUpdate
        return (
            dcc.send_bytes(go.Figure(figure).to_image(format="png"), filename="mohr_coulomb_plot.png"),
            dmc.Notification(
                title="Success",
                message="Plot downloaded successfully",
                color="green",
                action="show",
                autoClose=5000,
            )
        )

    @app.callback(
        Output("download-breakouts-polar", "data"),
        Output("notifications-container", "children", allow_duplicate=True),
        Input("download-breakouts-polar-button", "n_clicks"),
        State("breakouts-polar-plot", "src"),
        prevent_initial_call=True,
        running=[
            (Output("download-breakouts-polar-button", "disabled"), True, False),
        ],
    )
    def download_breakouts_polar_plot(n_clicks, src):
        if n_clicks is None:
            raise PreventUpdate
        image_data = base64.b64decode(src.split(",")[1])
        return (
            dcc.send_bytes(image_data, filename="breakouts_polar_plot.png"),
            dmc.Notification(
                title="Success",
                message="Plot downloaded successfully",
                color="green",
                action="show",
                autoClose=5000,
            )
        )

    @app.callback(
        Output("download-tensile-fracture-polar", "data"),
        Output("notifications-container", "children", allow_duplicate=True),
        Input("download-tensile-fracture-polar-button", "n_clicks"),
        State("tensile-fracture-polar-plot", "src"),
        prevent_initial_call=True,
        running=[
            (Output("download-tensile-fracture-polar-button", "disabled"), True, False),
        ],
    )
    def download_tensile_fracture_polar_plot(n_clicks, src):
        if n_clicks is None:
            raise PreventUpdate
        image_data = base64.b64decode(src.split(",")[1])
        return (
            dcc.send_bytes(image_data, filename="tensile_fracture_polar_plot.png"),
            dmc.Notification(
                title="Success",
                message="Plot downloaded successfully",
                color="green",
                action="show",
                autoClose=5000,
            )
        )

    @app.callback(
        Output("info-drawer-borehole-stress-and-mohr-coulomb-plot", "opened"),
        Input("info-icon-borehole-stress-and-mohr-coulomb-plot", "n_clicks"),
        State("info-drawer-borehole-stress-and-mohr-coulomb-plot", "opened"),
        prevent_initial_call=True,
    )
    def _info_drawer_borehole_stress_and_mohr_coulomb_plots(n_clicks, opened):
        return not opened

    @app.callback(
        Output("info-drawer-breakouts-polar-plot", "opened"),
        Input("info-icon-breakouts-polar-plot", "n_clicks"),
        State("info-drawer-breakouts-polar-plot", "opened"),
        prevent_initial_call=True,
    )
    def info_drawer_breakouts_polar_plot(n_clicks, opened):
        return not opened

    @app.callback(
        Output("info-drawer-tensile-fracture-polar-plot", "opened"),
        Input("info-icon-tensile-fracture-polar-plot", "n_clicks"),
        State("info-drawer-tensile-fracture-polar-plot", "opened"),
        prevent_initial_call=True,
    )
    def info_drawer_tensile_fracture_polar_plot(n_clicks, opened):
        return not opened
    
    return app