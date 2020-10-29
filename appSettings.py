import os

def isProduction():
    return os.environ.get('ENV') == 'production'