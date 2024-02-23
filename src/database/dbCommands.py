from datetime import datetime
from database.queris import Database
import google_api.calendar


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

def updateResponse(database: Database, email: str, date: datetime, response: str):
    query = """
            SELECT id, E.start, end, attendee, title, description, response
            FROM Events as E
            JOIN Schedule ON E.start = Schedule.start 
            WHERE attendee = %s AND YEAR(E.start) = %s AND MONTH(E.start) = %s AND DAY(E.start) = %s
            """
    
    values = [email, date.year, date.month, date.day]
    database.cursor.execute(query, values)

    fetched = database.cursor.fetchall()

    e = fetched[0]
    event = google_api.calendar.Event()
    event.id = e[0]
    event.start = e[1]
    event.end = e[2]
    event.attendee = e[3]
    event.title = e[4]
    event.description = e[5]
    event.response = google_api.calendar.stringToResponse(response)

    google_api.calendar.updateEvent(event)