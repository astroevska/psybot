from constants.types import TGlobals
from constants.data import TESTS_CONFIG


globals = TGlobals(**{
    'currentTest': TESTS_CONFIG[0],
    'data': dict(),
    'currentUser': "",
    'currentStartMessage': None,
    'currentQuestion': 0,
    'result': 0,
    'resultIndex': 0
})
