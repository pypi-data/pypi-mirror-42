import os
import json


class LoggerConfig(object):
    def __init__(
        self,
        __dsn__=None,
        __app_name__="_DefaultName",
        __version__="0.0.0",
        logspath="/opt/skynet/RedditBots/logs/",
    ):

        configfilepath = os.path.join(os.path.dirname(__file__), "logging_config.json")
        with open(configfilepath, "rt") as f:
            self.config = json.load(f)

        # Replaces the filename with one specific to each bot
        try:
            self.config["handlers"]["rotateFileHandler"][
                "filename"
            ] = f"{logspath}_DefaultName_Logs.log".replace(
                "_DefaultName", __app_name__.replace(" ", "_")
            )
        except Exception:
            raise AttributeError("Unable to set normal logging configuration location")

        try:
            self.config["handlers"]["rotateFileHandler_debug"][
                "filename"
            ] = f"{logspath}_DefaultName_Logs_Debug.log".replace(
                "_DefaultName", __app_name__
            )
        except Exception:
            raise AttributeError("Unable to set debug logging configuration location")

        # Replace the Sentry DSN ID with the app specific one
        try:
            self.config["handlers"]["SentryHandler"]["dsn"] = __dsn__
        except Exception:
            raise AttributeError("Unable to set Sentry DSN info")

        # Set the App Version / Release Version
        self.config["handlers"]["SentryHandler"]["release"] = __version__

    def get_config(self):
        return self.config
