from dash import html, callback, Input, Output
from flask_login import current_user


placeholder = html.Div(
    id='user-permissions'
)

def register_callbacks(app):

    @app.callback(
        Output('user-permissions', 'children'),
        Input('user-permissions', 'id')    
    )
    def getpermissions(_):
        return current_user.access
    
    return app