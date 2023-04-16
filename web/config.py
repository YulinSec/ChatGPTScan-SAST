from datetime import timedelta
from utils.config import Config

config = Config().config


class flask_config(object):
    DEBUG = config["web"]["DEBUG"]
    SECRET_KEY = config["web"]["SECRET_KEY"]
    PERMANENT_SESSION_LIFETIME = timedelta(days=config["web"]["PERMANENT_SESSION_LIFETIME"])

