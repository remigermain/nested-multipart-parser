import unittest
from django.http import QueryDict


def toQueryDict(data):
    q = QueryDict(mutable=True)
    q.update(data)
    q._mutable = False
    return q


class TestDrfParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        from django.conf import settings
        settings.configure()

    def test_querydict_mutable(self):
        from nested_multipart_parser.drf import NestedParser

        parser = NestedParser(
            {
                "dtc[key]": 'value',
                "dtc[vla]": "value2",
                "list[0]": "value1",
                "list[1]": "value2",
                "string": "value",
                "dtc[hh][oo]": "sub",
                "dtc[hh][aa]": "sub2"
            }
        )
        self.assertTrue(parser.is_valid())
        q = toQueryDict({
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
        self.assertEqual(parser.validate_data, q)
        self.assertFalse(parser.validate_data.mutable)

    def test_settings(self):
        from nested_multipart_parser.drf import NestedParser

        data = {
            "article.title": "youpi"
        }
        p = NestedParser(data)
        self.assertTrue(p.is_valid())
        expected = toQueryDict({
            "article.title": "youpi"
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
