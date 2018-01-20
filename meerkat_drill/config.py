import importlib.util
import os

SQS_ENDPOINT = 'http://tunnel:9324'
LOCAL = False

# Country config
config_directory = os.environ.get("COUNTRY_CONFIG_DIR",
                                  os.path.dirname(os.path.realpath(__file__)) + "/country_config/")
country_config_file = os.environ.get("COUNTRY_CONFIG", "demo_config.py")
country_queue_name = os.environ.get("COUNTRY_NAME", "demo").lower()
spec = importlib.util.spec_from_file_location(
    "country_config_module",
    config_directory + country_config_file
)
country_config_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(country_config_module)
country_config = country_config_module.country_config
