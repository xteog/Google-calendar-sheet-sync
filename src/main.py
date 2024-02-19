import config
from datetime import datetime, timedelta
import google_api.calendar
import google_api.sheet
from database.queris import Database
import time


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
        event = database.getEvent(user=user, date=date)

        equipment = database.getEquipment(date=date)
        event.description = f"- {type.type}\n- {equipment}"

        google_api.calendar.updateEvent(event)


def updateEquipment(database: Database, date: datetime) -> None:
    equipment = google_api.sheet.getEquipment(date)
    database.updateEquipment(date=date, value=equipment)

    for user in database.getUsers():
        event = database.getEvent(user=user, date=date)

        equipment = database.getEquipment(date=date)
        type = database.getTrainingType(date=date, user=user)
        event.description = f"- {type.type}\n- {equipment}"

        google_api.calendar.updateEvent(event)


def updateCalendar(database: Database, range=tuple[datetime,datetime]) -> None:
    trainings = database.getTrainingsDates(range=range)

    for t in trainings:

        google_api.sheet.addTraining(t[0])

        for user in database.getUsers():
            addEvent(database=database, user=user, start=t[0], end=t[1])

            updateResponse(database=database, date=t[0], user=user)

            updateTrainingType(database=database, date=t[0], user=user)

        updateEquipment(database=database, date=t[0])


if __name__ == "__main__":

    db = Database()
    db.connect()

    run = True
    while run:
        updateCalendar(db, (datetime.now(), datetime.now() + timedelta(days=7)))
        time.sleep(60)
    db.close()

    """
    db = Database()
    db.connect()

    try:
        date = datetime(2024, 2, 17)

        while date.month < 8:
            if date.weekday() == 0:
                insertDateTime(db, date + timedelta(hours=19, minutes=15), date + timedelta(hours=21, minutes=30))
                date += timedelta(days=3)
            elif date.weekday() == 3:
                insertDateTime(db, date + timedelta(hours=20, minutes=00), date + timedelta(hours=21, minutes=30))
                date += timedelta(days=2)
            elif date.weekday() == 5:
                insertDateTime(db, date + timedelta(hours=16, minutes=15), date + timedelta(hours=18))
                date += timedelta(days=2)

    except Exception as e:
        print(e)

    db.close()
    """
    """
    db = Database()
    db.connect()

    try:
        insertUser(db, "Matteo", "gallo.matteo@hotmail.com")
        insertUser(db, "Miriam", "gallomiriam18@gmail.com")

    except Exception as e:
        print(e)

    db.close()
    """
