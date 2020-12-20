import os
from collections import defaultdict

def isProduction():
    return os.environ.get('ENV') == 'production'

defaultState = {
    "secretSantaIsIniting": False,
    "gpt-3_context": defaultdict(list)
}

MAX_CONTEXT_SIZE = 3