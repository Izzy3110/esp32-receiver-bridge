import os
import random
import uuid
from datetime import datetime
import pytz


def localize_datetime(datetime_str: str):
    return (
        pytz.timezone(os.getenv("TZ"))
        .localize(datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S"))
        .isoformat()
    )


def format_value(value):
    if isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, bool):
        return str(value).lower()
    else:
        return value


def generate_random_float(min_value, max_value):
    random_float = random.uniform(min_value, max_value)
    return round(random_float, 2)


def generate_short_uuid(length=10):
    full_uuid = uuid.uuid4().hex
    return full_uuid[:length]
