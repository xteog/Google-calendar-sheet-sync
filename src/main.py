import utils
import config
from datetime import datetime, timedelta
import google_api.calendar
import google_api.sheet
from database import Database


def addEvent(database: Database, user: str, start: datetime, end: datetime) -> None:
    event = database.getEvent(user=user, date=start)

    if event == None:
        event = google_api.calendar.createEvent(
            title="Nuoto",
            description=config.defaultEquipment,
            start=start,
            end=end,
            attendee=user,
        )

        database.addTraining(event)


def updateResponse(database: Database, user: str, date: datetime) -> None:
    dbEvent = database.getEvent(user=user, date=date)
    calendarEvent = google_api.calendar.getEvent(dbEvent.id)

    if not dbEvent == calendarEvent:
        database.updateEvent(calendarEvent)
        google_api.sheet.updateAttendance(
            database.getUsername(user), calendarEvent.start, calendarEvent.response
        )


def updateTrainingType(database: Database, user: str, date: datetime) -> None:
    type = google_api.sheet.getTrainingType(date=date, user=database.getUsername(user))

    if not type == database.getTrainingType(date=date, user=user):
        database.updateTrainingType(date=date, user=user, type=type)


def updateEquipment(database: Database, date: datetime) -> None:
    equipment = google_api.sheet.getEquipment(date)
    database.updateEquipment(date=date, value=equipment)


def updateCalendar(database: Database, start: datetime, end: datetime) -> None:
    trainings = database.getTrainingsDates(start, end)

    for t in trainings:

        google_api.sheet.addTraining(t[0])

        for user in database.getUsers():
            addEvent(datatbase=database, date=t[0], user=user)

            updateResponse(database=database, date=t[0], user=user)

            updateTrainingType(database=database, date=t[0], user=user)

        updateEquipment(database=database, date=t[0])


if __name__ == "__main__":
    db = Database()
    db.connect()

    try:

        run = True
        while run:
            updateCalendar(db, datetime.now(), datetime.now() + timedelta(days=7))

    except Exception as e:
        print(e)

    db.close()
