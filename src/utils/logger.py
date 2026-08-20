import logging
import os
import re

from src.utils.config_loader import load_config, resolve_path

_ACCOUNT_NUMBER_PATTERN = re.compile(r"\b\d{9,18}\b")


class PIIMaskingFilter(logging.Filter):
    def filter(self, record):
        if isinstance(record.msg, str):
            record.msg = _ACCOUNT_NUMBER_PATTERN.sub(_mask_digits, record.msg)
        return True


def _mask_digits(match):
    value = match.group(0)
    if len(value) <= 4:
        return "*" * len(value)
    return "*" * (len(value) - 4) + value[-4:]


def get_logger(name):
    config = load_config()
    log_file = resolve_path(config["security"]["log_file"])
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    if config["security"]["mask_account_numbers_in_logs"]:
        pii_filter = PIIMaskingFilter()
        file_handler.addFilter(pii_filter)
        stream_handler.addFilter(pii_filter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger
