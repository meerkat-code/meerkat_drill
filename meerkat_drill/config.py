import os

# If local set to true, custom sqs endpoint will be used from SQS_ENDPOINT
LOCAL = os.environ.get('LOCAL', False) == 'True'
SQS_ENDPOINT = os.environ.get('SQS_ENDPOINT', 'http://tunnel:9324')

COUNTRY_QUEUE_NAME = os.environ.get("COUNTRY_NAME", "demo").lower()

SQS_QUEUE_URL = os.environ.get("SQS_QUEUE_URL", None)
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN", None)
