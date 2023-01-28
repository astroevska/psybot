from typing import List

from source.constants.types import TTest
from bson.objectid import ObjectId


INITIAL_ID = ObjectId('63d4e0ec4a669a4998b3bb81')


TEST_FOR_UPDATE: TTest = {
    "name": "test 2",
    "description": "test two description",
    "content": {
        "questions": ["question 1", "question 2", "question 3"],
        "interpretor": [{"key1": [1, 2]}, {"key2": [3, 4]}, {"key3": [5, 6]}],
    },
    "_id": INITIAL_ID
}


INSERTED_TEST: TTest = {
    "name": "test 4",
    "description": "test 4 description",
    "content": {
        "questions": ["question 1", "question 2", "question 3", "question 4"],
        "interpretor": [{"key1": [1, 2]}, {"key2": [3, 4]}, {"key3": [5, 6]}, {"key4": [7, 8]}],
    },
}


INITIAL_TESTS: List[TTest] = [
    {
        "name": "test 1",
        "description": "test one description",
        "content": {
            "questions": ["question 1", "question 2"],
            "interpretor": [{"key1": [1, 2]}, {"key2": [3, 4]}],
        },
    },
    TEST_FOR_UPDATE,
    {
        "name": "test 3",
        "description": "test three description",
        "content": {
            "questions": ["question 1", "question 2", "question 3", "question 5", "question 6"],
            "interpretor": [{"key1": [1, 2]}, {"key2": [3, 4]}, {"key3": [5, 6]}, {"key4": [7, 8]}, {"key5": [9, 10]}, {"key6": [11, 12]}],
        },
    }
]
