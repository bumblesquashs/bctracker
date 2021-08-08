import sqlite3

connection = None

def connect():
    global connection
    connection = sqlite3.connect('data/bctracker.db')

def disconnect():
    global connection
    connection.close()
    connection = None

def execute(sql, args=None):
    connection.cursor().execute(sql, args)
