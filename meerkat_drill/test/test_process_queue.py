from unittest import TestCase

import meerkat_drill

class TestProcessQueue(TestCase):
    def test_process_queue(self):
        meerkat_drill.process_queue()
