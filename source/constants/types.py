from threading import Thread
import pandas as pd
from numpy import datetime64, uint64
from datetime import date, datetime, time
from aiogram.types import Message
from dataclasses import astuple, dataclass
from typing import Any, Dict, List, Literal, NewType, TypeVar, TypedDict, Union, Optional


# simple types
TResultDF = type(List[int])
TDBFilters = Dict[str, Any]
TQuestion = NewType('TQuestion', List[str])
TResultData = NewType('TResultData', List[int])
TInterpretor = NewType('TInterpretor', List[Union[int, str]])
TPlotSupportedDataTypes = TypeVar('TPlotSupportedDataTypes', int, float, uint64, datetime, date, time, datetime64)

# types for TESTS_CONFIG
class TTestContent(TypedDict):
    questions: List[TQuestion]
    interpretor: List[TInterpretor]

class TTest(TypedDict):
    name: str
    description: str
    content: TTestContent

class TUnfinishedTest(TypedDict):
    userId: str
    chat_id: str
    datetime: datetime
    test_name: str
    data: TResultData

# types for BUTTONS_CONFIG
class TButtonBase(TypedDict):
    text: str
    callback_data: str

class TButton(TButtonBase):
    condition: str
class TButtonsBase(TypedDict):
    adjust: int
    buttons: List[TButton]

class TButtons(TButtonsBase):
    conditions: List[str]
    message_actions: List[Union[Literal["delete_reply_markup"], Literal["delete"]]]

# type for globals
@dataclass
class TGlobals:
    currentTest: Optional[TTest]
    data: TResultData
    currentUser: str
    currentStartMessage: Optional[Message]
    currentChatId: int
    currentQuestion: int
    result: int
    resultIndex: int
    test_timeout: Thread

    def __iter__(self):
        return iter(astuple(self))

    def __getitem__(self, key):
        return getattr(self, key)


# types for database
class TResulBase(TypedDict):
    userId: int
    test_name: str
    result: int
    date: datetime

class TResult(TResulBase, total=False):
    telegram_id: int

class TUserBase(TypedDict):
    name: str

class TUser(TUserBase, total=False):
    password: str
    email: str
    telegram_id: int
    telegram_username: str

class TReminder(TypedDict):
    user_id: str
    chat_id: int
    period: str
    next: datetime

# types for plot DataFrame
class TResultDFItems(TypedDict):
    result: List[int]
    date: List[date]

class TSendMessage(TypedDict):
    telegram_id: int
    text: str

class TResultDF(pd.DataFrame):
    __class_getitem__ = classmethod(TResultDFItems)

class T2dPlotDF(TypedDict):
    x: str
    y: str

class T2dPlotData(TypedDict):
    data: TResultDF
    x: str
    y: str
