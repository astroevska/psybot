from constants.config import TESTS_CONFIG
from constants.types import TGlobals


globals = TGlobals(**{
    'currentTest': TESTS_CONFIG[0],
    'data': dict(),
    'currentStartMessage': None,
    'currentQuestion': 0,
    'result': 0,
    'resultIndex': 0
})
