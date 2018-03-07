from meerkat_drill.sqs import create_sqs_queue_if_needed
from meerkat_drill import process_queue, init, config


def main():
    if config.external_message_queue == "SQS":
        create_sqs_queue_if_needed()
    init()
    while True:
        process_queue()


if __name__ == '__main__':
    main()
