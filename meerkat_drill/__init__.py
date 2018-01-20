import logging

console = logging.StreamHandler()
logger = logging.getLogger(__name__)
logger.addHandler(console)
logger.setLevel(logging.INFO)
