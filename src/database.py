import mysql.connector
from datetime import datetime
from google_api.calendar import Event
from trainings import TrainingType


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

    def insertUser(self, name: str, email: str):
        query = "INSERT INTO users (email, name) VALUES (%s, %s)"
        values = (email, name)
        self.cursor.execute(query, values)

        query = """
            SELECT start 
            FROM schedule
            WHERE start > %s;
            """
        values = [datetime.now()]
        self.cursor.execute(query, values)

        dates = self.cursor.fetchall()
        for i in range(len(dates)):
            query = (
                "INSERT INTO attendance (date, user, attendance) VALUES (%s, %s, %s)"
            )
            values = (dates[i][0], email, None)
            self.cursor.execute(query, values)

        self.database.commit()

    def getTrainingsDates(
        self, start: datetime, end: datetime
    ) -> list[tuple[datetime, datetime]]:
        query = """
            SELECT start, end 
            FROM schedule
            WHERE start > %s AND start < %s
            """
        values = [start, end]
        self.cursor.execute(query, values)

        return self.cursor.fetchall()

    def getEvent(self, user: str, date: datetime) -> Event | None:
        query = """
            SELECT id, Events.start, end, attendee, title, description, response
            FROM Events
            JOIN schedule ON Events.start = schedule.start 
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
            UPDATE schedule
            SET equipment = %s
            WHERE start = %s
            """
        values = (value, date)

        self.cursor.execute(query, values)
        self.database.commit()

    def insertDateTime(self, start: datetime, end: datetime):
        query = "INSERT INTO schedule (start, end) VALUES (%s, %s)"
        values = (start, end)
        self.cursor.execute(query, values)

        query = """
            SELECT start, email 
            FROM schedule, users
            WHERE start = %s
            """
        values = [start]
        self.cursor.execute(query, values)
        rows = self.cursor.fetchall()

        for row in rows:
            query = "INSERT INTO attendance (date, name) VALUES (%s, %s)"
            values = row
            self.cursor.execute(query, values)

        self.database.commit()

    def getUsers(self) -> list:
        self.cursor.execute(
            """
            SELECT email
            FROM users
            """
        )

        data = []
        for email in self.cursor.fetchall():
            data.append(email[0])

        return data

    def getUsername(self, email: str):
        query = """
            SELECT name
            FROM users
            WHERE email = %s
            """
        values = [email]
        self.cursor.execute(query, values)

        return self.cursor.fetchall()
