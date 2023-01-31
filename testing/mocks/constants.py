from typing import List

from source.constants.types import TButtons, TReminder, TResult, TTest, TUnfinishedTest, TUser
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


INSERTED_REMINDER: TReminder = {
    "user_id": "63b5e429dda2387a1b602e64",
    "period": "week",
    "chat_id": 5280581822,
    "next": "2023-02-25T13:59:23.325Z"
}


REMINDER_FOR_UPDATE: TUser = {
    "_id": INITIAL_ID,
    "user_id": "63b5e429dda2387a1b602e66",
    "period": "day",
    "chat_id": 5280581823,
    "next": "2023-02-22T13:59:23.325Z"
}


INITIAL_REMINDERS: TReminder = [
    {
        "user_id": "63b5e429dda2387a1b602e53",
        "period": "2weeks",
        "chat_id": 5280581800,
        "next": "2023-02-26T13:59:23.325Z"
    },
    REMINDER_FOR_UPDATE,
    {
        "user_id": "63b5e429dda2387a1b606t89",
        "period": "day",
        "chat_id": 5280581800,
        "next": "2023-02-23T13:59:23.325Z"
    }
]


UNFINISHED_FOR_UPDATE: TUnfinishedTest = {
    "chat_id": 5280581822,
    "test_name": "Тест Бека (депрессия)",
    "data": [2, 3, 1],
    "userId": "63b5e429dda2387a1b602e58",
    "_id": INITIAL_ID
}


INSERTED_UNFINISHED: TUnfinishedTest = {
    "chat_id": 5280581824,
    "test_name": "Тест Бека (депрессия)",
    "data": "2022-01-17T21:01:38.446Z",
    "userId": "63b5e429dda2387a1b602y83"
}


INITIAL_UNFINISHED_TESTS: List[TUnfinishedTest] = [
    {
        "chat_id": 52805818276,
        "test_name": "Тест Бека (депрессия)",
        "data": "2022-01-14T21:01:38.446Z",
        "userId": "63b5e429dda2387a1b602e44"
    },
    UNFINISHED_FOR_UPDATE,
    {
        "chat_id": 5280581899,
        "test_name": "Тест Бека (депрессия)",
        "data": "2022-01-13T21:01:38.446Z",
        "userId": "63b5e429dda2387a1b602y99"
    }
]


INITIAL_BUTTONS: TButtons = [
    {
        "_id": INITIAL_ID,
        "name": "exit_full",
        "buttons": [
        {
            "text": "exit_full_start",
            "callback_data": "start"
        },
        {
            "text": "exit_full_stat",
            "callback_data": "stat"
        }]
    },
    {
        "name": "testStat",
        "buttons": [
        {
            "text": "testStat_exit",
            "callback_data": "exit_photo"
        }]
    }
]
