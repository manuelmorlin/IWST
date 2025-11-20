from __future__ import annotations
from typing import Optional, Dict, Any, Union

import dash
from dash import dcc, html, callback, Input, Output, set_props
import flask
from flask import current_app
from flask_login import login_required, logout_user, login_user, LoginManager, current_user
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask_security.utils import verify_password, hash_password
from flask_bcrypt import Bcrypt

from pathlib import Path
import yaml
import secrets
import os
from datetime import datetime
import traceback
import logging
logger = logging.getLogger()

from iwst.utils.login import User, restrict_access
from iwst.routes.home.layout import layout as homelayout
from iwst.routes.homeevaluation.layout import layout as homelayout_trial

from iwst.routes.home.callbacks import register_callbacks as register_callbacks_home
from iwst.routes.homeevaluation.callbacks import register_callbacks as register_callbacks_homeevaluation


def create_app(config: Optional[Dict[str, Any]] = None) -> Union[flask.Flask, dash.Dash]:
    """Start a dash application. 
    
    It returns a Flask Server object to run production server (gunicorn for instance) and
    a Dash object to run the default(development) server from dash 

    Args:
        config: configuration settings be to attached to flask server

    Returns:
        Flask Server
        Dash app

    """
    pwamanifest = {
        'href': '/static/manifest.json',
        'rel': 'manifest',
    }

    serviceworker = '/static/js/service-worker.js'

    # start server
    server = flask.Flask(__name__)

    # attached configuration file to server
    server.config.update(
        IWST=config
    )
    
    # separate cookies path and name
    session_cookie_path = '/'
    server.config.update(
        SESSION_COOKIE_NAME = 'session_iwst',
        SESSION_COOKIE_PATH = session_cookie_path
    )

    # setup configurations
    server.config['SECRET_KEY'] = '^*@()Q%*(Y!)@!)^^^*#G(!@#'

    # password setup
    bcrypt = Bcrypt(server)

    login_manager = LoginManager()
    login_manager.login_view = "/login"
    login_manager.anonymous_user = User
    login_manager.init_app(server)

    # Create logout route
    @server.route("/logout")
    @login_required
    def logout():
        logger.info(f'User {current_user.username} logged out.')
        logout_user()
        return flask.redirect('/login')

    # Create a login route
    @server.route('/login', methods=['GET', 'POST'])
    def login():
        # load configuration file
        appconfig = current_app.config.get('IWST')
        
        # check browser type
        if flask.request.user_agent.browser == 'firefox':
            return flask.make_response(flask.render_template('notsupported.html'))

        if flask.request.method == 'GET':
            return flask.make_response(flask.render_template('login.html'))

        elif flask.request.method == 'POST':
            data = flask.request.form
            username = data.get('username')
            password = data.get('password')
            
            # find username
            user = next((user for user in appconfig.users if user.username == username), None)
            if user is None:
               return flask.make_response(flask.render_template('login.html'))

            # check password
            if bcrypt.check_password_hash(user.password, password):
                login_user(User(username))
                rep = flask.redirect('/full/home')
                rep.set_cookie(
                    'IWST - Isamgeo Wellbore Stability Tool', 
                    username,
                    path=session_cookie_path
                )
                logger.info(f'User {username} logged in.')
                return rep
            else:
                return flask.make_response(flask.render_template('login.html'))

    # to load current user
    @login_manager.user_loader
    def load_user(user_id):
        # check evaluation users first
        if user_id.startswith('evaluation'):
            return User(user_id, role='user', access='evaluation')

        # setup full users
        config = current_app.config.get('IWST')
        user = config.users.get_user(user_id)
        if user is not None:
            role = user.role
            access = user.access
        else:
            role = None
            access = None
        return User(user_id, role=role, access=access)

    # redirect home route to login
    @server.route("/")
    def start():
        return flask.redirect('/login')

    # setup global error handler
    errordialog = dcc.ConfirmDialog(
        id='global-error-dialog',
        message='Something went wrong. An email has already been sent to the support team. Sorry for the inconvenience.'
    )

    # create gloabl error handler for production
    def on_callback_error(err):
        set_props("global-error-dialog", {"displayed": True})
        logger.error(f'Error: {err}. Full traceback: {traceback.format_exc()}')

    # create full app
    app = dash.Dash(
        __name__,
        external_stylesheets=[pwamanifest],
        external_scripts=[serviceworker],
        server=server,
        update_title=None,
        suppress_callback_exceptions=True,
        url_base_pathname='/full/',
        prevent_initial_callbacks="initial_duplicate",
        on_error=on_callback_error
    )

    app.title = "IWST - Isamgeo Wellbore Stability Tool"

    # set up routing
    url = html.Div(
        children=[
            dcc.Location(id='url', refresh='callback-nav'),
            html.Div(
                children=[
                    errordialog,
                    html.Div(id='page-content')
                ]
            )
        ]
    )

    # start routing
    app.layout = url

    # register callbacks
    app = register_callbacks_home(app)

    # manage routes
    @callback(
        Output('page-content', 'children'),
        Input('url', 'pathname')
    )
    def display_page(pathname):
        if pathname == '/full/home':
            return homelayout
        else:
            return None

    # prevent views if not logged
    for view_name, view_method in app.server.view_functions.items():
        if view_name.startswith(app.config.url_base_pathname):
            app.server.view_functions[view_name] = login_required(view_method)

    # prevent views if restricted access
    for view_name, view_method in app.server.view_functions.items():
        if view_name.startswith(app.config.url_base_pathname):
            app.server.view_functions[view_name] = restrict_access(view_method, 'full')
        
    # Create a login route for evaluation (anonymous) user
    @server.route('/loginanonymous', methods=['POST'])
    def loginanonymous(): 
        # check browser type
        if flask.request.user_agent.browser == 'firefox':
            return flask.make_response(flask.render_template('notsupported.html'))

        addr = flask.request.remote_addr
        username = f'evaluation--{addr}--{datetime.today().isoformat()}'

        r = login_user(User(username))
        rep = flask.redirect('/evaluation/home')
        rep.set_cookie(
            'IWST - Isamgeo Wellbore Stability Tool - Evaluation', 
            username,
            path=session_cookie_path
        )
        logger.info(f'User {username} logged in for Evaluation version.')
        return rep

    # define evaluation app
    appevaluation = dash.Dash(
        __name__,
        external_stylesheets=[pwamanifest],
        external_scripts=[serviceworker],
        server=server,
        update_title=None,
        suppress_callback_exceptions=True,
        url_base_pathname='/evaluation/',
        prevent_initial_callbacks="initial_duplicate",
    )
    appevaluation.title = "IWST - Evaluation"

    # set main layout for the trial app
    appevaluation.layout = url

    # register callbacks
    appevaluation = register_callbacks_homeevaluation(appevaluation)

    # manage routes for the evaluation version
    @appevaluation.callback(
        Output('page-content', 'children'),
        Input('url', 'pathname')
    )
    def display_page(pathname):
        if pathname == '/evaluation/home':
            return homelayout_trial
        else:
            return None

    # prevent views if not logged
    for view_name, view_method in appevaluation.server.view_functions.items():
        if view_name.startswith(appevaluation.config.url_base_pathname):
            appevaluation.server.view_functions[view_name] = login_required(view_method)

    # prevent views if restricted access
    for view_name, view_method in appevaluation.server.view_functions.items():
        if view_name.startswith(appevaluation.config.url_base_pathname):
            appevaluation.server.view_functions[view_name] = restrict_access(view_method, 'evaluation')

    # redirect root route to main dash page route
    @server.route('/')
    def render_dashboard():
        return flask.redirect('/dashevaluation')

    # join apps
    server = DispatcherMiddleware(
        app=server, 
        mounts={
            '/dashfull': app.server,
            '/dashevaluation': appevaluation.server
        }
    )

    return server, app
    
