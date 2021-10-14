import unittest
from django.http import QueryDict


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
        q = QueryDict(mutable=True)
        q.update({
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
        q.mutable = False
        self.assertEqual(parser.validate_data, q)
        self.assertFalse(parser.validate_data.mutable)
