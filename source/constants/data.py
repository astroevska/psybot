from typing import List, Dict

from ..db.get import getTests, getButtons
from ..constants.types import TTest, TButtons


TESTS_CONFIG: List[TTest] = list(getTests())
BUTTONS_CONFIG: Dict[str, TButtons] = list(getButtons())
