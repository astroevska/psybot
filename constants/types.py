import pandas as pd
from datetime import date
from aiogram.types import Message
from dataclasses import astuple, dataclass
from typing import Dict, List, NewType, TypedDict, Union, Optional


TResultDF = type(List[int])
TQuestion = NewType('TQuestion', List[str])
TResultData = NewType('TResultData', Dict[str, List[int]])
TInterpretor = NewType('TInterpretor', List[Union[int, str]])

class TTestContent(TypedDict):
    questions: List[TQuestion]
    interpretor: List[TInterpretor]

class TTest(TypedDict):
    name: str
    description: str
    content: TTestContent

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

class TResultDFItems(TypedDict):
    result: List[int]
    date: List[date]

class TResultDF(pd.DataFrame):
    __class_getitem__ = classmethod(TResultDFItems)
