import sys
import inspect
import argparse

import subprocess
import os
import json

from iwst.app import create_app
from iwst.utils.config import Config
import iwst as iwst_app

import logging
logger = logging.getLogger()


def iwst():
    """Command to start IWST - Isamgeo Wellbore stability Tool"""
    parser = argparse.ArgumentParser(description='Command to start IWST - Isamgeo Wellbore stability Tool')
    parser.add_argument('-dev', dest='dev', action='store_true', help='Use the server integrated in dash (for debugging)')
    parser.add_argument('-config', dest='config', help='IWST config file (default: /home/$USER/.config/iswt/iwst.conf)')
    parser.add_argument('-j', action='version')

    parser.version = iwst_app.__version__
    args = parser.parse_args()
    
    # read config file
    config = Config.load(args.config)
    
    # start server
    if args.dev:
        _, app = create_app(config)

        # reset on error handler to default
        app._on_error = None

        # run dev server
        app.run(
            debug=True, 
            host='0.0.0.0', 
            port=8050, 
            dev_tools_silence_routes_logging=False
        )
    else:
        subprocess.call(
            [
                "gunicorn", 
                "iwst.wsgi:server", 
                "-w", 
                "4", 
                "-b", 
                ":8051", 
                "--timeout", 
                "5000"
            ]
        )

