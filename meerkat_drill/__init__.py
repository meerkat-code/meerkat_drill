import logging

from meerkat_drill.redis import fetch_messages_from_queue, redis_connection, REDIS_IN_PROGRESS_QUEUE_NAME, \
    remove_message_from_in_process_queue
from meerkat_drill.sqs import MAX_BATCH_SIZE, send_batch_entries_to_sqs, notify_sns

console = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

console.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(console)

logger.setLevel(logging.INFO)


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
        sqs_response = send_batch_entries_to_sqs(entries)
    else:
        logger.info("Empty batch. No action neede.")
        return
    if sqs_response.get('Failed'):
        logger.error("Failed so send some messages to sqs")
    else:
        on_success(messages, sqs_response)
    notify_sns()


def on_success(messages, sqs_response):
    logger.info("Succesfully send batch to SQS.")
    logger.info("Removing send messages from redis")
    for success in sqs_response.get('Successful', []):
        message_id = int(success['Id'])
        message_sent = messages[message_id]
        remove_message_from_in_process_queue(message_sent)
