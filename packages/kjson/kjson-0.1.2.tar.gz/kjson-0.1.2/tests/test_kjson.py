import json
import unittest
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from uuid import UUID

from django.utils.text import format_lazy
from parameterized import parameterized
from pytz import timezone, utc

from kjson.impl import \
    decode_time, \
    encode_time, encode_datetime, \
    loads, dumps, \
    Encoder, Decoder


t_date = (
    date(2018, 5, 18),
    '{"__t": "date", "__v": "2018-05-18"}',
)
t_datetime = (
    datetime(2018, 5, 18, 11, 5, 53, tzinfo=timezone("Asia/Saigon")),
    '{"__t": "datetime", "__v": "2018-05-18T11:05:53+07:07"}',
)
t_time = (
    time(11, 5, 53, microsecond=500),
    '{"__t": "time", "__v": "11:05:53.000500"}',
)
t_timedelta = (
    timedelta(days=12),
    '{"__t": "timedelta", "__v": 1036800.0}',
)
t_decimal = (
    Decimal("1.55"),
    '{"__t": "Decimal", "__v": "1.55"}',
)
t_uuid = (
    UUID("f2304d9a-b005-4573-a98c-19630c5dde0e"),
    '{"__t": "UUID", "__v": "f2304d9a-b005-4573-a98c-19630c5dde0e"}',
)
t_uuid = (
    UUID("f2304d9a-b005-4573-a98c-19630c5dde0e"),
    '{"__t": "UUID", "__v": "f2304d9a-b005-4573-a98c-19630c5dde0e"}',
)
t_promise = (
    format_lazy('{s}', s="fixed"),
    '"fixed"',
)


TESTDATA = (
    t_date,
    t_datetime,
    t_time,
    t_timedelta,
    t_decimal,
    t_uuid,
    t_promise,
)


class TestDecodeTime(unittest.TestCase):
    @parameterized.expand([
        ('18:57:16.007424', time(18, 57, 16, 7424)),
        ('18:57:16.', time(18, 57, 16)),
        ('18:57:16', time(18, 57, 16)),
    ])
    def test_decode_time(self, input, expected):
        self.assertEqual(decode_time(input), expected)

    @parameterized.expand([
        ('18:57',),
        ('18:57:16.garbage',),
        ('garbage',),
        ('garbage18:57:16',),
    ])
    def test_decode_wrong_time(self, input):
        with self.assertRaises(ValueError):
            decode_time(input)


class TestEncodeTime(unittest.TestCase):
    def test_aware_time(self):
        with self.assertRaises(ValueError):
            encode_time(time(11, 5, 53, tzinfo=utc))


class TestEncodeDateTime(unittest.TestCase):
    def test_microsecond(self):
        self.assertEqual(
            encode_datetime(datetime(2019, 5, 23, microsecond=500)),
            {"__t": "datetime", "__v": "2019-05-23T00:00:00.000500"},
        )

    def test_utc(self):
        self.assertEqual(
            encode_datetime(datetime(2019, 5, 23, tzinfo=utc)),
            {"__t": "datetime", "__v": "2019-05-23T00:00:00Z"},
        )


class TestEncoder(unittest.TestCase):
    @parameterized.expand(TESTDATA)
    def test_encoder(self, input, expected_output):
        actual_output = Encoder().encode(input)
        self.assertEqual(actual_output, expected_output)

    @parameterized.expand(TESTDATA)
    def test_dumps(self, input, expected_output):
        actual_output = dumps(input)
        self.assertEqual(actual_output, expected_output)


class TestDecoder(unittest.TestCase):
    @parameterized.expand(TESTDATA)
    def test_decoder(self, expected_output, input):
        actual_output = Decoder().decode(input)
        self.assertEqual(actual_output, expected_output)

    @parameterized.expand(TESTDATA)
    def test_loads(self, expected_output, input):
        actual_output = loads(input)
        self.assertEqual(actual_output, expected_output)

    @parameterized.expand((
        ['{"__t": "Decimal", "__x": "1.55"}'],
        ['{"__x": "Decimal", "__v": "1.55"}'],
        ['{"__y": "Decimal"}'],
        ['{"__v": "1.55"}'],
        ['["Decimal", "1.55"]'],
    ))
    def test_invalid_objects(self, value):
        self.assertEqual(loads(value), json.loads(value))

    def test_unsupported_type(self):
        with self.assertRaises(NotImplementedError):
            loads('{"__t": "Unsupported", "__v": "1.55"}')
