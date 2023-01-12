import json
import pandas as pd

from aiogram.types import User
from bson import json_util
from datetime import date
from functools import reduce
from collections.abc import Iterable, ItemsView
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from constants.data import TESTS_CONFIG
from init.globals import globalsList
from utils.globals import getOrSetCurrentGlobal
from utils.datetime import datetimeToDateStr, strToDate
from constants.types import T2dPlotDF, T2dPlotData, TPlotSupportedDataTypes, TInterpretor


# Telegram Bot data helpers
def getTag(callbackData: str) -> Union[str, bool]:
    splitted = callbackData.split("_")
    return splitted[1] if len(splitted) > 1 else False


def getStartMessage() -> str:
    startText = f"На данный момент в боте доступны следующие тесты:\n\n"
    for i in range(len(TESTS_CONFIG)):
        startText += f"<b>{i + 1}. {TESTS_CONFIG[i]['name']}</b>\n"

    startText += "\nВы можете выбрать любой из них, пройти его, а в дальнейшем отслеживать динамику изменений своего психологического состояния. Тесты постоянно дополняются."
    return startText


def getHelpMessage() -> str:
    return "Ваше состояние вызывает озабоченность. Вам стоит продолжить за ним наблюдать, а также по возможности обратиться к специалисту."


def getResult(interpretor: List[TInterpretor], result: int) -> int:
    for i in range(len(interpretor)):
        if result >= interpretor[i][0] and result <= interpretor[i][1]:
            return i


async def clearTestData(user: User):
    globalsIdx = await getOrSetCurrentGlobal(user)

    globalsList[globalsIdx].data[user.id] = []
    globalsList[globalsIdx].currentQuestion = 0


# Abstract helpers
def getQuotientWithoutRemainder(nums: List[int]) -> int:
    return reduce(lambda acc, item: acc // item, nums)


def trivialFunc(some: Any) -> Any:
    return some


def countRepeats(
    data: Iterable,
    countByKey: str,
    countKey: str,
    additional: Optional[List[Any]] = None,
    wrapKeyFunc: Callable = trivialFunc
) -> ItemsView[str, List[int]]:
    withCountsDict = reduce(lambda acc, item: {**acc, wrapKeyFunc(item[countByKey]):
                                               [
        acc[item[countByKey]][0] + item[countKey],
        acc[item[countByKey]][1] + 1
    ]
        if item[countByKey] in acc else
        [item[countKey], 1]
    }, data, {})

    if additional:
        withCountsDict[additional[0]] = [
            withCountsDict[additional[0]][0] + additional[1],
            withCountsDict[additional[0]][1] + 1] if additional[0] in withCountsDict else [*additional[1:]
                                                                                           ]

    return withCountsDict.items()


def to2dDict(
    dataSource: Iterable[Dict[str, Any]],
    colNames: T2dPlotDF,
    colHandlers: Tuple[Optional[Callable], Optional[Callable]],
    dataHandler: Callable = trivialFunc,
    *dataHandlerArgs: Any
) -> Dict[str, List[TPlotSupportedDataTypes]]:
    return reduce(
        lambda acc, item: {
            colNames['y']: [
                *acc[colNames['y']], colHandlers[1](item[1])
            ],
            colNames['x']: [
                *acc[colNames['x']], colHandlers[0](item[0])
            ]
        },
        dataHandler(dataSource, *colNames.values(), *dataHandlerArgs),
        {colNames['y']: [], colNames['x']: []}
    )


# Plot data helpers
def get2dPlotData(dbGetter: Callable, dbSearchConfig: Dict[str, Union[str, int]], colNames: T2dPlotDF, isCurrent: bool, result: int) -> T2dPlotData:
    return {
        "data": pd.DataFrame(to2dDict(
            dbGetter(dbSearchConfig),
            colNames,
            (strToDate, getQuotientWithoutRemainder),
            countRepeats,
            [str(date.today()), result, 1] if isCurrent and result else None,
            datetimeToDateStr
        )),
        **colNames
    }


def json_serialize(data):
    return str(json.dumps(data, ensure_ascii=False, indent=2, default=json_util.default)).encode().decode('utf-8')
