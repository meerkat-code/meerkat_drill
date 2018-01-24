from meerkat_drill.sqs import create_sqs_queue_if_needed
from meerkat_drill import process_queue


def main():
    create_sqs_queue_if_needed()
    while True:
        process_queue()


if __name__ == '__main__':
    main()
