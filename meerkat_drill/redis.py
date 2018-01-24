from time import time

import redis

from meerkat_drill import config, logger

BATCH_COLLECTION_TIMEOUT = 60
TIMEOUT = 10
REDIS_QUEUE_NAME = 'nest-queue-' + config.country_queue_name
REDIS_IN_PROGRESS_QUEUE_NAME = 'nest-in-progress-queue-' + config.country_queue_name

redis_connection = redis.StrictRedis(host='redis', port=6379, db=0)


def fetch_messages_from_queue(count):
    logger.info("Starting fetching messages from redis queue {}.".format(REDIS_QUEUE_NAME))
    result = []
    start_time = time()
    elapsed_time = time() - start_time
    while elapsed_time < BATCH_COLLECTION_TIMEOUT and len(result) < count:
        message = __get_message()
        if message:
            result.append(message)
        elapsed_time = time() - start_time
    logger.info(f"Fetched {len(result)} records in {int(elapsed_time)} second.")
    return result


def __get_message():
    return redis_connection.brpoplpush(REDIS_QUEUE_NAME, REDIS_IN_PROGRESS_QUEUE_NAME, TIMEOUT)


def remove_message_from_in_process_queue(message_sent):
    redis_connection.lrem(REDIS_IN_PROGRESS_QUEUE_NAME, 0, message_sent)