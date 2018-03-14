# Meerkat Drill

Meerkat Drill is used to consume messages send by Nest and send them to Amazon
SQS or local message queue run with RabbitMQ.

The Docker setup for running Drill together with the rest of the services can be found in the docs of  `Meerkat Country Server` project. It mainly covers setting up Drill's backend db - redis.

The Drill has the following main components:
 * `redis.py` module responsible for message queue connections:
    -   fetches messages from the queue
    -   handles resending of earlier failed messages
 * `sqs.py` module responsible for sending messages to Amazon AWS queue
    - fetches messages from redis and sends them to sqs in batches
    - monitor the status of sent messages and if successful removes them from
    the redis queue

