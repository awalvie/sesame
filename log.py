import logging

logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)


formatter = logging.Formatter(
    ('{"time":"%(asctime)s", "level":"%(levelname)s", "msg":"%(message)s"},')
)

ch = logging.StreamHandler()
ch.setFormatter(formatter)

ch.setLevel(logging.INFO)
logger.addHandler(ch)
