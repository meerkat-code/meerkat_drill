import importlib.util
import os

SQS_ENDPOINT = 'http://tunnel:9324'
LOCAL = bool(os.environ.get("LOCAL", False))

rabbit_url = os.environ.get("RABBIT_URL", "amqp://guest:guest@rabbit:5672/%2F")
external_message_queue = os.environ.get("EXTERNAL_MESSAGE_QUEUE", "sqs")
# Country config
config_directory = os.environ.get("COUNTRY_CONFIG_DIR",
                                  os.path.dirname(os.path.realpath(__file__)) + "/country_config/")
country_config_file = os.environ.get("COUNTRY_CONFIG", "demo_config.py")
country_queue_name = os.environ.get("COUNTRY_NAME", "demo").lower()

sqs_queue_url = os.environ.get("SQS_QUEUE_URL", None)
sns_topic_arn = os.environ.get("SNS_TOPIC_ARN", None)

spec = importlib.util.spec_from_file_location(
    "country_config_module",
    config_directory + country_config_file
)
country_config_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(country_config_module)
country_config = country_config_module.country_config
