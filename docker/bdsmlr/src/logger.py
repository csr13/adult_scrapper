import logging


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[bdsmlr] %(asctime)s - %(levelname)s - %(message)s')
    console_header = logging.StreamHandler()
    console_header.setFormatter(formatter)
    console_header.setLevel(logging.INFO)
    logger.addHandler(console_header)
    return logger
