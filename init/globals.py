from constants.types import TGlobals
from constants.data import TESTS_CONFIG

# TODO: in globals we're storing current session data - test that user chose, 
# data (i don't remember what is it), currentUser (id, i think), currentStartMessage and etc.
# We need to make an array from it. And in each moment when we use globals (use can find it by project finding tab) 
# we need to find necessary object from this array by condition that currentUser == callback.from_user.id. 
# So, you can make it in middleware. Then you can put necessary object to arguments of handler that uses globals.

globals = TGlobals(**{
    'currentTest': TESTS_CONFIG[0],
    'data': dict(),
    'currentUser': "",
    'user': "",
    'currentStartMessage': None,
    'currentQuestion': 0,
    'result': 0,
    'resultIndex': 0
})

