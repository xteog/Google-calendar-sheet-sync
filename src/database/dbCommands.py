from datetime import datetime
from database.queris import Database


def insertDateTime(database: Database, start: datetime, end: datetime):
    query = "INSERT INTO Schedule (start, end) VALUES (%s, %s)"
    values = (start, end)
    database.cursor.execute(query, values)

    database.database.commit()


def insertUser(database: Database, name: str, email: str):
    query = "INSERT INTO Users (email, name) VALUES (%s, %s)"
    values = (email, name)
    database.cursor.execute(query, values)

    database.database.commit()
