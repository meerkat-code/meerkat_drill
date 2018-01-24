class RedisMock():
    def __init__(self):
        self.incoming_queue = []
        self.in_progress_queue = []

    def brpoplpush(self, *args):
        if self.incoming_queue:
            item = self.incoming_queue.pop(0)
            self.in_progress_queue.append(item)
            return item
        else:
            return None

    def lrem(self, queue_name, op_type, item):
        self.in_progress_queue.remove(item)

    def create_init_data(self, initial_messages: list):
        self.incoming_queue = initial_messages


def mock_redis():
    return RedisMock()

