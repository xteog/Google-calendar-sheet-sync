import mysql.connector
from datetime import datetime
from google_api.calendar import Event
from utils import TrainingType


class Database:
    def __init__(self) -> None:
        self.database = None
        self.cursor = None

    def connect(self) -> None:
        try:
            self.database = mysql.connector.connect(
                user="root",
                password="7ClsWHSf6?a52v6#[?4T",
                host="localhost",
                database="ApneaSchedule",
            )
            self.cursor = self.database.cursor()
            print("Connessione al database riuscita!")
        except mysql.connector.Error as err:
            print(f"Errore durante la connessione al database: {err}")

    def close(self) -> None:
        self.database.close()
        print("Connessione chiusa.")

    def getTrainingsDates(
        self, start: datetime, end: datetime
    ) -> list[tuple[datetime, datetime]]:
        query = """
            SELECT start, end 
            FROM Schedule
            WHERE start > %s AND start < %s
            """
        values = [start, end]
        self.cursor.execute(query, values)

        return self.cursor.fetchall()

    def getEvent(self, user: str, date: datetime) -> Event | None:
        query = """
            SELECT id, Events.start, end, attendee, title, description, response
            FROM Events
            JOIN Schedule ON Events.start = Schedule.start 
            WHERE Events.start = %s AND attendee = %s
            """
        values = [date, user]
        self.cursor.execute(query, values)

        if (self.cursor.fetchall()) > 0:
            e = self.cursor.fetchall()[0]
            event = Event()
            event.id = e[0]
            event.start = e[1]
            event.end = e[2]
            event.attendee = e[3]
            event.title = e[4]
            event.description = e[5]
            event.response = e[6]

            return event

        return None

    def updateEvent(self, event: Event) -> None:
        query = """
            UPDATE Events
            SET description = %s, response = %s
            WHERE id = %s
            """
        values = (event.description, event.response, event.id)

        self.cursor.execute(query, values)
        self.database.commit()

    def addTraining(self, event: Event) -> None:
        query = "INSERT INTO Events (id, start, attendee, title, description, response) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (
            event.id,
            event.start,
            event.attendee,
            event.title,
            event.description,
            event.response,
        )

        self.cursor.execute(query, values)

        query = "INSERT INTO TrainingType (date, user) VALUES (%s, %s)"
        values = (event.start, event.attendee)

        self.cursor.execute(query, values)

        self.database.commit()

    def getTrainingType(self, date: datetime, user: str) -> TrainingType:
        query = """
            SELECT type, priority, lock
            FROM TrainingType
            WHERE date = %s AND user = %s
            """
        values = [date, user]
        self.cursor.execute(query, values)

        result = self.cursor.fetchall()[0]

        return TrainingType(type=result[0], priority=result[1], lock=result[2])

    def updateTrainingType(self, date: datetime, user: str, type: TrainingType) -> None:
        query = """
            UPDATE TrainingType
            SET type = %s, priority = %s, lock = %s
            WHERE date = %s AND user = %s
            """
        values = (type.type, type.priority, type.lock, date, user)

        self.cursor.execute(query, values)
        self.database.commit()

    def updateEquipment(self, date: datetime, value: str) -> None:
        query = """
            UPDATE Schedule
            SET equipment = %s
            WHERE start = %s
            """
        values = (value, date)

        self.cursor.execute(query, values)
        self.database.commit()

    def getUsers(self) -> list:
        self.cursor.execute(
            """
            SELECT email
            FROM Users
            """
        )

        data = []
        for email in self.cursor.fetchall():
            data.append(email[0])

        return data

    def getUsername(self, email: str):
        query = """
            SELECT name
            FROM Users
            WHERE email = %s
            """
        values = [email]
        self.cursor.execute(query, values)

        return self.cursor.fetchall()
