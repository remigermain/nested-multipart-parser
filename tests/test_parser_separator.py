from nested_multipart_parser import NestedParser
from unittest import TestCase


class TestSettingsSeparator(TestCase):
    def test_parser_object(self):
        data = {"title.id.length": "lalal"}
        parser = NestedParser(data, {"separator": "dot"})
        self.assertTrue(parser.is_valid())
        expected = {"title": {"id": {"length": "lalal"}}}
        self.assertEqual(expected, parser.validate_data)

    def test_parser_object2(self):
        data = {"title.id.length": "lalal", "title.id.value": "lalal"}
        parser = NestedParser(data, {"separator": "dot"})
        self.assertTrue(parser.is_valid())
        expected = {"title": {"id": {"length": "lalal", "value": "lalal"}}}
        self.assertEqual(expected, parser.validate_data)

    def test_parser_object3(self):
        data = {
            "title.id.length": "lalal",
            "title.id.value": "lalal",
            "title.id.value": "lalal",
            "title.value": "lalal",
        }
        parser = NestedParser(data, {"separator": "dot"})
        self.assertTrue(parser.is_valid())
        expected = {
            "title": {"id": {"length": "lalal", "value": "lalal"}, "value": "lalal"}
        }
        self.assertEqual(expected, parser.validate_data)

    def test_parser_object4(self):
        data = {
            "title.id.length": "lalal",
            "title.id.value": "lalal",
            "title.id.value": "lalal",
            "title.value": "lalal",
            "sub": "lalal",
            "title.id.recusrive.only.field": "icci",
        }
        parser = NestedParser(data, {"separator": "dot"})
        self.assertTrue(parser.is_valid())
        expected = {
            "title": {
                "id": {
                    "length": "lalal",
                    "value": "lalal",
                    "recusrive": {"only": {"field": "icci"}},
                },
                "value": "lalal",
            },
            "sub": "lalal",
        }
        self.assertEqual(expected, parser.validate_data)

    def test_parser_object_reasing2(self):
        data = {
            "title.id.length": "lalal",
            "title.value": "lalal",
            "sub": "lalal",
            "title.id.recusrive.only.field": "icci",
        }
        parser = NestedParser(data, {"separator": "dot"})
        self.assertTrue(parser.is_valid())
        expected = {
            "title": {
                "id": {
                    "length": "lalal",
                    "recusrive": {
                        "only": {"field": "icci"},
                    },
                },
                "value": "lalal",
            },
            "sub": "lalal",
        }
        self.assertEqual(expected, parser.validate_data)

    def test_parser_classic(self):
        data = {"title": "lalal"}
        parser = NestedParser(data, {"separator": "dot"})
        self.assertTrue(parser.is_valid())
        expected = {"title": "lalal"}
        self.assertDictEqual(expected, parser.validate_data)

    def test_parser_list_out_index(self):
        data = {
            "title": "dddddddddddddd",
            "tist.0": "lalal",
            "tist.2": "lalal",
        }
        parser = NestedParser(data, {"separator": "dot"})
        self.assertFalse(parser.is_valid())

    def test_parser_empty_list_out_index(self):
        data = {
            "title": "dddddddddddddd",
            "tist.0": "lalal",
            "tist.": "lalal",
        }
        parser = NestedParser(data, {"separator": "dot"})
        self.assertFalse(parser.is_valid())

    def test_parser_list(self):
        data = {"title": "lalal", "list.0": "icicici"}
        parser = NestedParser(data, {"separator": "dot"})
        expected = {"title": "lalal", "list": ["icicici"]}
        self.assertTrue(parser.is_valid())
        self.assertEqual(expected, parser.validate_data)

    def test_parser_list_index_out_of_range(self):
        data = {"title": "lalal", "list.0": "icicici"}
        parser = NestedParser(data, {"separator": "dot"})
        self.assertTrue(parser.is_valid())
        expected = {"title": "lalal", "list": ["icicici"]}
        self.assertEqual(expected, parser.validate_data)

    def test_parser_list_object_index(self):
        data = {"title": "lalal", "list.length.0": "icicici"}
        parser = NestedParser(data, {"separator": "dot"})
        expected = {"title": "lalal", "list": {"length": ["icicici"]}}
        self.assertTrue(parser.is_valid())
        self.assertEqual(expected, parser.validate_data)

    def test_parser_space_key(self):
        data = {
            "title ": "lalal",
        }
        parser = NestedParser(data, {"separator": "dot"})
        self.assertFalse(parser.is_valid())

    def test_real(self):
        data = {
            "title": "title",
            "date": "time",
            "langs.0.id": "id",
            "langs.0.title": "title",
            "langs.0.description": "description",
            "langs.0.language": "language",
            "langs.1.id": "id1",
            "langs.1.title": "title1",
            "langs.1.description": "description1",
            "langs.1.language": "language1",
        }
        parser = NestedParser(data, {"separator": "dot"})
        self.assertTrue(parser.is_valid())
        expected = {
            "title": "title",
            "date": "time",
            "langs": [
                {
                    "id": "id",
                    "title": "title",
                    "description": "description",
                    "language": "language",
                },
                {
                    "id": "id1",
                    "title": "title1",
                    "description": "description1",
                    "language": "language1",
                },
            ],
        }
        self.assertDictEqual(parser.validate_data, expected)

    def test_parser_rewrite_key_list(self):
        data = {
            "title": "lalal",
            "title.0": "lalal",
        }
        parser = NestedParser(data, {"separator": "dot"})
        self.assertFalse(parser.is_valid())

    def test_parser_rewrite_key_boject(self):
        data = {
            "title": "lalal",
            "title.object": "lalal",
        }
        parser = NestedParser(data, {"separator": "dot"})
        self.assertFalse(parser.is_valid())
