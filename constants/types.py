import pandas as pd
from datetime import date, datetime
from aiogram.types import Message
from dataclasses import astuple, dataclass
from typing import Dict, List, NewType, TypedDict, Union, Optional


# simple types
TResultDF = type(List[int])
TQuestion = NewType('TQuestion', List[str])
TResultData = NewType('TResultData', Dict[str, List[int]])
TInterpretor = NewType('TInterpretor', List[Union[int, str]])

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
    currentStartMessage: Optional[Message]
    currentQuestion: int
    result: int
    resultIndex: int

    def __iter__(self):
        return iter(astuple(self))
    
    def __getitem__(self, keys):
        return iter(getattr(self, k) for k in keys)

# types for database
class TResult:
    telegram_id: int
    test_name: str
    result: int
    date: datetime

# types for plot DataFrame
class TResultDFItems(TypedDict):
    result: List[int]
    date: List[date]

class TResultDF(pd.DataFrame):
    __class_getitem__ = classmethod(TResultDFItems)
