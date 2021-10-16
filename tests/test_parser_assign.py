from nested_multipart_parser import NestedParser
from unittest import TestCase


class TestSettingsSeparator(TestCase):

    def test_raise_duplicate(self):
        data = {
            "title": 42,
            "title  ": 101
        }
        p = NestedParser(data, {"raise_duplicate": False})
        self.assertTrue(p.is_valid())
        expected = {
            "title": 42
        }
        self.assertEqual(p.validate_data, expected)

    def test_assign_duplicate(self):
        data = {
            "title": 42,
            "title  ": 101
        }
        p = NestedParser(
            data, {"raise_duplicate": False, "assign_duplicate": True})
        self.assertTrue(p.is_valid())
        expected = {
            "title": 101
        }
        self.assertEqual(p.validate_data, expected)

    def test_assign_duplicate_list(self):
        data = {
            "title": 42,
            "title[0]": 101
        }
        p = NestedParser(
            data, {"raise_duplicate": False, "assign_duplicate": True})
        self.assertTrue(p.is_valid())
        expected = {
            "title": [101]
        }
        self.assertEqual(p.validate_data, expected)

    def test_assign_duplicate_number_after_list(self):
        data = {
            "title[0]": 101,
            "title": 42,
        }
        p = NestedParser(
            data, {"raise_duplicate": False, "assign_duplicate": True})
        self.assertTrue(p.is_valid())
        expected = {
            "title": 42
        }
        self.assertEqual(p.validate_data, expected)

    def test_assign_nested_duplicate_number_after_list(self):
        data = {
            "title[0][sub][0]": 101,
            "title[0][sub]": 42,
        }
        p = NestedParser(
            data, {"raise_duplicate": False, "assign_duplicate": True})
        self.assertTrue(p.is_valid())
        expected = {
            "title": [
                {
                    "sub": 42
                }
            ]
        }
        self.assertEqual(p.validate_data, expected)

    def test_assign_nested_duplicate_number_after_list2(self):
        data = {
            "title[0][sub]": 42,
            "title[0][sub][0]": 101,
        }
        p = NestedParser(
            data, {"raise_duplicate": False, "assign_duplicate": True})
        self.assertTrue(p.is_valid())
        expected = {
            "title": [
                {
                    "sub": [101]
                }
            ]
        }
        self.assertEqual(p.validate_data, expected)

    def test_assign_nested_duplicate_number_after_dict(self):
        data = {
            "title[0][sub]": 42,
            "title[0][sub][title]": 101,
        }
        p = NestedParser(
            data, {"raise_duplicate": False, "assign_duplicate": True})
        self.assertTrue(p.is_valid())
        expected = {
            "title": [
                {
                    "sub": {
                        "title": 101
                    }
                }
            ]
        }
        self.assertEqual(p.validate_data, expected)


def test_assign_nested_duplicate_number_after_dict2(self):
    data = {
        "title[0][sub][title]": 101,
        "title[0][sub]": 42,
    }
    p = NestedParser(
        data, {"raise_duplicate": False, "assign_duplicate": True})
    self.assertTrue(p.is_valid())
    expected = {
        "title": [
            {
                "sub": 42
            }
        ]
    }
    self.assertEqual(p.validate_data, expected)
