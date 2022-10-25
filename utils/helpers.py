from functools import reduce
from typing import Any, Callable, Iterable, List, Optional

from init.globals import globals
from constants.types import TInterpretor
from constants.config import TESTS_CONFIG

def getTag(callbackData: str) -> str:
    return callbackData.split("_")[1]

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

def clearTestData(userId: int):    
    globals.data[userId] = []
    globals.currentQuestion = 0

def trivialFunc(some: Any) -> Any:
    return some

def countRepeats(
    data: Iterable,
    countByKey: str,
    countKey: str,
    additional: Optional[List[Any]] = None,
    wrapKeyFunc: Callable = trivialFunc
):
    withCountsDict = reduce(lambda acc, item: { **acc, wrapKeyFunc(item[countByKey]):
            [
                acc[item[countByKey]][0] + item[countKey],
                acc[item[countByKey]][1] + 1
            ]
        if item[countByKey] in acc else
            [ item[countKey], 1 ]
    }, data, {})
    
    if additional: withCountsDict[additional[0]] = [
        withCountsDict[additional[0]][0] + additional[1],
        withCountsDict[additional[0]][1] + 1 ] if additional[0] in withCountsDict else [*additional[1:]
    ]
    
    return withCountsDict.items()