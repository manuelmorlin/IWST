import dash_mantine_components as dmc
import dash
import uuid
import pymongo
import smtplib

from dash import dcc, html, Output, State, Input, no_update, ctx, ALL
from dash.exceptions import PreventUpdate
from email.utils import formatdate
from pymongo import MongoClient
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from iwst import __version__
from flask import current_app
from flask_login import current_user
from iwst.utils.config import Config
from iwst.routes.home.utils.utils import send_email
from datetime import datetime


toolbar = dmc.Flex(
    align="center",
    justify="space-between",  
    style={
        "backgroundColor": "#f8f9fa",
        "borderBottom": "1px solid #e9ecef",
        "height": "20px",  
    },
    children=[
        dmc.Flex(
            gap=0,  
            align="center",  
            children=[
                dmc.Menu(
                    [
                        dmc.MenuTarget(
                            dmc.Button(
                                "File",
                                variant="subtle",
                                style={"padding": "0 2px", "height": "100%", "marginLeft": "5px"},
                            )
                        ),
                        dmc.MenuDropdown(
                            [
                                dmc.MenuItem("Create Project", id="create-project", styles={"item": {"padding": "5px 4px", "height": "100%"}}),  
                                dmc.MenuItem("Save Project", id="save-project", styles={"item": {"padding": "5px 4px", "height": "100%"}}, disabled=True),
                                dmc.MenuItem("Load Project", id="load-project", styles={"item": {"padding": "5px 4px", "height": "100%"}}),
                                dmc.Menu( 
                                    [
                                        dmc.MenuTarget(
                                            dmc.MenuItem("Recent Projects", id="recent-project")
                                        ),
                                        dmc.MenuDropdown(
                                            id="recent-projects-dropdown",
                                            children=[]
                                        ),
                                    ],
                                    position="right-start",  
                                    offset=0,  
                                    transitionProps={"transition": "pop-top-left", "duration": 150},
                                    styles={
                                        "item": {
                                            "padding": "5px 4px",  
                                            "height": "100%",    
                                        }
                                    },
                                ),
                                dmc.MenuItem("Delete Project", id="drop-project", styles={"item": {"padding": "5px 4px", "height": "100%"}}),
                                dmc.MenuItem(
                                    dmc.Anchor(
                                        children="Logout", 
                                        href="/logout", 
                                        underline='never', 
                                        refresh=True
                                    )
                                )
                            ]
                        ),
                    ],
                    position="bottom-start",  
                    offset=0,  
                    transitionProps={"transition": "pop-top-left", "duration": 150},
                    shadow="md",
                    styles={
                        "item": {
                            "padding": "5px 4px",  
                            "height": "100%",    
                        }
                    },
                    keepMounted=True
                ),
                dmc.Menu(
                    [
                        dmc.MenuTarget(
                            dmc.Button(
                                "Help",
                                variant="subtle",
                                style={"padding": "0 2px", "height": "100%"},
                            )
                        ),
                        dmc.MenuDropdown(
                            [
                                dmc.MenuItem("Contact Support", id="contact-support"),
                            ]
                        ),
                    ],
                    position="bottom-start",
                    offset=0,
                    transitionProps={"transition": "pop-top-left", "duration": 150},
                    shadow="md",
                    styles={
                        "item": {
                            "padding": "5px 4px",  
                            "height": "100%",   
                        }
                    },
                    keepMounted=True
                ),
                dmc.Menu(
                    [
                        dmc.MenuTarget(
                            dmc.Button(
                                "About us",
                                variant="subtle",
                                style={"padding": "0 2px", "height": "100%"},
                            )
                        ),
                        dmc.MenuDropdown(
                            [
                                dmc.MenuItem(f"Version {__version__}", id="version"),
                                dmc.MenuItem(
                                    dmc.Anchor(
                                        children="www.isamgeo.com", 
                                        href="https://www.isamgeo.com/", 
                                        target="_blank",  
                                        underline="never",
                                    ),
                                    id="website-link",
                                ),
                                dmc.MenuItem("Written By", id="written-by"),
                            ]
                        ),
                    ],
                    position="bottom-start",
                    offset=0,
                    transitionProps={"transition": "pop-top-left", "duration": 150},
                    shadow="md",
                    styles={
                        "item": {
                            "padding": "5px 4px",  
                            "height": "100%",    
                        }
                    },
                    keepMounted=True
                ),
            ], 
        ),
        dmc.Text("IWST- Unsaved*", id="project-title", size="sm"),

        html.Div(style={"width": "100px"}),

        dmc.Modal(
            id="create-project-modal",
            title="Create Project",
            centered=True,
            size="lg",
            children=[
                dmc.Stack([
                    dmc.TextInput(
                        label="Project Name",
                        id="project-name-input",
                        error="",  
                    ),
                    dmc.Textarea(label="Project Description", id="project-description-input", autosize=True, minRows=2),
                    dmc.Button("Confirm", id="confirm-create-project", fullWidth=True, mt=10),
                ])
            ],
        ),
        dmc.Modal(
            id="overwrite-project-modal",
            title="Project Already Exists",
            centered=True,
            size="md",
            children=[
                dmc.Text("A project with this name already exists. Do you want to overwrite it?"),
                dmc.Group(
                    [
                        dmc.Button("Yes", id="confirm-overwrite-project", variant="filled", color="green"),
                        dmc.Button("No", id="cancel-overwrite-project", variant="outline", color="red"),
                    ],
                    justify="right",
                    mt="md",
                ),
            ],
        ),
        dmc.Modal(
            id="load-project-modal",
            title="Load Project",
            centered=True,
            size="lg",
            children=[
                dmc.Stack([
                    dmc.Text("Select a project to import:"),
                    dmc.Select(
                        id="project-list-select",
                        data=[],
                        searchable=True,
                        placeholder="Choose a project",
                    ),
                    dmc.Text(id="project-description-display", c="dimmed"),
                    dmc.Group(
                        [
                            dmc.Button("Load", id="confirm-load-project", variant="filled", color="green"),
                            dmc.Button("Cancel", id="cancel-load-project", variant="outline", color="red"),
                        ],
                        justify="right",
                        mt="md",
                    ),
                ]),
            ],
        ),
        dmc.Modal(
            id="drop-project-modal",
            title="Delete Project",
            centered=True,
            size="lg",
            children=[
                dmc.Stack([
                    dmc.Text("Select a project to delete:"),
                    dmc.Select(
                        id="project-delete-list-select",
                        data=[],  
                        searchable=True,
                        placeholder="Choose a project",
                    ),
                    dmc.Group(
                        [
                            dmc.Button("Delete", id="confirm-drop-project", variant="filled", color="red"),
                            dmc.Button("Cancel", id="cancel-drop-project", variant="outline", color="gray"),
                        ],
                        justify="right",
                        mt="md",
                    ),
                ])
            ],
        ),
        dmc.Modal(
            id="confirm-delete-project-modal",
            title="Confirm Deletion",
            centered=True,
            size="md",
            children=[
                dmc.Text("Are you sure you want to delete the selected project?", mb=20),
                dmc.Group(
                    [
                        dmc.Button("Delete", id="confirm-delete-project", variant="filled", color="red"),
                        dmc.Button("Cancel", id="cancel-delete-project", variant="outline", color="gray"),
                    ],
                    justify="right",
                ),
            ],
            opened=False,
        ),
        dmc.Modal(
            id="written-by-modal",
            title="Written by",
            children=[
                dmc.Text("Isamgeo Italia S.r.l. 2025", style={"text-align": "center"}),
            ],
            opened=False,  
            centered=True,
            size="md",
        ),
        dmc.Modal(
            id="contact-support-modal",
            title="Contact Support",
            centered=True,
            size="lg",
            children=[
                dmc.Stack([
                    dmc.TextInput(
                        label="Your Email",
                        id="support-email-input",
                        placeholder="Enter your email address:",
                        required=True,
                    ),
                    dmc.TextInput(
                        label="Subject",
                        id="support-subject-input",
                        placeholder="Enter the subject of your message:",
                        required=True,
                    ),
                    dmc.Textarea(
                        label="Message",
                        id="support-message-input",
                        placeholder="Describe your issue or request:",
                        minRows=5,
                        required=True,
                    ),
                    dmc.Group(
                        [
                            dmc.Button("Send", id="send-support-message", variant="filled", color="green"),
                            dmc.Button("Cancel", id="cancel-support-message", variant="outline", color="red"),
                        ],
                        justify="right",
                        mt="md",
                    ),
                ]),
            ],
            opened=False,  
        ),
    ],
)

def register_callbacks(app):
    @app.callback(
        Output("project-title", "children", allow_duplicate=True),
        Output("create-project-modal", "opened"),
        Output("overwrite-project-modal", "opened"),  
        Output("project-data", "data", allow_duplicate=True),
        Output("project-name-input", "error"),
        Input("create-project", "n_clicks"),
        Input("confirm-create-project", "n_clicks"),
        Input("confirm-overwrite-project", "n_clicks"),  
        Input("cancel-overwrite-project", "n_clicks"),  
        Input("save-project", "n_clicks"), 
        State("project-name-input", "value"),
        State("project-description-input", "value"),
        State("project-data", "data"),
        State("max-principal-stress-input", "value"),
        State("intermediate-principal-stress-input", "value"),
        State("min-principal-stress-input", "value"),
        State("pore-pressure-input", "value"),
        State("mud-pressure-input", "value"),
        State("poisson-ratio-input", "value"),
        State("azimuth-input", "value"),
        State("inclination-angle-input", "value"),
        State("friction-coefficient-input", "value"),
        State("alpha-angle-input", "value"),
        State("beta-angle-input", "value"),
        State("gamma-angle-input", "value"),
        State("tensile-strength-input", "value"),
        prevent_initial_call=True,
    )
    def handle_project_actions(
        create_clicks, 
        confirm_clicks, 
        confirm_overwrite, 
        cancel_overwrite, 
        save_clicks,
        name, 
        description, 
        current_data, 
        max_principal_stress, 
        intermediate_principal_stress,
        min_principal_stress, 
        pore_pressure, 
        mud_pressure, 
        poisson_ratio, 
        azimuth,
        inclination_angle, 
        friction_coefficient, 
        alpha_angle, 
        beta_angle, 
        gamma_angle, 
        tensile_strength
    ):
        triggered_id = ctx.triggered_id

        if triggered_id == "create-project":
            return no_update, True, False, no_update, ""  

        elif triggered_id == "confirm-create-project":
            if not name:
                return no_update, no_update, no_update, no_update, "Project name is required." 

            config = current_app.config.get("IWST")
            db_config = config.database
            client = MongoClient(
                host=db_config.host,
                port=db_config.port,
            )
            db = client[db_config.name]
            collection_name = current_user.username 
            collection = config.users.get_user(collection_name).get_collection_name()
            projects_collection = db[collection]["projects"]

            existing_project = projects_collection.find_one({"project_name": name})
            if existing_project:
                return no_update, False, True, no_update, ""  

            if current_data is None:
                current_data = {}  

            current_data["project_name"] = name
            current_data["project_description"] = description
            return f"IWST- {name}*", False, False, current_data, ""  

        elif triggered_id == "confirm-overwrite-project":
            if current_data is None:
                current_data = {}
            current_data["project_name"] = name
            current_data["project_description"] = description

            config = current_app.config.get("IWST")
            db_config = config.database
            client = MongoClient(
                host=db_config.host,
                port=db_config.port,
            )
            db = client[db_config.name]
            collection_name = current_user.username 
            collection = config.users.get_user(collection_name).get_collection_name()
            projects_collection = db[collection]["projects"]

            creating_time = datetime.utcnow()
            inputs = {
                "max_principal_stress": max_principal_stress,
                "intermediate_principal_stress": intermediate_principal_stress,
                "min_principal_stress": min_principal_stress,
                "pore_pressure": pore_pressure,
                "mud_pressure": mud_pressure,
                "poisson_ratio": poisson_ratio,
                "azimuth": azimuth,
                "inclination_angle": inclination_angle,
                "friction_coefficient": friction_coefficient,
                "alpha_angle": alpha_angle,
                "beta_angle": beta_angle,
                "gamma_angle": gamma_angle,
                "tensile_strength": tensile_strength,
            }

            projects_collection.update_one(
                {"project_name": name},
                {
                    "$set": {
                        "project_description": description,
                        "last_updated": creating_time,
                        "inputs": inputs,
                    }
                },
                upsert=True,
            )

            current_data["last_updated"] = creating_time
            current_data["inputs"] = inputs

            return f"IWST- {name}", False, False, current_data, ""  

        elif triggered_id == "cancel-overwrite-project":
            return no_update, False, False, no_update, ""

        elif triggered_id == "save-project":
            if current_data is None or "project_name" not in current_data:
                raise PreventUpdate 

            project_name = current_data["project_name"]
            project_description = current_data.get("project_description", "")
            creating_time = datetime.utcnow()

            inputs = {
                "max_principal_stress": max_principal_stress,
                "intermediate_principal_stress": intermediate_principal_stress,
                "min_principal_stress": min_principal_stress,
                "pore_pressure": pore_pressure,
                "mud_pressure": mud_pressure,
                "poisson_ratio": poisson_ratio,
                "azimuth": azimuth,
                "inclination_angle": inclination_angle,
                "friction_coefficient": friction_coefficient,
                "alpha_angle": alpha_angle,
                "beta_angle": beta_angle,
                "gamma_angle": gamma_angle,
                "tensile_strength": tensile_strength,
            }

            config = current_app.config.get("IWST")
            db_config = config.database
            client = MongoClient(
                host=db_config.host,
                port=db_config.port,
            )
            db = client[db_config.name]
            collection_name = current_user.username 
            collection = config.users.get_user(collection_name).get_collection_name()
            projects_collection = db[collection]["projects"]

            projects_collection.update_one(
                {"project_name": project_name},
                {
                    "$set": {
                        "project_description": project_description,
                        "last_updated": creating_time,
                        "inputs": inputs,
                    }
                },
                upsert=True,  
            )

            current_data["last_updated"] = creating_time
            current_data["inputs"] = inputs

            return f"IWST- {project_name}", False, False, no_update, ""

        return no_update, no_update, no_update, no_update, ""

    @app.callback(
        Output("save-project", "disabled"),  
        Input("project-data", "data"),  
        prevent_initial_call=True,
    )
    def save_project(current_data):
        if current_data is None or "project_name" not in current_data:
            return True 
        return False 

    @app.callback(
        Output("load-project-modal", "opened"),  
        Output("project-list-select", "data"),  
        Input("load-project", "n_clicks"),
        prevent_initial_call=True,
    )
    def load_project(load_clicks):
        if not load_clicks:
            raise PreventUpdate
        config = current_app.config.get("IWST")
        db_config = config.database
        client = MongoClient(
            host=db_config.host,
            port=db_config.port,
        )
        db = client[db_config.name]
        collection_name = current_user.username 
        collection = config.users.get_user(collection_name).get_collection_name()
        projects_collection = db[collection]["projects"]
        projects = list(projects_collection.find({}, {"_id": 0, "project_name": 1, "project_description": 1}).sort("last_updated", pymongo.DESCENDING))
        
        project_list = [{"value": p["project_name"], "label": p["project_name"]} for p in projects]

        return True, project_list

    @app.callback(
        Output("project-description-display", "children"),
        Input("project-list-select", "value"),
        prevent_initial_call=True,
    )
    def save_project_description(project_name):
        if not project_name:
            raise PreventUpdate
        
        config = current_app.config.get("IWST")
        db_config = config.database
        client = MongoClient(
            host=db_config.host,
            port=db_config.port,
        )
        db = client[db_config.name]
        collection_name = current_user.username 
        collection = config.users.get_user(collection_name).get_collection_name()
        projects_collection = db[collection]["projects"]
        
        project = projects_collection.find_one({"project_name": project_name}, {"_id": 0, "project_description": 1})
        
        description = project.get("project_description", "No description available")
        
        return description or "No description available" 

    @app.callback(
        Output("recent-projects-dropdown", "children"),  
        Input("recent-project", "n_clicks"), 
        prevent_initial_call=True,
    )
    def recent_projects(n_clicks):
        if not n_clicks:
            raise PreventUpdate

        config = current_app.config.get("IWST")
        db_config = config.database
        client = MongoClient(
            host=db_config.host,
            port=db_config.port,
        )
        db = client[db_config.name]
        collection_name = current_user.username 
        collection = config.users.get_user(collection_name).get_collection_name()
        projects_collection = db[collection]["projects"]

        recent_projects = list(
            projects_collection.find({}, {"_id": 0, "project_name": 1}).sort("last_updated", pymongo.DESCENDING).limit(5)
        )

        if not recent_projects:
            return [dmc.MenuItem("No recent projects", disabled=True)]

        project_items = [
            dmc.MenuItem(
                project["project_name"],
                id={"type": "recent-project-item", "index": idx}, 
            )
            for idx, project in enumerate(recent_projects)
        ]

        return project_items

    @app.callback(
        Output("project-title", "children"),
        Output("project-data", "data"),
        Output("max-principal-stress-input", "value", allow_duplicate=True),
        Output("intermediate-principal-stress-input", "value", allow_duplicate=True),
        Output("min-principal-stress-input", "value", allow_duplicate=True),
        Output("pore-pressure-input", "value", allow_duplicate=True),
        Output("mud-pressure-input", "value", allow_duplicate=True),
        Output("poisson-ratio-input", "value", allow_duplicate=True),
        Output("azimuth-input", "value", allow_duplicate=True),
        Output("inclination-angle-input", "value", allow_duplicate=True),
        Output("friction-coefficient-input", "value", allow_duplicate=True),
        Output("alpha-angle-input", "value", allow_duplicate=True),
        Output("beta-angle-input", "value", allow_duplicate=True),
        Output("gamma-angle-input", "value", allow_duplicate=True),
        Output("tensile-strength-input", "value", allow_duplicate=True),
        Input({"type": "recent-project-item", "index": ALL}, "n_clicks"),
        State({"type": "recent-project-item", "index": ALL}, "children"),
        State("project-data", "data"),
        prevent_initial_call=True,
    )
    def load_recent_project(clicked_buttons, project_names, current_data):
        ctx = dash.callback_context
        if not ctx.triggered:
            raise PreventUpdate

        triggered_index = None
        for i, n_clicks in enumerate(clicked_buttons):
            if n_clicks and n_clicks > 0:
                triggered_index = i
                break

        if triggered_index is None:
            raise PreventUpdate

        project_name = project_names[triggered_index]

        config = current_app.config.get("IWST")
        db_config = config.database
        client = MongoClient(
            host=db_config.host,
            port=db_config.port,
        )
        db = client[db_config.name]
        collection_name = current_user.username 
        collection = config.users.get_user(collection_name).get_collection_name()
        projects_collection = db[collection]["projects"]

        project = projects_collection.find_one({"project_name": project_name}, {"_id": 0, "inputs": 1})

        if not project:
            raise PreventUpdate

        inputs = project.get("inputs", {})

        if current_data is None:
            current_data = {}

        current_data["project_name"] = project_name
        current_data["inputs"] = inputs

        return (
            f"IWST- {project_name}",
            current_data,
            inputs.get("max_principal_stress"),
            inputs.get("intermediate_principal_stress"),
            inputs.get("min_principal_stress"),
            inputs.get("pore_pressure"),
            inputs.get("mud_pressure"),
            inputs.get("poisson_ratio"),
            inputs.get("azimuth"),
            inputs.get("inclination_angle"),
            inputs.get("friction_coefficient"),
            inputs.get("alpha_angle"),
            inputs.get("beta_angle"),
            inputs.get("gamma_angle"),
            inputs.get("tensile_strength"),
        )

    @app.callback(
        Output("load-project-modal", "opened", allow_duplicate=True),  
        Input("cancel-load-project", "n_clicks"),  
        prevent_initial_call=True,  
    )
    def close_load_project_modal(cancel_clicks):
        if cancel_clicks is None:
            raise PreventUpdate  
        return False  

    @app.callback(
        Output("project-title", "children", allow_duplicate=True),
        Output("project-data", "data", allow_duplicate=True),
        Output("load-project-modal", "opened", allow_duplicate=True),
        Input("confirm-load-project", "n_clicks"),
        State("project-list-select", "value"),
        State("project-data", "data"),
        prevent_initial_call=True,
    )
    def confirm_load_project(n_clicks, selected_project_name, current_data):
        if not n_clicks or not selected_project_name:
            raise PreventUpdate

        config = current_app.config.get("IWST")
        db_config = config.database
        client = MongoClient(
            host=db_config.host,
            port=db_config.port,
        )
        db = client[db_config.name]
        collection_name = current_user.username 
        collection = config.users.get_user(collection_name).get_collection_name()
        projects_collection = db[collection]["projects"]

        project = projects_collection.find_one({"project_name": selected_project_name}, {"_id": 0})

        if not project:
            raise PreventUpdate

        if current_data is None:
            current_data = {}

        current_data["project_name"] = project.get("project_name", "")
        current_data["project_description"] = project.get("project_description", "")
        current_data["inputs"] = project.get("inputs", {})

        return f"IWST- {selected_project_name}", current_data, False

    @app.callback(
        Output("max-principal-stress-input", "value", allow_duplicate=True),
        Output("intermediate-principal-stress-input", "value", allow_duplicate=True),
        Output("min-principal-stress-input", "value", allow_duplicate=True),
        Output("pore-pressure-input", "value", allow_duplicate=True),
        Output("mud-pressure-input", "value", allow_duplicate=True),
        Output("poisson-ratio-input", "value", allow_duplicate=True),
        Output("azimuth-input", "value", allow_duplicate=True),
        Output("inclination-angle-input", "value", allow_duplicate=True),
        Output("friction-coefficient-input", "value", allow_duplicate=True),
        Output("alpha-angle-input", "value", allow_duplicate=True),
        Output("beta-angle-input", "value", allow_duplicate=True),
        Output("gamma-angle-input", "value", allow_duplicate=True),
        Output("tensile-strength-input", "value", allow_duplicate=True),
        Input("project-data", "data"),
        prevent_initial_call=True,
    )
    def update_inputs_for_loading(data):
        if not data or "inputs" not in data:
            raise PreventUpdate
        inputs = data["inputs"]

        return (
            inputs.get("max_principal_stress"),
            inputs.get("intermediate_principal_stress"),
            inputs.get("min_principal_stress"),
            inputs.get("pore_pressure"),
            inputs.get("mud_pressure"),
            inputs.get("poisson_ratio"),
            inputs.get("azimuth"),
            inputs.get("inclination_angle"),
            inputs.get("friction_coefficient"),
            inputs.get("alpha_angle"),
            inputs.get("beta_angle"),
            inputs.get("gamma_angle"),
            inputs.get("tensile_strength"),
        )

    @app.callback(
        Output("written-by-modal", "opened"),  
        Input("written-by", "n_clicks"),      
        State("written-by-modal", "opened"),  
        prevent_initial_call=True,
    )
    def written_by_modal(n_clicks, is_open):
        if n_clicks:
            return not is_open  
        return is_open

    @app.callback(
        Output("contact-support-modal", "opened"),  
        Input("contact-support", "n_clicks"),      
        Input("send-support-message", "n_clicks"),  
        Input("cancel-support-message", "n_clicks"),  
        State("contact-support-modal", "opened"),  
        prevent_initial_call=True,
    )
    def contact_support_modal(contact_clicks, send_clicks, cancel_clicks, is_open):
        triggered_id = ctx.triggered_id
        if triggered_id == "contact-support":
            return True  
        elif triggered_id == "send-support-message" or triggered_id == "cancel-support-message":
            return False  
        return is_open

    @app.callback(
        Output("contact-support-modal", "opened", allow_duplicate=True),  
        Output("support-email-input", "value", allow_duplicate=True),     
        Output("support-subject-input", "value", allow_duplicate=True),
        Output("support-message-input", "value", allow_duplicate=True),
        Output("notifications-container", "children", allow_duplicate=True),
        Input("send-support-message", "n_clicks"),  
        State("support-email-input", "value"),   
        State("support-subject-input", "value"),   
        State("support-message-input", "value"),   
        prevent_initial_call=True,
    )
    def send_support_message(send_clicks, email, subject, message):
        if not send_clicks or not email or not subject or not message:
            raise PreventUpdate

        config = current_app.config.get("IWST")
        email_config = config.emailsettings
        recipient_emails = email_config.mailing_lists if email_config else []
        email_body = f"From: {email}\n{message}"
        success = send_email(recipient_emails, subject, email_body)

        if success:
            notification = dmc.Notification(
                title="Success",
                message="Your message has been successfully sent to support.",
                color="green",
                autoClose=3000,
                action="show"
            )
            return False, "", "", "", notification
        else:
            notification = dmc.Notification(
                title="Error",
                message="Failed to send email. Please try again later.",
                color="red",
                autoClose=4000,
                action="show"
            )
            return True, email, subject, message, notification

    @app.callback(
        Output("drop-project-modal", "opened"),
        Output("project-delete-list-select", "data"),
        Input("drop-project", "n_clicks"),
        prevent_initial_call=True,
    )
    def delete_project_modal(n_clicks):
        if not n_clicks:
            raise PreventUpdate
        
        config = current_app.config.get("IWST")
        db_config = config.database
        client = MongoClient(
            host=db_config.host,
            port=db_config.port,
        )
        db = client[db_config.name]
        collection_name = current_user.username 
        collection = config.users.get_user(collection_name).get_collection_name()
        projects_collection = db[collection]["projects"]

        projects = list(projects_collection.find({}, {"_id": 0, "project_name": 1}).sort("last_updated", pymongo.DESCENDING))
        project_list = [{"value": p["project_name"], "label": p["project_name"]} for p in projects]

        return True, project_list

    @app.callback(
        Output("confirm-delete-project-modal", "opened"),
        Input("confirm-drop-project", "n_clicks"),
        State("project-delete-list-select", "value"),
        prevent_initial_call=True,
    )
    def confirm_delete_project(n_clicks, project_name):
        if not n_clicks or not project_name:
            raise PreventUpdate
        return True  

    @app.callback(
        Output("confirm-delete-project-modal", "opened", allow_duplicate=True),
        Output("drop-project-modal", "opened", allow_duplicate=True),
        Output("project-delete-list-select", "data", allow_duplicate=True),
        Output("project-title", "children", allow_duplicate=True),
        Output("project-data", "data", allow_duplicate=True),
        Output("max-principal-stress-input", "value", allow_duplicate=True),
        Output("intermediate-principal-stress-input", "value", allow_duplicate=True),
        Output("min-principal-stress-input", "value", allow_duplicate=True),
        Output("pore-pressure-input", "value", allow_duplicate=True),
        Output("mud-pressure-input", "value", allow_duplicate=True),
        Output("poisson-ratio-input", "value", allow_duplicate=True),
        Output("azimuth-input", "value", allow_duplicate=True),
        Output("inclination-angle-input", "value", allow_duplicate=True),
        Output("friction-coefficient-input", "value", allow_duplicate=True),
        Output("alpha-angle-input", "value", allow_duplicate=True),
        Output("beta-angle-input", "value", allow_duplicate=True),
        Output("gamma-angle-input", "value", allow_duplicate=True),
        Output("tensile-strength-input", "value", allow_duplicate=True),
        Output("notifications-container", "children", allow_duplicate=True),  
        Input("confirm-delete-project", "n_clicks"),
        State("project-delete-list-select", "value"),
        State("project-data", "data"),
        prevent_initial_call=True,
    )
    def execute_delete_project(n_clicks, project_name, current_data):
        if not n_clicks or not project_name:
            raise PreventUpdate

        config = current_app.config.get("IWST")
        db_config = config.database
        client = MongoClient(
            host=db_config.host,
            port=db_config.port,
        )
        db = client[db_config.name]
        collection_name = current_user.username 
        collection = config.users.get_user(collection_name).get_collection_name()
        projects_collection = db[collection]["projects"]

        projects_collection.delete_one({"project_name": project_name})

        updated_projects = list(projects_collection.find({}, {"_id": 0, "project_name": 1})
                                .sort("last_updated", pymongo.DESCENDING))
        updated_list = [{"value": p["project_name"], "label": p["project_name"]} for p in updated_projects]

        reset_project = current_data and current_data.get("project_name") == project_name
        if reset_project:
            return (
                False, False, updated_list,
                "IWST - Unsaved", {}, 70.0, 67.0, 45.0, 32.0, 32.0, 0.15, 90.0, 85.0, 1.0, 0.0, 90.0, 0.0, 0.0,
                dmc.Notification(
                    title="Success",
                    message=f"'{project_name}' deleted successfully.",
                    color="green",
                    autoClose=3000,
                    action="show"
                )
            )

        return (
            False, False, updated_list,
            no_update, no_update,
            no_update, no_update, no_update, no_update, no_update,
            no_update, no_update, no_update, no_update, no_update,
            no_update, no_update, no_update,
            dmc.Notification(
                title="Success",
                message=f"Project '{project_name}' deleted successfully.",
                color="green",
                autoClose=3000,
                action="show"
            )
        )

    @app.callback(
        Output("confirm-delete-project-modal", "opened", allow_duplicate=True),
        Input("cancel-delete-project", "n_clicks"),
        prevent_initial_call=True,
    )
    def close_delete_modal(n_clicks):
        if n_clicks is None:
            raise PreventUpdate
        return False

    @app.callback(
        Output("drop-project-modal", "opened", allow_duplicate=True),
        Input("cancel-drop-project", "n_clicks"),
        prevent_initial_call=True,
    )
    def close_drop_project_modal(n_clicks):
        if n_clicks is None:
            raise PreventUpdate
        return False

    @app.callback(
        Output("project-title", "children", allow_duplicate=True),
        Input("save-project", "n_clicks"),
        Input("max-principal-stress-input", "value"),
        Input("intermediate-principal-stress-input", "value"),
        Input("min-principal-stress-input", "value"),
        Input("pore-pressure-input", "value"),
        Input("mud-pressure-input", "value"),
        Input("poisson-ratio-input", "value"),
        Input("azimuth-input", "value"),
        Input("inclination-angle-input", "value"),
        Input("friction-coefficient-input", "value"),
        Input("alpha-angle-input", "value"),
        Input("beta-angle-input", "value"),
        Input("gamma-angle-input", "value"),
        Input("tensile-strength-input", "value"),
        State("project-title", "children"),
        prevent_initial_call=True,
    )
    def update_project_title_on_change(
        save_clicks,
        max_principal_stress,
        intermediate_principal_stress,
        min_principal_stress,
        pore_pressure,
        mud_pressure,
        poisson_ratio,
        azimuth,
        inclination_angle,
        friction_coefficient,
        alpha_angle,
        beta_angle,
        gamma_angle,
        tensile_strength,
        current_title,
    ):
        ctx = dash.callback_context
        triggered_id = ctx.triggered_id

        # Remove asterisk if "Save Project" is clicked
        if triggered_id == "save-project":
            return current_title.replace("*", "")

        # Add asterisk if any input changes
        if "*" not in current_title:
            return f"{current_title}*"

        return current_title

    return app