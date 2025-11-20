import dash_mantine_components as dmc
import importlib_resources
routes = importlib_resources.files('iwst')
markdown1 = routes.joinpath('routes', 'home', 'data', 'boreholeandmohrcoulomb.md').read_text()
markdown2 = routes.joinpath('routes', 'home', 'data', 'breakouts.md').read_text()
markdown3 = routes.joinpath('routes', 'home', 'data', 'tensilefracture.md').read_text()

from dash import html, dcc


notifications_container = html.Div(id="notifications-container")

info_drawer_borehole_stress_and_mohr_coulomb_plot = dmc.Drawer(
    title=html.H3("Documentation", style={"font-size": "30px", "marginTop": "0px", "marginBottom": "0px"}),
    id="info-drawer-borehole-stress-and-mohr-coulomb-plot",
    children=[
        html.Div(
            dcc.Markdown(children=markdown1),
            style={"margin-top": "-15px"} 
        )
    ],
    padding="md",
    size="lg",
    opened=False,
)

info_drawer_breakouts_polar_plot = dmc.Drawer(
    title=html.H3("Documentation", style={"font-size": "30px", "marginTop": "0px", "marginBottom": "0px"}),
    id="info-drawer-breakouts-polar-plot",
    children=[
        html.Div(
            dcc.Markdown(children=markdown2),
            style={"margin-top": "-15px"} 
        )
    ],
    padding="md",
    size="lg",
    opened=False,
)

info_drawer_tensile_fracture_polar_plot = dmc.Drawer(
    title=html.H3("Documentation", style={"font-size": "30px", "marginTop": "0px", "marginBottom": "0px"}),
    id="info-drawer-tensile-fracture-polar-plot",
    children=[
        html.Div(
            dcc.Markdown(children=markdown3),
            style={"margin-top": "-15px"} 
        )
    ],
    padding="md",
    size="lg",
    opened=False,
)