import pika
from meerkat_drill import config
from meerkat_drill import logger

QUEUE_NAME = 'nest-queue-' + config.country_queue_name

logger.info(f"Connecting to {config.rabbit_url}")
connection = pika.BlockingConnection(pika.URLParameters(config.rabbit_url))
channel = connection.channel()
channel.confirm_delivery()
channel.queue_declare(queue=QUEUE_NAME, durable=True)

# connection.close()


def send_batch_entries_to_rabbit(entries):
    global connection
    global channel

    response = {}
    for entry in entries:
        try:
            res = channel.basic_publish(exchange='',
                                        routing_key=QUEUE_NAME,
                                        properties=pika.BasicProperties(
                                            delivery_mode=2,  # make message persistent
                                        ),
                                        body=entry["MessageBody"])
        except pika.exceptions.ConnectionClosed:
            connection = pika.BlockingConnection(pika.URLParameters(config.rabbit_url))
            channel = connection.channel()
            channel.confirm_delivery()
            channel.queue_declare(queue=QUEUE_NAME, durable=True)
        if res:
            response.setdefault("Successful", [])
            response["Successful"].append({"Id": entry["Id"]})
        else:
            response.setdefault("Failed", [])
            response["Failed"].append({"Id": entry["Id"]})
    return response
