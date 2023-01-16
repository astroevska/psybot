import json
import pandas as pd

from datetime import date
from bson import json_util
from functools import reduce
from threading import Thread
from collections.abc import Iterable, ItemsView
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from utils.datetime import datetimeToDateStr, strToDate
from constants.types import T2dPlotDF, T2dPlotData, TPlotSupportedDataTypes, TInterpretor


def getKeyList(array: List[Any], value: str):
    return list(map(lambda x: x[value], array))


# Telegram Bot data helpers
def getTag(callbackData: str) -> Union[str, bool]:
    splitted = callbackData.split("_")
    return splitted[1] if len(splitted) > 1 else False


def getResult(interpretor: List[TInterpretor], result: int) -> int:
    for i in range(len(interpretor)):
        if result >= interpretor[i][0] and result <= interpretor[i][1]:
            return i


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


def workInParallel(*funcs: List[Callable[[Any], Any]], args: Dict[str, List[Any]]):
    results = []
    for f in funcs:
        t = Thread(target=f, args=args[f.__name__])
        results.append(t)
        
        t.start()
        t.join()

    return results
