import unittest
from source.utils.helpers import json_serialize

class TestJsonSerialize(unittest.TestCase):
    def test_json_serialize(self):
        data = {"key1": "value1", "key2": "value2"}
        expected_output = '{\n  "key1": "value1",\n  "key2": "value2"\n}'

        self.assertEqual(json_serialize(data), expected_output)

    def test_json_serialize_with_unicode(self):
        data = {"key1": "value1", "key2": "こんにちは"}
        expected_output = '{\n  "key1": "value1",\n  "key2": "こんにちは"\n}'

        self.assertEqual(json_serialize(data), expected_output)

    def test_json_serialize_with_empty_string(self):
        data = ""
        expected_output = "\"\""

        self.assertEqual(json_serialize(data), expected_output)

    def test_json_serialize_with_none(self):
        data = None
        expected_output = 'null'

        self.assertEqual(json_serialize(data), expected_output)

    def test_json_serialize_without_dict(self):
        data = "value"
        expected_output = '"value"'

        self.assertEqual(json_serialize(data), expected_output)

    def test_json_serialize_with_num(self):
        data = 4
        expected_output = '4'

        self.assertEqual(json_serialize(data), expected_output)

    def test_json_serialize_with_empty_list(self):
        data = []
        expected_output = '[]'

        self.assertEqual(json_serialize(data), expected_output)

    def test_json_serialize_with_list(self):
        data = ["value1", "value2", "value3"]
        expected_output = '[\n  "value1",\n  "value2",\n  "value3"\n]'

        self.assertEqual(json_serialize(data), expected_output)


if __name__ == '__main__':
    unittest.main()
