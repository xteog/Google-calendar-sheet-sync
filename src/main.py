import config
from datetime import datetime, timedelta
import google_api.calendar
import google_api.sheet
from database.queris import Database
import time
import utils
import logging


def addEvent(database: Database, user: str, start: datetime, end: datetime) -> None:
    event = database.getEvent(user=user, date=start)

    if event == None:
        event = google_api.calendar.createEvent(
            title="Allenamento Apnea",
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

    if not type == database.getTrainingType(date=date, user=user) and date - datetime.now() < config.noticeTime:
        type.lock = True
        database.updateTrainingType(date=date, user=user, type=type)

        event = database.getEvent(user=user, date=date)

        event.description = utils.getEventDescription(database=database, date=date, user=user)

        google_api.calendar.updateEvent(event)

    #TODO aggiorna database -> sheet


def updateEquipment(database: Database, date: datetime) -> None:
    equipment = google_api.sheet.getEquipment(date)
    database.updateEquipment(date=date, value=equipment)

    for user in database.getUsers():
        event = database.getEvent(user=user, date=date)

        description = utils.getEventDescription(database=database, date=date, user=user)

        if event.description != description:
            event.description = description
            google_api.calendar.updateEvent(event)


def updateCalendar(database: Database, range=tuple[datetime,datetime]) -> None:
    trainings = database.getTrainingsDates(range=range)

    for t in trainings:

        google_api.sheet.addTraining(t[0])

        for user in database.getUsers():
            addEvent(database=database, user=user, start=t[0], end=t[1])

            updateResponse(database=database, date=t[0], user=user)

            updateTrainingType(database=database, date=t[0], user=user)
            time.sleep(1)

        updateEquipment(database=database, date=t[0])


if __name__ == "__main__":
    logging.basicConfig(
        filename=config.loggerPath,
        format="%(asctime)s [%(levelname)s]:%(name)s:%(message)s",
        level=logging.INFO,
    )

    db = Database()
    db.connect()

    run = True
    while run:
        try:

            updateCalendar(db, (datetime.now() - timedelta(days=5), datetime.now() + timedelta(days=14)))
        
        except KeyboardInterrupt:
            run = False
            print("KeyboardInterrupt detected")
        except Exception as e:
            run = False
            logging.error("Execution terminated")

    db.close()