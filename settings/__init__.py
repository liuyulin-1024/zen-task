import os
from dynaconf import Dynaconf

environ = os.getenv("environ", "local")
if environ == "local":
    config_filepath = os.path.join(os.path.dirname(__file__), "local.toml")
else:
    raise ValueError('Environment variable `environ` is not defined')


settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[config_filepath, ".secrets.toml"],
)
env = settings.app.env
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_DIR = "./logs"
