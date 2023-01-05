import pandas as pd
from numpy import datetime64, uint64
from datetime import date, datetime, time
from aiogram.types import Message
from dataclasses import astuple, dataclass
from typing import Any, Dict, List, NewType, TypeVar, TypedDict, Union, Optional


# simple types
TResultDF = type(List[int])
TQuestion = NewType('TQuestion', List[str])
TResultData = NewType('TResultData', Dict[str, List[int]])
TInterpretor = NewType('TInterpretor', List[Union[int, str]])
TPlotSupportedDataTypes = TypeVar('TPlotSupportedDataTypes', int, float, uint64, datetime, date, time, datetime64)

# types for TEST_CONFIG
class TTestContent(TypedDict):
    questions: List[TQuestion]
    interpretor: List[TInterpretor]

class TTest(TypedDict):
    name: str
    description: str
    content: TTestContent

# type for globals
@dataclass
class TGlobals:
    currentTest: Optional[TTest]
    data: TResultData
    currentUser: str
    currentStartMessage: Optional[Message]
    currentQuestion: int
    result: int
    resultIndex: int

    def __iter__(self):
        return iter(astuple(self))
    
    def __getitem__(self, keys):
        return iter(getattr(self, k) for k in keys)


# types for database
class TResult(TypedDict):
    telegram_id: int
    test_name: str
    result: int
    date: datetime

class TUser(TypedDict):
    telegram_id: int
    name: str
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

class TResultDF(pd.DataFrame):
    __class_getitem__ = classmethod(TResultDFItems)

class T2dPlotDF(TypedDict):
    x: str
    y: str

class T2dPlotData(TypedDict):
    data: TResultDF
    x: str
    y: str