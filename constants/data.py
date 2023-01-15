from typing import List, Dict

from db.get import getTests
from constants.types import TTest, TButtons


TESTS_CONFIG: List[TTest] = list(getTests())

BUTTONS_CONFIG: Dict[str, TButtons] = [
    {
        "name": "init",
        "mode": "single",
        "adjust": 1,
        "buttons": [
            {
                "text": "Выбрать тест",
                "callback_data": "start"
            },
            {
                "text": "Статистика",
                "callback_data": "stat"
            },
            {
                "text": "Напоминания",
                "callback_data": "reminder"
            }
        ],
    },
    {
        "name": "reminder",
        "mode": "single",
        "adjust": 2,
        "buttons": [
            {
                "text": "Ежедневно",
                "callback_data": "every_day"
            },
            {
                "text": "Каждую неделю",
                "callback_data": "every_week"
            },
            {
                "text": "2 раза в месяц",
                "callback_data": "every_2weeks"
            },
            {
                "text": "Каждый месяц",
                "callback_data": "every_month"
            },
            {
                "text": "Удалить",
                "callback_data": "removeReminder",
                "condition": "hasReminders"
            },
            {
                "text": "Выход",
                "callback_data": "exit_full"
            }
        ]
    },
    {
        "name": "stat",
        "mode": "single",
        "adjust": 1,
        "buttons": [
            {
                "text": "Выход",
                "callback_data": "exit_fullPhoto"
            }
        ]
    },
    {
        "name": "exit_full",
        "mode": "single",
        "adjust": 2,
        "buttons": [
            {
                "text": "Выбрать тест",
                "callback_data": "start"
            },
            {
                "text": "Статистика",
                "callback_data": "stat"
            },
            {
                "text": "Напоминания",
                "callback_data": "reminder"
            }
        ]
    },
    {
        "name": "exit_photo",
        "mode": "single",
        "adjust": 2,
        "buttons": [
            {
                "text": "Выбрать тест",
                "callback_data": "start"
            },
            {
                "text": "Статистика",
                "callback_data": "stat"
            },
            {
                "text": "Напоминания",
                "callback_data": "reminder"
            }
        ]
    },
    {
        "name": "exit_fullPhoto",
        "mode": "single",
        "adjust": 2,
        "buttons": [
            {
                "text": "Выбрать тест",
                "callback_data": "start"
            },
            {
                "text": "Напоминания",
                "callback_data": "reminder"
            }
        ]
    },
    {
        "name": "exit_simple",
        "mode": "single",
        "adjust": 2,
        "buttons": [
            {
                "text": "Продолжить",
                "callback_data": "next_"
            },
            {
                "text": "Выбрать тест",
                "callback_data": "start"
            },
            {
                "text": "Выход",
                "callback_data": "exit_full"
            }
        ]
    },
    {
        "name": "next_",
        "mode": "",
        "adjust": 2,
        "buttons": [
            {
                "text": "Выбрать тест",
                "callback_data": "start"
            },
            {
                "text": "Напоминания",
                "callback_data": "reminder"
            }
        ]
    },
    {
        "name": "test_",
        "mode": "single",
        "adjust": 1,
        "buttons": [
            {
                "text": "Продолжить",
                "callback_data": "next_"
            },
            {
                "text": "Выход",
                "callback_data": "start"
            }
        ]
    },
    {
        "name": "testStat",
        "mode": "single",
        "adjust": 1,
        "buttons": [
            {
                "text": "Выход",
                "callback_data": "exit_photo"
            }
        ]
    },
]