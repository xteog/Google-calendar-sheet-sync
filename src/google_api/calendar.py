from src.google_api.api import sendRequest, Request
import config
from datetime import datetime


class Event:
    def __init__(self, data: dict = None) -> None:
        self.id = None
        self.start = None
        self.end = None
        self.title = "No title"
        self.description = ""
        self.attendees = []

        if data != None:
            self.loadEvent(data)

    def loadEvent(self, data: dict) -> None:
        self.id = data["id"]
        self.title = data["summary"]
        self.description = data["description"]
        self.start = datetime.fromisoformat(data["start"]["dateTime"])
        self.end = datetime.fromisoformat(data["end"]["dateTime"])

        for attendee in data["attendees"]:
            self.addAttendees(attendee["email"])

    def addAttendees(self, email: str) -> None:
        self.attendees.append({"email": email, "responseStatus": "needsAction"})

    def getMetaData(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "start": {"dateTime": self.start.isoformat()},
            "end": {"dateTime": self.end.isoformat()},
            "attendees": self.attendees,
        }


def createEvent(
    title: str, description: str, start: datetime, end: datetime, attendees: list
) -> Event:
    event = Event()
    event.title = title
    event.description = description
    event.start = start
    event.end = end

    for attendee in attendees:
        event.addAttendees(attendee)

    url = config.googleCalendarURL.format(calendarId=config.calendarId, eventId="")
    response = sendRequest(Request.POST, url, event.getMetaData())  # TODO catch

    return Event(response)


def updateEvent(event: Event):
    url = config.googleCalendarURL.format(
        calendarId=config.calendarId, eventId=event.id
    )

    sendRequest(Request.PUT, url, event.getMetaData())


def getEvent(id: str) -> Event:
    url = config.googleCalendarURL.format(calendarId=config.calendarId, eventId=id)

    response = sendRequest(Request.GET, url)

    return Event(response)
