from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from iwst.routes.home.components.placeholder import register_callbacks as register_callbacks_placeholder
from iwst.routes.home.components.toolbar import register_callbacks as register_callbacks_toolbar
from iwst.routes.home.components.sidebar import register_callbacks as register_callbacks_sidebar
from iwst.routes.home.components.tabs import register_callbacks as register_callbacks_tabs
from iwst.routes.home.utils.defaults import DEFAULT_VALUES


import dash
import logging
logger = logging.getLogger()

def register_callbacks(app):
    register_callbacks_placeholder(app)
    register_callbacks_toolbar(app)
    register_callbacks_sidebar(app)
    register_callbacks_tabs(app)
    
    return app