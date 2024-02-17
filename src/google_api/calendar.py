from enum import Enum
from src.google_api.api import sendRequest, Request
import config
from datetime import datetime


class Response(Enum):
    YES = "accepted"
    NO = "declined"
    MAYBE = "tentative"
    NONE = "needsAction"


class Event:
    def __init__(self, data: dict = None) -> None:
        self.id = None
        self.start = None
        self.end = None
        self.title = "No title"
        self.description = ""
        self.response = "needsAction"
        self.attendee = None

        if data != None:
            self.loadEvent(data)

    def loadEvent(self, data: dict) -> None:
        self.id = data["id"]
        self.title = data["summary"]
        self.description = data["description"]
        self.start = datetime.fromisoformat(data["start"]["dateTime"])
        self.end = datetime.fromisoformat(data["end"]["dateTime"])

        for attendee in data["attendees"]:
            self.attendee = attendee["email"]
            self.response = attendee["responseStatus"]

    def getMetaData(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "start": {"dateTime": self.start.isoformat()},
            "end": {"dateTime": self.end.isoformat()},
            "attendees": [self.attendee],
        }


def createEvent(
    title: str, description: str, start: datetime, end: datetime, attendee: str
) -> Event:
    event = Event()
    event.title = title
    event.description = description
    event.start = start
    event.end = end

    event.attendee = attendee

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
