import utils
import config
from datetime import datetime, timedelta
import google_api.calendar
import google_api.sheet
from database import Database


def createEvents(database: Database, user: str, start: datetime, end: datetime) -> None:
    trainings = database.getTrainings(start, end)
    events = database.getEvents(user, start, end)

    if len(trainings) > len(events):
        for t in trainings:
            found = False
            for e in events:
                if t[0].day == e.start.day:
                    found = True
            if not found:
                event = google_api.calendar.createEvent(
                    title="Nuoto",
                    description=config.defaultEquipment,
                    start=t[0],
                    end=t[1],
                    attendee=user,
                )
                
                database.addEvent(event)
                google_api.sheet.addTraining(event)


def checkResponses(
    database: Database, user: str, start: datetime, end: datetime
) -> None:
    events = database.getEvents(user, start, end)
    for i in range(len(events)):
        event = google_api.calendar.getEvent(events[i].id)
        if event.response != events[i].response:
            database.updateEvent(event)
            google_api.sheet.updateAttendance(user, event.start, event.response)


def updateEvents(database: Database, start: datetime, end: datetime) -> None:
    for user in database.getUsers():
        createEvents(database, user, start, end)

        checkResponses(database, user, start, end)


if __name__ == "__main__":
    db = Database()
    db.connect()

    try:

        run = True
        while run:
            updateEvents(db, datetime.now(), datetime.now() + timedelta(days=7))
            run = False

    except Exception as e:
        print(e)

    db.close()
