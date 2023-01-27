from typing import List, Dict

from source.db.get import getTests, getButtons
from source.constants.types import TTest, TButtons


TESTS_CONFIG: List[TTest] = list(getTests())
BUTTONS_CONFIG: Dict[str, TButtons] = list(getButtons())
