from enum import Enum
from google_api.api import sendRequest, Request
import config
from datetime import datetime


class Response(Enum):
    YES = "accepted"
    NO = "declined"
    MAYBE = "tentative"
    NONE = "needsAction"


def responseToString(value: Response) -> str:
    if value == Response.YES:
        return "Presente"
    elif value == Response.NO:
        return "Assente"
    elif value == Response.MAYBE:
        return "Forse"
    elif value == Response.NONE:
        return ""


def stringToResponse(value: str) -> Response:
    if value == Response.YES.value:
        return Response.YES
    elif value == Response.NO.value:
        return Response.NO
    elif value == Response.MAYBE.value:
        return Response.MAYBE
    elif value == Response.NONE.value:
        return Response.NONE


class Event:
    def __init__(self, data: dict = None) -> None:
        self.id = None
        self.start = None
        self.end = None
        self.title = "No title"
        self.description = ""
        self.response = Response.NONE
        self.attendee = None

        if data != None:
            self.loadEvent(data)

    def __eq__(self, other: object) -> bool:
        return (
            other != None and
            self.id == other.id
            and self.description == other.description
            and self.response == other.response
        )

    def loadEvent(self, data: dict) -> None:
        self.id = data["id"]
        self.title = data["summary"]
        self.description = data["description"]
        self.start = datetime.fromisoformat(data["start"]["dateTime"][:-1])
        self.end = datetime.fromisoformat(data["end"]["dateTime"][:-1])

        for attendee in data["attendees"]:
            self.attendee = attendee["email"]
            self.response = stringToResponse(attendee["responseStatus"])

    def getMetaData(self) -> dict:
        return {
            "summary": self.title,
            "description": self.description,
            "start": {"dateTime": self.start.astimezone().isoformat()},
            "end": {"dateTime": self.end.astimezone().isoformat()},
            "attendees": [{"email": self.attendee, "responseStatus": self.response.value}],
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
