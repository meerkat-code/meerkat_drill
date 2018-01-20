import logging

console = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

console.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(console)


logger.setLevel(logging.INFO)
