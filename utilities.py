import os
import psycopg2
import discord
from conversationData import data
from chatter import Chatter

import appSettings

_connection = None
_client = None
_state = appSettings.defaultState
_chatter = Chatter(data)

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

def getChatter():
    global _chatter
    return _chatter