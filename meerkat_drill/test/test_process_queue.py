from unittest import TestCase
from unittest.mock import patch

import meerkat_drill
import meerkat_drill.redis
from meerkat_drill.test.mocks import RedisMock

INIT_DATA_LENGTH = 10

class TestProcessQueue(TestCase):
    def setUp(self):
        self.redis_mock = RedisMock()
        messages = [bytes(f"message{i}", 'utf-8') for i in range(INIT_DATA_LENGTH)]
        self.redis_mock.create_init_data(messages)
        meerkat_drill.redis.redis_connection = self.redis_mock
        meerkat_drill.redis.BATCH_COLLECTION_TIMEOUT = 5

    @patch('meerkat_drill.sqs.sts_client')
    @patch('meerkat_drill.sqs.sns_client')
    @patch('meerkat_drill.sqs.sqs_client')
    def test_process_queue(self, sqs_mock, *mocks):
        sqs_mock.send_message_batch.return_value = {
            'Successful': [
                {
                    'Id': i,
                    'Message': f"message{i}"
                } for i in range(INIT_DATA_LENGTH)
            ]
        }
        meerkat_drill.process_queue()

        self.assertEqual([], self.redis_mock.in_progress_queue)

    @patch('meerkat_drill.sqs.sts_client')
    @patch('meerkat_drill.sqs.sns_client')
    @patch('meerkat_drill.sqs.sqs_client')
    def test_process_queue_failes_for_all_messages(self, sqs_mock, *mocks):
        sqs_mock.send_message_batch.return_value = {
            'Failed': [
                {
                    'Id': i,
                    'SenderFault': False,
                    'Message': f"message{i}"
                } for i in range(INIT_DATA_LENGTH)
            ]
        }
        meerkat_drill.process_queue()

        actual_unsuccesful_count = len(self.redis_mock.in_progress_queue)
        self.assertEqual(actual_unsuccesful_count, INIT_DATA_LENGTH)
