import dash_mantine_components as dmc

from dash import html, dcc
from iwst.routes.home.components.toolbar import toolbar
from iwst.routes.home.components.sidebar import sidebar
from iwst.routes.home.components.tabs import tabs
from iwst.routes.home.utils.overlay import notifications_container


layout = dmc.MantineProvider(
    theme={"colorScheme": "light"},
    children=[
        dmc.NotificationProvider(position="top-right"),
        notifications_container,
        toolbar,
        html.Div(
            id="placeholder-output",
            style={"display": "none"},  
        ),
        dcc.Store(id="project-data", storage_type="memory"),
        dmc.Flex(
            align="flex-start", 
            style={"marginTop": "5px", "width": "100%"}, 
            children=[
                dmc.Paper(
                    sidebar,
                ),
                dmc.Flex(
                    justify="center",  
                    align="flex-start",
                    style={"width": "100%"},  
                    children=[
                        tabs,
                    ],
                ),
            ],
        ),
    ],
)