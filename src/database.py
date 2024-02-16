import mysql.connector
import datetime



def insertUser(name:str, email:str):
    query = "INSERT INTO users (email, name) VALUES (%s, %s)"
    values = (email, name)
    db.execute(query, values)

    query = """
        SELECT start 
        FROM schedule
        WHERE start > %s;
        """
    values = [datetime.datetime.now()]
    db.execute(query, values)

    dates = db.fetchall()
    for i in range(len(dates)):
        query = "INSERT INTO attendance (date, user, attendance) VALUES (%s, %s, %s)"
        values = (dates[i][0], email, None)
        db.execute(query, values)

    cnx.commit()

def getUserSchedule()

def insertDateTime(start: datetime, end: datetime):
    query = "INSERT INTO schedule (start, end) VALUES (%s, %s)"
    values = (start, end)
    db.execute(query, values)

    query = """
        SELECT start, email 
        FROM schedule, users
        WHERE start = %s
        """
    values = [start]
    db.execute(query, values)
    rows = db.fetchall()

    for row in rows:
        query = "INSERT INTO attendance (date, name) VALUES (%s, %s)"
        values = row
        db.execute(query, values)

    cnx.commit()

def getUsers() -> list:
    db.execute(
        """
        SELECT email
        FROM users
        """
    )

    data = []
    for email in db.fetchall():
        data.append(email[0])

    return data

def getUsername(email: str):
    query = """
        SELECT name
        FROM users
        WHERE email = %s
        """
    values = [email]
    db.execute(query, values)

    return db.fetchall()

cnx = mysql.connector.connect(user="root", password="7ClsWHSf6?a52v6#[?4T", host="localhost", database="ApneaSchedule")
print("Connessione al database riuscita!")

db = cnx.cursor()

if __name__ == "__main__":
    try:
        cnx = mysql.connector.connect(user="root", password="7ClsWHSf6?a52v6#[?4T", host="localhost", database="ApneaSchedule")
        print("Connessione al database riuscita!")

        db = cnx.cursor()


        cnx.close()
        print("Connessione chiusa.")

    except mysql.connector.Error as err:
        print(f"Errore durante la connessione al database: {err}")


