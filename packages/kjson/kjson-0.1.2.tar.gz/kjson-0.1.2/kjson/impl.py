import json
from datetime import datetime, date, time, timedelta
from decimal import Decimal
from uuid import UUID

import ciso8601

try:
    from django.utils.encoding import force_text
except ImportError:  # pragma: no cover
    force_text = str

try:
    from django.utils.functional import Promise
except ImportError:  # pragma: no cover
    Promise = str


def dumps(*args, **kwargs):
    return json.dumps(*args, cls=Encoder, **kwargs)


def loads(*args, **kwargs):
    return json.loads(*args, cls=Decoder, **kwargs)


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return encode_datetime(obj)
        if isinstance(obj, date):
            return {"__t": "date", "__v": obj.isoformat()}
        elif isinstance(obj, time):
            return encode_time(obj)
        elif isinstance(obj, timedelta):
            return {"__t": "timedelta", "__v": obj.total_seconds()}
        if isinstance(obj, Decimal):
            return {"__t": "Decimal", "__v": str(obj)}
        if isinstance(obj, UUID):
            return {"__t": "UUID", "__v": str(obj)}
        if isinstance(obj, Promise):
            return force_text(obj)

        return super(Encoder, self).default(obj)  # pragma: no cover


class Decoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(Decoder, self).__init__(
            object_hook=type_converter, *args, **kwargs)


def type_converter(o):
    """Convert a type-value dict to a Python type.

    ``o`` is a dict with two keys: ``__t`` and ``__v``, the type and the
    value. ``o`` is returned unchanged when it isn't a dict or when it
    doesn't have the ``__t`` and ``__v`` keys.

    ``type_converter`` supports:

    - datetime.date
    - datetime.datetime
    - datetime.time
    - datetime.timedelta
    - decimal.Decimal
    - uuid.UUID

    A ``NotImplementedError`` is raised when an unsupported type is given.
    """

    if not isinstance(o, dict) or "__t" not in o or "__v" not in o:
        return o

    t, v = o["__t"], o["__v"]

    if t == "datetime":
        return ciso8601.parse_datetime(v)
    if t == "date":
        return ciso8601.parse_datetime(v).date()
    if t == "time":
        return decode_time(v)
    if t == "timedelta":
        return timedelta(seconds=float(v))
    if t == "Decimal":
        return Decimal(v)
    if t == "UUID":
        return UUID(v)

    raise NotImplementedError(f"unknown type: {t}")


def decode_time(s):
    hour = int(s[:2])
    minute = int(s[3:5])
    second = int(s[6:8])
    microsecond = int(s[9:] or 0)
    return time(hour, minute, second, microsecond)


def encode_time(obj):
    if _is_aware(obj):
        raise ValueError("JSON can't represent timezone-aware times.")
    return {"__t": "time", "__v": obj.isoformat()}


def encode_datetime(obj):
    v = obj.isoformat()
    if v.endswith("+00:00"):
        v = v[:-6] + "Z"
    return {"__t": "datetime", "__v": v}


def _is_aware(value):
    return value.utcoffset() is not None
