import os
import psycopg2

import appSettings

_connection = None

def getConnection():
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

def cleanUpConnection():
    global _connection
    _connection.close()