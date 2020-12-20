import os
import psycopg2
import discord
import re
import sys
from io import StringIO
import contextlib

import appSettings

_connection = None
_client = None
_state = appSettings.defaultState
_chatter = None

def getDBConnection():
    global _connection
    if not _connection:
        if appSettings.isProduction():
            DB_URL = os.environ.get('DATABASE_URL')
            _connection = psycopg2.connect(DB_URL)
        else:
            DB_NAME = os.environ.get('DB_NAME')
            DB_USER = os.environ.get('DB_USER')
            DB_PASSWORD = os.environ.get('DB_PASSWORD')
            _connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host="localhost")
    return _connection

def cleanUpDBConnection():
    global _connection
    _connection.close()

def getPersistantState(key):
    connection = getDBConnection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM global_state WHERE key=%s', (key, ))
        row = cursor.fetchone()
        if row:
            _id, key, value = row
            return value
        else:
            return None

def setPersistantState(key, value):
    connection = getDBConnection()
    with connection.cursor() as cursor:
        if getPersistantState(key):
            cursor.execute('UPDATE global_state SET value=%s WHERE key=%s', (value, key))
        else:
            cursor.execute('INSERT INTO global_state (key, value) VALUES (%s, %s)', (key, value))
        connection.commit()

def getDiscordClient():
    global _client
    if not _client:
        _client = discord.Client()
    return _client

def getState():
    global _state
    return _state.copy()

def setState(state):
    global _state
    _state = state

def startsWithAny(content, tokens):
    for token in tokens:
        if content.startswith(token):
            return True
    return False

def replaceAnyFront(content, tokens, replacement):
    for token in tokens:
        if content.startswith(token):
            return content.replace(token, replacement)
    return content

def betweenQuotes(content):
    return content.split('"')[1::2]

def normalizeText(content):
    return re.sub(r'[^ a-z]', '', str(content).lower()).strip()

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

def evaluatePython(code):
    with stdoutIO() as s:
        try:
            exec(code)
            return s.getvalue()
        except:
            return ("Something is wrong with your code.")