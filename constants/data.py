from typing import List, Dict
from functools import reduce

from db.get import getTests, getButtons, getTranslates
from constants.types import TTest, TButtons, TTranslation


TESTS_CONFIG: List[TTest] = list(getTests())
BUTTONS_CONFIG: Dict[str, TButtons] = list(getButtons())
TRANSLATIONS: List[TTranslation] = reduce(lambda acc, item: {**acc, item['language']: {"data": item['data'], "buttons": item['buttons']}}, list(getTranslates()), {})
