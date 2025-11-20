from dash import html, callback, Input, Output
from flask_login import current_user


placeholder = html.Div(
    id='evaluation',
)

def register_callbacks(app):
    
    @app.callback(
        Output('evaluation', 'children'),
        Input('evaluation', 'id')    
    )
    def getpermissions(_):
        return f"I am the evaluation version, user connected as {current_user.username}"

    return app