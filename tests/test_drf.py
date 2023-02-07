import unittest

from django.conf import settings
from django.http import QueryDict

settings.configure()

from django.core.files.uploadedfile import (InMemoryUploadedFile,
                                            SimpleUploadedFile)
from django.test.client import encode_multipart  # noqa: E402
from rest_framework.exceptions import ParseError  # noqa: E402
from rest_framework.request import Request  # noqa: E402
# need to be after settings configure
from rest_framework.test import APIRequestFactory  # noqa: E402

from nested_multipart_parser.drf import (DrfNestedParser,  # noqa: E402
                                         NestedParser)


def toQueryDict(data):
    q = QueryDict(mutable=True)
    q.update(data)
    q._mutable = False
    return q


class TestDrfParser(unittest.TestCase):
    def setUp(self):
        # reset settings
        setattr(settings, "DRF_NESTED_MULTIPART_PARSER", {})

    def test_querydict_mutable(self):
        parser = NestedParser(
            {
                "dtc.key": "value",
                "dtc.vla": "value2",
                "list[0]": "value1",
                "list[1]": "value2",
                "string": "value",
                "dtc.hh.oo": "sub",
                "dtc.hh.aa": "sub2",
            },
        )
        self.assertTrue(parser.is_valid())
        expected = toQueryDict(
            {
                "dtc": {
                    "key": "value",
                    "vla": "value2",
                    "hh": {"oo": "sub", "aa": "sub2"},
                },
                "list": [
                    "value1",
                    "value2",
                ],
                "string": "value",
            }
        )
        self.assertEqual(parser.validate_data, expected)
        self.assertFalse(parser.validate_data.mutable)

    def test_settings(self):
        from nested_multipart_parser.drf import NestedParser

        data = {"article.title": "youpi"}
        p = NestedParser(data)
        self.assertTrue(p.is_valid())
        expected = toQueryDict({"article": {"title": "youpi"}})
        self.assertEqual(p.validate_data, expected)

        # set settings
        from django.conf import settings

        options = {"separator": "dot"}
        setattr(settings, "DRF_NESTED_MULTIPART_PARSER", options)

        p = NestedParser(data)
        self.assertTrue(p.is_valid())
        expected = toQueryDict({"article": {"title": "youpi"}})
        self.assertEqual(p.validate_data, expected)

    def parser_boundary(self, data):
        factory = APIRequestFactory()
        content = encode_multipart("BoUnDaRyStRiNg", data)
        content_type = "multipart/form-data; boundary=BoUnDaRyStRiNg"
        request = factory.put("/notes/547/", content, content_type=content_type)
        return Request(request, parsers=[DrfNestedParser()])

    def test_views(self):
        setattr(settings, "DRF_NESTED_MULTIPART_PARSER", {"separator": "bracket"})
        data = {
            "dtc[key]": "value",
            "dtc[vla]": "value2",
            "list[0]": "value1",
            "list[1]": "value2",
            "string": "value",
            "dtc[hh][oo]": "sub",
            "dtc[hh][aa]": "sub2",
        }
        results = self.parser_boundary(data)
        expected = toQueryDict(
            {
                "dtc": {
                    "key": "value",
                    "vla": "value2",
                    "hh": {"oo": "sub", "aa": "sub2"},
                },
                "list": [
                    "value1",
                    "value2",
                ],
                "string": "value",
            }
        )
        self.assertEqual(results.data, expected)
        self.assertFalse(results.data.mutable)

    def test_views_options(self):
        setattr(settings, "DRF_NESTED_MULTIPART_PARSER", {"separator": "dot"})
        data = {
            "dtc.key": "value",
            "dtc.vla": "value2",
            "list.0": "value1",
            "list.1": "value2",
            "string": "value",
            "dtc.hh.oo": "sub",
            "dtc.hh.aa": "sub2",
        }
        results = self.parser_boundary(data)
        expected = toQueryDict(
            {
                "dtc": {
                    "key": "value",
                    "vla": "value2",
                    "hh": {"oo": "sub", "aa": "sub2"},
                },
                "list": [
                    "value1",
                    "value2",
                ],
                "string": "value",
            }
        )
        self.assertEqual(results.data, expected)
        self.assertFalse(results.data.mutable)

    def test_views_invalid(self):
        setattr(settings, "DRF_NESTED_MULTIPART_PARSER", {"separator": "bracket"})
        data = {"dtc[key": "value", "dtc[hh][oo]": "sub", "dtc[hh][aa]": "sub2"}
        results = self.parser_boundary(data)

        with self.assertRaises(ParseError):
            results.data

    def test_views_invalid_options(self):
        setattr(settings, "DRF_NESTED_MULTIPART_PARSER", {"separator": "invalid"})
        data = {"dtc[key]": "value", "dtc[hh][oo]": "sub", "dtc[hh][aa]": "sub2"}
        results = self.parser_boundary(data)

        with self.assertRaises(AssertionError):
            results.data

    def test_views_options_mixed_invalid(self):
        setattr(settings, "DRF_NESTED_MULTIPART_PARSER", {"separator": "mixed"})
        data = {"dtc[key]": "value", "dtc[hh][oo]": "sub", "dtc[hh][aa]": "sub2"}
        results = self.parser_boundary(data)

        with self.assertRaises(ParseError):
            results.data

    def test_views_options_mixed_valid(self):
        setattr(settings, "DRF_NESTED_MULTIPART_PARSER", {"separator": "mixed"})
        data = {"dtc.key": "value", "dtc.hh.oo": "sub", "dtc.hh.aa": "sub2"}
        results = self.parser_boundary(data)

        expected = {"dtc": {"key": "value", "hh": {"aa": "sub2", "oo": "sub"}}}

        self.assertEqual(results.data, toQueryDict(expected))

    def test_output_querydict(self):
        setattr(
            settings,
            "DRF_NESTED_MULTIPART_PARSER",
            {"separator": "mixed", "querydict": False},
        )
        data = {"dtc.key": "value", "dtc.hh.oo": "sub", "dtc.hh.aa": "sub2"}
        results = self.parser_boundary(data)

        expected = {"dtc": {"key": "value", "hh": {"aa": "sub2", "oo": "sub"}}}

        self.assertDictEqual(results.data, expected)

    def test_nested_files(self):
        file = SimpleUploadedFile("file.png", b"file_content", content_type="image/png")
        file1 = SimpleUploadedFile(
            "file.pdf", b"file_content", content_type="application/pdf"
        )

        data = {
            "file": file,
            "title": "title",
            "files[0].description": "description",
            "files[1].file": file1,
            "files[1].description": "description2",
        }
        results = self.parser_boundary(data)

        # files is not in
        expected = {
            "file": file,
            "title": "title",
            "files": [
                {
                    "description": "description",
                },
                {
                    "file": file1,
                    "description": "description2",
                },
            ],
        }
        data = results.data.dict()
        self.assertEqual(len(data), 3)

        self.assertIsInstance(data["file"], InMemoryUploadedFile)
        self.assertEqual(data["title"], expected["title"])

        self.assertEqual(len(data["files"]), 2)
        self.assertIsInstance(data["files"], list)

        self.assertIsInstance(data["files"][0], dict)
        self.assertEqual(len(data["files"][0]), 1)
        self.assertEqual(data["files"][0]["description"], "description")

        self.assertIsInstance(data["files"][1], dict)
        self.assertEqual(len(data["files"][1]), 2)
        self.assertEqual(data["files"][1]["description"], "description2")
        self.assertIsInstance(data["files"][1]["file"], InMemoryUploadedFile)

    def test_nested_files_index_not_order(self):
        file = SimpleUploadedFile("file.png", b"file_content", content_type="image/png")
        file1 = SimpleUploadedFile("file.pdf", b"file_content", content_type="application/pdf")

        data = {
            "files[2]": file1,
            "files[1].description": "description2",
            "files[1].file": file,
            "files[0].description": "description",
        }
        results = self.parser_boundary(data)

        data = results.data.dict()
        self.assertEqual(len(data), 1)

        self.assertEqual(len(data["files"]), 3)
        self.assertIsInstance(data["files"], list)

        self.assertIsInstance(data["files"][0], dict)
        self.assertEqual(len(data["files"][0]), 1)
        self.assertEqual(data["files"][0]["description"], "description")

        self.assertIsInstance(data["files"][1], dict)
        self.assertEqual(len(data["files"][1]), 2)
        self.assertEqual(data["files"][1]["description"], "description2")
        self.assertIsInstance(data["files"][1]["file"], InMemoryUploadedFile)
    
        self.assertIsInstance(data["files"][2], InMemoryUploadedFile)