"""
Data resource for interacting with Amazon Simple Queue Service
"""
import json

import boto3
from meerkat_drill import logger

from meerkat_drill import config

AWS_REGION_NAME = 'eu-west-1'
SQS_QUEUE_NAME = 'nest-queue-' + config.country_queue_name
DEAD_LETTER_QUEUE_NAME = 'nest-dead-letter-queue-' + config.country_queue_name

if hasattr(config, "LOCAL") and config.LOCAL:
    sqs_client = boto3.client('sqs', region_name=AWS_REGION_NAME,
                              endpoint_url=config.SQS_ENDPOINT)
else:
    sqs_client = boto3.client('sqs', region_name=AWS_REGION_NAME)
sts_client = boto3.client('sts', region_name=AWS_REGION_NAME)
sns_client = boto3.client('sns', region_name=AWS_REGION_NAME)

def get_account_id():
    """
    Returns AWS account ID

    Returns:\n
        account ID for the configured AWS user\n
    """
    if hasattr(config, "LOCAL") and config.LOCAL:
        return ""
    account_id = sts_client.get_caller_identity()["Account"]
    return account_id

def send_batch_entries_to_sqs(entries):
    """
    Sends data to an Amazon Simple Message Service queue

    Returns:\n
        'Successful': [
            {
                'Id': 'string',
                'MessageId': 'string',
                'MD5OfMessageBody': 'string',
                'MD5OfMessageAttributes': 'string',
                'SequenceNumber': 'string'
            },
        ],
        'Failed': [
            {
                'Id': 'string',
                'SenderFault': True|False,
                'Code': 'string',
                'Message': 'string'
            },
        ]
}
    """

    response = sqs_client.send_message_batch(
        QueueUrl=get_queue_url(SQS_QUEUE_NAME),
        Entries=entries
    )
    logger.debug("SQS send message response " + str(response))
    return response


def create_queue():
    """
    Creates a queue based on the given data entry
    """
    try:
        queue_name = SQS_QUEUE_NAME
        response = sqs_client.create_queue(
            QueueName=queue_name
        )
        return response
    except Exception as e:
        message = e.args[0]
        message += "\Message queue creation failed."
        e.args = (message,)
        raise

def get_queue_url(queue_name):
    """
    Creates a queue URL based on given queue name

    Returns:\n
        URL for the given queue\n
    """
    if config.sqs_queue_url:
        return config.sqs_queue_url
    response = sqs_client.get_queue_url(
        QueueName=queue_name,
        QueueOwnerAWSAccountId=get_account_id()
    )
    return response['QueueUrl']

def notify_sns():
    """
    Notify Simple Notification service that queue has new data
    """
    message = {
        "queue": SQS_QUEUE_NAME,
        "dead-letter-queue": DEAD_LETTER_QUEUE_NAME
    }

    if config.sns_topic_arn is None:
        topic_arn = create_sns_topic()
    else:
        topic_arn = config.sns_topic_arn
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=json.dumps({'default': json.dumps(message)}),
        MessageStructure='json'
    )
    logger.debug("SNS notification response " + str(response))

def create_sns_topic():
    """
    Creates a SNS topic based on the country configurations

    Returns:\n
        Topic ARN
    """
    topic = sns_client.create_topic(
        Name='nest-incoming-topic-' + config.country_config['country_name'].lower()
    )

    return topic['TopicArn']


def create_sqs_queue_if_needed():
    # Making sure queue is created'
    logger.debug("Creating SQS queue.")
    created = create_queue()
    try:
        assert created, "Queue could not be created"
    except AssertionError as e:
        message = e.args[0]
        message += " Message queue creation failed."
        e.args = (message,)
        raise


MAX_BATCH_SIZE = 10
