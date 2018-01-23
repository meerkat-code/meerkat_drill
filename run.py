from time import time

import redis
from meerkat_drill.message_service import send_batch_entries_to_sqs, notify_sns, create_sqs_queue_if_needed
from meerkat_drill import config, logger

MAX_BATCH_SIZE = 10
BATCH_COLLECTION_TIMEOUT = 60
REDIS_QUEUE_NAME = 'nest-queue-' + config.country_queue_name
REDIS_IN_PROGRESS_QUEUE_NAME = 'nest-in-progress-queue-' + config.country_queue_name
redis_ = redis.StrictRedis(host='redis', port=6379, db=0)

def fetch_messages_from_queue(count=MAX_BATCH_SIZE):
    logger.info("Starting fetching messages from redis queue {}.".format(REDIS_QUEUE_NAME))
    result = []
    start_time = time()
    elapsed_time = time() - start_time
    while elapsed_time < BATCH_COLLECTION_TIMEOUT and len(result) < count:
        message = redis_.brpoplpush(REDIS_QUEUE_NAME, REDIS_IN_PROGRESS_QUEUE_NAME, 10)
        if message:
            result.append(message)
        elapsed_time = time() - start_time
    logger.info(f"Fetched {len(result)} records in {int(elapsed_time)} second.")
    return result

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
        logger.info("Succesfully send batch to SQS.")
    logger.info("Removing send messages from redis")
    for success in sqs_response.get('Successful', []):
        message_id = int(success['Id'])
        message_sent = messages[message_id]
        redis_.lrem(REDIS_IN_PROGRESS_QUEUE_NAME, 0, message_sent)

    notify_sns()


def main():
    create_sqs_queue_if_needed()
    while True:
        process_queue()


if __name__ == '__main__':
    main()
