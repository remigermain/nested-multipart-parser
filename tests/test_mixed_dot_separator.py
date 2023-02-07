from nested_multipart_parser import NestedParser
from unittest import TestCase


class TestSettingsSeparatorMixedDot(TestCase):
    def test_assign_duplicate_list(self):
        data = {"title": 42, "title[0]": 101}
        p = NestedParser(
            data,
            {
                "raise_duplicate": False,
                "assign_duplicate": True,
                "separator": "mixed-dot",
            },
        )
        self.assertTrue(p.is_valid())
        expected = {"title": [101]}
        self.assertEqual(p.validate_data, expected)

    def test_assign_duplicate_number_after_list(self):
        data = {
            "title[0]": 101,
            "title": 42,
        }
        p = NestedParser(
            data,
            {
                "raise_duplicate": False,
                "assign_duplicate": True,
                "separator": "mixed-dot",
            },
        )
        self.assertTrue(p.is_valid())
        expected = {"title": 42}
        self.assertEqual(p.validate_data, expected)

    def test_assign_nested_duplicate_number_after_list(self):
        data = {
            "title[0].sub[0]": 101,
            "title[0].sub": 42,
        }
        p = NestedParser(
            data,
            {
                "raise_duplicate": False,
                "assign_duplicate": True,
                "separator": "mixed-dot",
            },
        )
        self.assertTrue(p.is_valid())
        expected = {"title": [{"sub": 42}]}
        self.assertEqual(p.validate_data, expected)

    def test_assign_nested_duplicate_number_after_list2(self):
        data = {
            "title[0].sub": 42,
            "title[0].sub[0]": 101,
        }
        p = NestedParser(
            data,
            {
                "raise_duplicate": False,
                "assign_duplicate": True,
                "separator": "mixed-dot",
            },
        )
        self.assertTrue(p.is_valid())
        expected = {"title": [{"sub": [101]}]}
        self.assertEqual(p.validate_data, expected)

    def test_assign_nested_duplicate_number_after_dict(self):
        data = {
            "title[0].sub": 42,
            "title[0].sub.title": 101,
        }
        p = NestedParser(
            data,
            {
                "raise_duplicate": False,
                "assign_duplicate": True,
                "separator": "mixed-dot",
            },
        )
        self.assertTrue(p.is_valid())
        expected = {"title": [{"sub": {"title": 101}}]}
        self.assertEqual(p.validate_data, expected)

    def test_assign_nested_duplicate_number_after_dict2(self):
        data = {
            "title[0].sub.title": 101,
            "title[0].sub": 42,
        }
        p = NestedParser(
            data,
            {
                "raise_duplicate": False,
                "assign_duplicate": True,
                "separator": "mixed-dot",
            },
        )
        self.assertTrue(p.is_valid())
        expected = {"title": [{"sub": 42}]}
        self.assertEqual(p.validate_data, expected)

    def test_mixed_spearator(self):
        data = {
            "title": "lalal",
            "article.object": "lalal",
        }
        parser = NestedParser(data, {"separator": "mixed-dot"})
        self.assertTrue(parser.is_valid())
        expected = {"title": "lalal", "article": {"object": "lalal"}}
        self.assertEqual(expected, parser.validate_data)

    def test_mixed_int_object(self):
        data = {
            "title": "lalal",
            "article.0": "lalal",
        }
        parser = NestedParser(data, {"separator": "mixed-dot"})
        self.assertTrue(parser.is_valid())
        expected = {"title": "lalal", "article": {"0": "lalal"}}
        self.assertEqual(expected, parser.validate_data)

    def test_mixed_int_list(self):
        data = {
            "title": "lalal",
            "article[0]": "lalal",
        }
        parser = NestedParser(data, {"separator": "mixed-dot"})
        self.assertTrue(parser.is_valid())
        expected = {"title": "lalal", "article": ["lalal"]}
        self.assertEqual(expected, parser.validate_data)

    def test_real(self):
        data = {
            "title": "title",
            "date": "time",
            "langs[0].id": "id",
            "langs[0].title": "title",
            "langs[0].description": "description",
            "langs[0].language": "language",
            "langs[1].id": "id1",
            "langs[1].title": "title1",
            "langs[1].description": "description1",
            "langs[1].language": "language1",
        }
        parser = NestedParser(data, {"separator": "mixed-dot"})
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

    def test_mixed_invalid_list_index(self):
        data = {
            "title": "lalal",
            "article[0f]": "lalal",
        }
        parser = NestedParser(data, {"separator": "mixed-dot"})
        self.assertFalse(parser.is_valid())

    def test_mixed_invalid_list_empty_index(self):
        data = {
            "title": "lalal",
            "article[]": None,
        }
        parser = NestedParser(data, {"separator": "mixed-dot"})
        self.assertTrue(parser.is_valid())
        expected = {"title": "lalal", "article": []}
        self.assertDictEqual(parser.validate_data, expected)

    def test_mixed_invalid_bracket(self):
        data = {
            "title": "lalal",
            "article[": "lalal",
        }
        parser = NestedParser(data, {"separator": "mixed-dot"})
        self.assertFalse(parser.is_valid())

    def test_mixed_invalid_bracket2(self):
        data = {
            "title": "lalal",
            "article]": "lalal",
        }
        parser = NestedParser(data, {"separator": "mixed-dot"})
        self.assertFalse(parser.is_valid())

    def test_mixed_invalid_list_dot(self):
        data = {
            "title": "lalal",
            "article[3.]": "lalal",
        }
        parser = NestedParser(data, {"separator": "mixed-dot"})
        self.assertFalse(parser.is_valid())

    def test_mixed_invalid_list_negative_index(self):
        data = {
            "title": "lalal",
            "article[-3]": "lalal",
        }
        parser = NestedParser(data, {"separator": "mixed-dot"})
        self.assertFalse(parser.is_valid())

    def test_mixed_invalid_object(self):
        data = {
            "title": "lalal",
            "article..op": "lalal",
        }
        parser = NestedParser(data, {"separator": "mixed-dot"})
        self.assertFalse(parser.is_valid())

    def test_mixed_invalid_object2(self):
        data = {
            "title": "lalal",
            "article.op.": "lalal",
        }
        parser = NestedParser(data, {"separator": "mixed-dot"})
        self.assertTrue(parser.is_valid())
        expected = {"title": "lalal", "article": {"op": {}}}
        self.assertDictEqual(parser.validate_data, expected)

    def test_mixed_invalid_object3(self):
        data = {
            "title": "lalal",
            "article.op..": "lalal",
        }
        parser = NestedParser(data, {"separator": "mixed-dot"})
        self.assertFalse(parser.is_valid())

    def test_mixed_invalid_object4(self):
        data = {
            "title": "lalal",
            "article[0]op": "lalal",
        }
        parser = NestedParser(data, {"separator": "mixed-dot"})
        self.assertFalse(parser.is_valid())

    def test_mixed_invalid_list_with_object_dot(self):
        data = {
            "title": "lalal",
            "article[0].op..": "lalal",
        }
        parser = NestedParser(data, {"separator": "mixed-dot"})
        self.assertFalse(parser.is_valid())

    def test_mixed_list_with_object_dot2(self):
        data = {
            "title": "lalal",
            "article[0]op[0]e.": "lalal",
        }
        parser = NestedParser(data, {"separator": "mixed-dot"})
        self.assertFalse(parser.is_valid())

    def test_mixed_invalid_list_with_object_dot3(self):
        data = {
            "title": "lalal",
            "article.op.[0]": "lalal",
        }
        parser = NestedParser(data, {"separator": "mixed-dot"})
        self.assertFalse(parser.is_valid())
