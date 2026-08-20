import re

ACCOUNT_NUMBER_PATTERN = re.compile(r"\b\d{9,18}\b")


def mask_account_number(account_number):
    if not account_number:
        return account_number
    digits = re.sub(r"\D", "", account_number)
    if len(digits) <= 4:
        return "*" * len(digits)
    return "*" * (len(digits) - 4) + digits[-4:]


def mask_text(text):
    if not text:
        return text
    return ACCOUNT_NUMBER_PATTERN.sub(lambda m: mask_account_number(m.group(0)), text)
