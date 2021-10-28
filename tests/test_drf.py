import unittest
from django.http import QueryDict

from django.conf import settings
settings.configure()

# need to be after settings configure
from rest_framework.test import APIRequestFactory  # noqa: E402
from django.test.client import encode_multipart  # noqa: E402
from nested_multipart_parser.drf import DrfNestedParser, NestedParser  # noqa: E402
from rest_framework.request import Request  # noqa: E402
from rest_framework.exceptions import ParseError  # noqa: E402


def toQueryDict(data):
    q = QueryDict(mutable=True)
    q.update(data)
    q._mutable = False
    return q


class TestDrfParser(unittest.TestCase):

    def test_querydict_mutable(self):
        parser = NestedParser(
            {
                "dtc.key": 'value',
                "dtc.vla": "value2",
                "list[0]": "value1",
                "list[1]": "value2",
                "string": "value",
                "dtc.hh.oo": "sub",
                "dtc.hh.aa": "sub2"
            },
        )
        self.assertTrue(parser.is_valid())
        expected = toQueryDict({
            "dtc": {
                "key": "value",
                "vla": "value2",
                "hh": {
                    "oo": "sub",
                    "aa": "sub2"
                }
            },
            "list": [
                "value1",
                "value2",
            ],
            "string": "value",
        })
        self.assertEqual(parser.validate_data, expected)
        self.assertFalse(parser.validate_data.mutable)

    def test_settings(self):
        from nested_multipart_parser.drf import NestedParser

        data = {
            "article.title": "youpi"
        }
        p = NestedParser(data)
        self.assertTrue(p.is_valid())
        expected = toQueryDict({
            "article": {
                "title": "youpi"
            }
        })
        self.assertEqual(p.validate_data, expected)

        # set settings
        from django.conf import settings
        options = {
            "separator": "dot"
        }
        setattr(settings, 'DRF_NESTED_MULTIPART_PARSER', options)

        p = NestedParser(data)
        self.assertTrue(p.is_valid())
        expected = toQueryDict({
            "article": {
                "title": "youpi"
            }
        })
        self.assertEqual(p.validate_data, expected)

    def parser_boundary(self, data):
        factory = APIRequestFactory()
        content = encode_multipart('BoUnDaRyStRiNg', data)
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        request = factory.put('/notes/547/', content,
                              content_type=content_type)
        return Request(request, parsers=[DrfNestedParser()])

    def test_views(self):
        setattr(settings, 'DRF_NESTED_MULTIPART_PARSER',
                {"separator": "bracket"})
        data = {
            "dtc[key]": 'value',
            "dtc[vla]": "value2",
            "list[0]": "value1",
            "list[1]": "value2",
            "string": "value",
            "dtc[hh][oo]": "sub",
            "dtc[hh][aa]": "sub2"
        }
        results = self.parser_boundary(data)
        expected = toQueryDict({
            "dtc": {
                "key": "value",
                "vla": "value2",
                "hh": {
                    "oo": "sub",
                    "aa": "sub2"
                }
            },
            "list": [
                "value1",
                "value2",
            ],
            "string": "value",
        })
        self.assertEqual(results.data, expected)
        self.assertFalse(results.data.mutable)

    def test_views_options(self):
        setattr(settings, 'DRF_NESTED_MULTIPART_PARSER', {"separator": "dot"})
        data = {
            "dtc.key": 'value',
            "dtc.vla": "value2",
            "list.0": "value1",
            "list.1": "value2",
            "string": "value",
            "dtc.hh.oo": "sub",
            "dtc.hh.aa": "sub2"
        }
        results = self.parser_boundary(data)
        expected = toQueryDict({
            "dtc": {
                "key": "value",
                "vla": "value2",
                "hh": {
                    "oo": "sub",
                    "aa": "sub2"
                }
            },
            "list": [
                "value1",
                "value2",
            ],
            "string": "value",
        })
        self.assertEqual(results.data, expected)
        self.assertFalse(results.data.mutable)

    def test_views_invalid(self):
        setattr(settings, 'DRF_NESTED_MULTIPART_PARSER',
                {"separator": "bracket"})
        data = {
            "dtc[key": 'value',
            "dtc[hh][oo]": "sub",
            "dtc[hh][aa]": "sub2"
        }
        results = self.parser_boundary(data)

        with self.assertRaises(ParseError):
            results.data

    def test_views_invalid_options(self):
        setattr(settings, 'DRF_NESTED_MULTIPART_PARSER',
                {"separator": "invalid"})
        data = {
            "dtc[key]": 'value',
            "dtc[hh][oo]": "sub",
            "dtc[hh][aa]": "sub2"
        }
        results = self.parser_boundary(data)

        with self.assertRaises(AssertionError):
            results.data

    def test_views_options_mixed_invalid(self):
        setattr(settings, 'DRF_NESTED_MULTIPART_PARSER',
                {"separator": "mixed"})
        data = {
            "dtc[key]": 'value',
            "dtc[hh][oo]": "sub",
            "dtc[hh][aa]": "sub2"
        }
        results = self.parser_boundary(data)

        with self.assertRaises(ParseError):
            results.data

    def test_views_options_mixed_valid(self):
        setattr(settings, 'DRF_NESTED_MULTIPART_PARSER',
                {"separator": "mixed"})
        data = {
            "dtc.key": 'value',
            "dtc.hh.oo": "sub",
            "dtc.hh.aa": "sub2"
        }
        results = self.parser_boundary(data)

        expected = {
            "dtc": {
                "key": "value",
                "hh": {
                    "aa": "sub2",
                    "oo": "sub"
                }
            }
        }

        self.assertEqual(results.data, toQueryDict(expected))
