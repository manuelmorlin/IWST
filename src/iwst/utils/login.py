from dataclasses import dataclass
import sys
import functools
from flask_login import current_user
from flask import current_app
import logging
logger = logging.getLogger()


def restrict_access(func, accesstype: str):
    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.access != accesstype:
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view

@dataclass
class User:
    """Class to manage user info"""
    username: str = None
    password: str = None
    role: str = 'user'
    access: str = 'trial'

    @classmethod
    def load(cls, data: dict[str, str]):
        """Load class from dict"""
        username = data.get('username')
        if username is None:
            logger.error('Username for login not found.')
            sys.exit(1)

        password = data.get('password')
        if password is None:
            logger.error('Password for login not found.')
            sys.exit(1)
        
        role = data.get('role')
        if role is None:
            logger.debug(f"Role for user {username} not found. Set 'user'")
            role = 'user'

        if role not in ['admin', 'user']:
            logger.error("Passed wrong role for user {username}. Available choices: 'user', 'admin'")
            sys.exit(1)
        
        access = data.get('access')
        if access is None:
            logger.debug(f"Access type for user {username} not found. Set 'trial'")
            access = 'evaluation'

        if access not in ['evaluation', 'full']:
            logger.error(f"Passed wrong access type for user {username}. Available choices: 'evaluation', 'full'")
            sys.exit(1)

        return cls(username, password, role, access)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_credential(self):
        return self.username, self.password

    def get_id(self):
        return self.username

    def get_collection_name(self):
        username_part = current_user.username.split("@")[0]
        collection_name = username_part.replace(".", "_") 
        return collection_name