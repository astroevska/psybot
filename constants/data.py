from typing import List

from db.get import getTests
from constants.types import TTest


TESTS_CONFIG: List[TTest] = list(getTests())
