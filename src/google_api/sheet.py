from google_api.api import sendRequest, Request
import config
from datetime import datetime
from utils import stringToDatetime, datetimeToString
from utils import TrainingType
from google_api import calendar


class sheetRange:
    def __init__(self, cell_1: list[int, int], cell_2: list[int, int] = None) -> None:
        self.cell_1 = cell_1
        self.cell_2 = cell_2

    def __str__(self) -> str:
        range = ""

        range += f"R{self.cell_1[0] + 1}"
        range += f"C{self.cell_1[1] + 1}"

        if self.cell_2 != None:
            range += ":"
            range += f"R{self.cell_2[0] + 1}"
            range += f"C{self.cell_2[1] + 1}"

        return range


def sheetUpdate(range: sheetRange, data: list) -> None:
    json = {"values": [data]}

    url = config.googleSheetURL.format(
        sheetId=config.sheetId,
        sheetName=config.sheetName,
        range=range,
        options="valueInputOption=RAW",
    )

    sendRequest(Request.PUT, url, json)


def sheetGet(range: sheetRange) -> None:
    url = config.googleSheetURL.format(
        sheetId=config.sheetId, sheetName=config.sheetName, range=range, options=""
    )

    response = sendRequest(Request.GET, url)
    return response["values"]


def addTraining(date: datetime) -> None:
    cols = getDates()
    if cols[-1].weekday == 0:
        index = len(cols) + 1
    else:
        index = len(cols)

    range = sheetRange((0, index))
    sheetUpdate(range=range, data=[datetimeToString(date)])

    range = sheetRange((len(getUsers()) + 1, index))
    sheetUpdate(range=range, data=[config.defaultEquipment])

    if date.weekday == 0:
        range = sheetRange((1, index + 1), (len(getUsers()), index + 1))
        values = ["Dinamica"] * len(getUsers())
        sheetUpdate(range=range, data=values)


def getTrainingType(date: datetime, user: str) -> TrainingType:
    row = getUsers().index(user)
    col = getDates().index(date)

    range = sheetRange((row, col))

    value = sheetGet(range)

    return value[0][0]


def getEquipment(date: datetime) -> str:
    row = len(getUsers()) + 1
    col = getDates().index(date)

    range = sheetRange((row, col))

    value = sheetGet(range)

    return value[0][0]


def updateAttendance(user: str, date: datetime, response: calendar.Response) -> None:
    row = getUsers().index(user)
    col = getDates().index(date)

    range = sheetRange((row, col))
    sheetUpdate(range=range, data=calendar.responseToString(response))


def getDates() -> list[datetime]:
    sheet = sheetGet(sheetRange((0, 1), (0, 1000)))
    return [stringToDatetime(x) for x in sheet]


def getUsers() -> list[str]:
    sheet = sheetGet(sheetRange((1, 0), (100, 0)))
    return [x[0] for x in sheet][:-1]
