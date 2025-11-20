from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import yaml
import os
import sys
from pathlib import Path
from iwst.utils.logging import MongoFormatter, MongoHandler
from iwst.utils.login import User
import logging.config
logger = logging.getLogger()


@dataclass 
class DatabaseConfig:
    """Class to manage the database for storing data
    
    The only support DBMS is MongoDB.

    Args:
        host: host of the mongdb instance
        port: port of the mongodb instance
        name: name of the db
        timeout: time in MS before raising a timeout exception in connection

    """
    host: str
    port: int
    name: str
    timeout: int = 5000

    @classmethod
    def load(cls, data: Optional[Dict[str, Any]]):
        """Load database config from dict"""

        if data is None:
            logger.info('Database configuration not found.')
            return None
        
        host = data.get('host')
        if host is None:
            logger.error('Database host not found.')
            sys.exit(1)

        port = data.get('port')
        if port is None:
            logger.error('Database port not found.')
            sys.exit(1)

        name = data.get('name')
        if name is None:
            logger.error('Database name not found.')
            sys.exit(1)

        timeout = data.get('timeout')
        if timeout is None:
            logger.debug('Database timeout not found. Set default (5000ms).')

        return cls(
            host, 
            port, 
            name,
            timeout
        )


@dataclass
class Users:
    """Class to manage login user
    
    Args:
        users: list of User

    """
    users: List[User]

    @classmethod
    def load(cls, data: Optional[List[Dict[str, str]]]):
        """Load user data from dict"""
        if data is None:
            logger.debug('Login users not found.')
            return None
        else:
            users = [User.load(user) for user in data]
            return cls(users)
    
    def __iter__(self):
        for user in self.users:
            yield user

    def get_user(self, username: str) -> Optional[User]:
        return next((user for user in self.users if user.username == username), None)

    def is_admin(self, username: str) -> bool:
        """Whether the user is admin"""
        user = self.get_user(username)
        if user is None:
            logger.error(f'User {username} not found.')
            return False

        if user.role == 'admin':
            return True
        else:
            return False
    
    def get_accesstype(self, username: str) -> bool:
        """Get the access type of a user"""
        user = self.get_user(username)
        if user is None:
            logger.error(f'User {username} not found.')
            return False
        return user.access

@dataclass
class EmailSettings:
    """ """
    active: bool
    domain: str
    port: int
    user: str
    password: str
    from_address: str
    mailing_lists: List[str]
    subject: str

    @classmethod
    def load(cls, data: Optional[dict]):
        if data is None:
            logger.error("Email settings not found.") 
            sys.exit(1)
        
        active = data.get("active", False)
        domain = data.get("domain")
        port = data.get("port")
        user = data.get("user")
        password = data.get("password")
        from_address = data.get("from_address")
        mailing_lists = data.get("mailing_lists", []) 
        subject = data.get("subject", "Support Request")

        if not domain:
            logger.info('Domain not found.')
            return None

        if not port:
            logger.info('Port not found.')
            return None

        if not user:
            logger.info('User not found.')
            return None

        if not password:
            logger.info('Password not found.')
            return None

        if not from_address:
            logger.info('From address not found.')
            return None

        if not isinstance(mailing_lists, list):
            logger.info('Mailing lists must be a list.')
            return None
            
        return cls(
            active=active,
            domain=domain,
            port=port,
            user=user,
            password=password,
            from_address=from_address,
            mailing_lists=mailing_lists,
            subject=subject
        )

@dataclass
class Config:
    """Manage configuration file
    
    Args:
        database: settings of the database
        log: settings for logging

    """
    database: DatabaseConfig
    users: Users
    emailsettings: EmailSettings

    @classmethod
    def load(cls, argconfig: Optional[str] = None):
        """Load configuration from file
        
        Load configuration from file by checking input data.
        Set the basic configuration of the logger.
        Set environment variable for the dashboard.

        Args:
            argconfig: absolute path of the configuration file 

        """
        # check configuration file from path
        if argconfig is not None:
            if os.path.exists(argconfig):
                with open(argconfig, 'r') as fid:
                    config = yaml.full_load(fid)
            else:
                logger.debug(f'Configuration file {argconfig} does not exist.')
                config = None
        else:
            config = None
        
        # check configuration file from environment variables
        if config is None:
            envconfig = os.environ.get('IWST_CONFIG')
            if envconfig is not None:
                if os.path.exists(envconfig):
                    with open(envconfig, 'r') as fid:
                        config = yaml.full_load(fid)
                else:
                    logger.error("Config file from os environ not found.")
                    sys.exit(1)

        # check configuration file from .config folder
        if config is None:
            root = Path.home()
            filename = '.config/iwst/iwst.conf'
            homeconfig = os.path.join(root, filename)
            if os.path.exists(homeconfig):
                with open(homeconfig, 'r') as fid:
                    config = yaml.full_load(fid)
            else:
                logger.error(f'Default configuration file does not exist. ({homeconfig})')
                sys.exit(1)

        # load logging configuration
        loggingdata = config.get('logging')
        if loggingdata is not None:
            # add version
            loggingdata['version'] = 1
            
            # create log folder
            logfolder = os.path.dirname(loggingdata['handlers']['file']['filename'])
            os.makedirs(logfolder, exist_ok=True)

            # load logging config
            logging.config.dictConfig(loggingdata)
        
        # load database config
        dbconfig = DatabaseConfig.load(config.get('database'))
        
        # add logging to mongodb after parsing the database settings
        if loggingdata is not None:
            if loggingdata['db']:
                mongoformatter = MongoFormatter()
                mongohandler = MongoHandler(dbconfig.host, dbconfig.port, dbconfig.name)
                mongohandler.setFormatter(mongoformatter)
                mongohandler.setLevel(logging.INFO)
                logger.addHandler(mongohandler)

        # load users
        users = Users.load(config.get('users'))

        # load email settings
        emailsettings = EmailSettings.load(config.get('emailsettings'))

        # log end of parsing data
        logger.info('Configuration file loaded.')

        return cls(
            dbconfig,
            users,
            emailsettings
        )
