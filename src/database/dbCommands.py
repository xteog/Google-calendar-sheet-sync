from datetime import datetime
from database.queris import Database


def insertDateTime(database: Database, start: datetime, end: datetime):
    query = "INSERT INTO schedule (start, end) VALUES (%s, %s)"
    values = (start, end)
    database.cursor.execute(query, values)

    query = """
            SELECT start, email 
            FROM schedule, users
            WHERE start = %s
            """
    values = [start]
    database.cursor.execute(query, values)
    rows = database.cursor.fetchall()

    for row in rows:
        query = "INSERT INTO attendance (date, name) VALUES (%s, %s)"
        values = row
        database.cursor.execute(query, values)

    database.database.commit()


def insertUser(database: Database, name: str, email: str):
    query = "INSERT INTO users (email, name) VALUES (%s, %s)"
    values = (email, name)
    database.cursor.execute(query, values)

    query = """
            SELECT start 
            FROM schedule
            WHERE start > %s;
            """
    values = [datetime.now()]
    database.cursor.execute(query, values)

    dates = database.cursor.fetchall()
    for i in range(len(dates)):
        query = "INSERT INTO attendance (date, user, attendance) VALUES (%s, %s, %s)"
        values = (dates[i][0], email, None)
        database.cursor.execute(query, values)

    database.database.commit()
