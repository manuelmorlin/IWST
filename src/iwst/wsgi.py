from iwst.app import create_app
from iwst.utils.config import Config


# load config file
config = Config.load()

# create server
server, _  = create_app(config)