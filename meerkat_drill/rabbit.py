import pika
from meerkat_drill import config
from meerkat_drill import logger

QUEUE_NAME = 'nest-queue-' + config.country_queue_name


def send_batch_entries_to_rabbit(entries):
    connection = pika.BlockingConnection(pika.URLParameters(config.rabbit_url))
    channel = connection.channel()
    channel.confirm_delivery()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    response = {}
    for entry in entries:
        res = channel.basic_publish(exchange='',
                                    routing_key=QUEUE_NAME,
                                    properties=pika.BasicProperties(
                                        delivery_mode=2,  # make message persistent
                                    ),
                                    body=entry["MessageBody"])
        if res:
            response.setdefault("Successful", [])
            response["Successful"].append({"Id": entry["Id"]})
        else:
            response.setdefault("Failed", [])
            response["Failed"].append({"Id": entry["Id"]})

    connection.close()
    logger.debug("Rabbit send message response " + str(response))
    return response
