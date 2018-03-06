import logging
from meerkat_drill import config
console = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

console.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(console)

logger.setLevel(logging.INFO)

from meerkat_drill.redis import fetch_messages_from_queue, redis_connection, REDIS_IN_PROGRESS_QUEUE_NAME, \
    remove_message_from_in_process_queue, resend_any_stale_in_progress_messages
from meerkat_drill.sqs import MAX_BATCH_SIZE, send_batch_entries_to_sqs, notify_sns

from meerkat_drill.rabbit import send_batch_entries_to_rabbit

def init():
    resend_any_stale_in_progress_messages()


def process_queue():
    messages = fetch_messages_from_queue(MAX_BATCH_SIZE)
    entries = []
    logger.info(f"Got {len(messages)} message batch. Processing...")
    for i, message in enumerate(messages):
        entries.append(
            {
                "Id": str(i),
                "MessageBody": message.decode("utf-8")
            }
        )

    if entries:
        response = send_batch_entries(entries)
    else:
        logger.info("Empty batch. No action needed.")
        return
    if response.get('Failed'):
        logger.error("Failed to send some messages to the external message queue")
    else:
        on_success(messages, response)
    notify_sucess()


def send_batch_entries(entries):
    if config.external_message_queue == "SQS":
        response = send_batch_entries_to_sqs(entries)
    elif config.external_message_queue == "rabbitMQ":
        response = send_batch_entries_to_rabbit(entries)
    else:
        raise NotImplementedError("External queue type not implemented")
    return response


def notify_sucess():
    if config.external_message_queue == "SQS":
        notify_sns()


def on_success(messages, sqs_response):
    logger.info("Succesfully send batch to external queue.")
    logger.info("Removing send messages from redis")
    for success in sqs_response.get('Successful', []):
        message_id = int(success['Id'])
        message_sent = messages[message_id]
        remove_message_from_in_process_queue(message_sent)
