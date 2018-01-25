from unittest import TestCase

import meerkat_drill
from meerkat_drill.test.mocks import RedisMock

MESSAGES_COUNT = 10

class TestInit(TestCase):
    def setUp(self):
        self.redis_mock = RedisMock()
        meerkat_drill.redis.redis_connection = self.redis_mock
        meerkat_drill.redis.BATCH_COLLECTION_TIMEOUT = 5

    def test_init_with_stale_in_progress_messages(self):
        messages = [bytes(f"failed_message{i}", 'utf-8') for i in range(MESSAGES_COUNT)]
        self.redis_mock.set_in_progress_data(messages)

        meerkat_drill.init()
        actual = self.redis_mock.in_progress_queue
        expected = []
        self.assertEqual(expected, actual)

        for message in messages:
            self.assertIn(message, self.redis_mock.incoming_queue)



    def test_init_with_in_progress_and_actual_queue(self):
        old_messages = [bytes(f"failed_message{i}", 'utf-8') for i in range(MESSAGES_COUNT)]
        self.redis_mock.set_in_progress_data(old_messages)
        new_messages = [bytes(f"new_message{i}", 'utf-8') for i in range(MESSAGES_COUNT)]
        self.redis_mock.create_init_data(new_messages)

        meerkat_drill.init()

        actual = self.redis_mock.in_progress_queue
        expected = []
        self.assertEqual(expected, actual)

        for new_message in new_messages:
            self.assertIn(new_message, self.redis_mock.incoming_queue)

        for old_message in old_messages:
            self.assertIn(old_message, self.redis_mock.incoming_queue)

