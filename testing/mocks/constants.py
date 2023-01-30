from typing import List

from source.constants.types import TReminder, TResult, TTest, TUser
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
    }
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

USER_FOR_UPDATE: TUser = {
    "name": "user 2",
    "telegram_id": 5376281834,
    "telegram_username": "user2_tg",
    "_id": INITIAL_ID
}

INSERTED_USER: TUser = {
    "name": "user4",
    "telegram_id": 5222582222,
    "telegram_username": "user4_tg"
}

INITIAL_USERS: TUser = [
    {
        "name": "user1",
        "telegram_id": 5286581834,
        "telegram_username": "user1_tg"
    },
    USER_FOR_UPDATE,
    {
        "name": "user3",
        "telegram_id": 5611111834,
        "telegram_username": "user3_tg"
    }
]

INSERTED_RESULT: TResult = {
    "telegram_id": 5222582222,
    "test_name": "Тест Бека (депрессия)",
    "userId": "77d4e0ec4a669a4998b3aa81",
    "result": 53,
}


INITIAL_RESULTS: TResult = [
    {
        "_id": INITIAL_ID,
        "telegram_id": 5222582333,
        "userId": "77d4e0ec4a669a4778b3aa81",
        "test_name": "Тест Бека (депрессия)",
        "result": 18,
        "date": "2022-03-14T00:20:19.066Z"
    },
    {
        "telegram_id": 5222582666,
        "userId": "77d4e0ec4a669a4998b3aa81",
        "test_name": "Тест Бека (депрессия)",
        "result": 26,
        "date": "2022-02-14T00:20:19.066Z"
    }
]


INITIAL_REMINDERS: TReminder = [
    {
        "_id": INITIAL_ID,
        "user_id": "63b5e429dda2387a1b602e53",
        "period": "2weeks",
        "chat_id": 5280581800,
        "next": "2023-02-26T13:59:23.325Z"
    },
    {
        "user_id": "63b5e429dda2387a1b606t89",
        "period": "day",
        "chat_id": 5280581800,
        "next": "2023-02-23T13:59:23.325Z"
    }
]
