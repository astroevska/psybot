from typing import List
from constants.types import TTest
from db.get import getTests


API_TOKEN: str = 't123456789'
MONGODB_CONNECTION: str = "mongodb123456789"
LEGEND_POSITION_Y: float = -0.45
TESTS_CONFIG: List[TTest] = list(getTests())