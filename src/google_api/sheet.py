from google_api.api import sendRequest, Request
import config
from datetime import datetime
from utils import stringToDatetime, datetimeToString
from utils import TrainingType
from google_api import calendar
import logging


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

    try:
        return response["values"]
    except Exception as e:
        logging.error(f"No data fetched: {e}")
        return [[]]


def addTraining(date: datetime) -> None:
    cols = getDates()

    if not date in cols:
        if len(cols) > 0 and cols[-1].weekday() == 0:
            index = len(cols) + 2
        else:
            index = len(cols) + 1

        r = sheetRange((0, index))
        sheetUpdate(range=r, data=[datetimeToString(date)])

        r = sheetRange((len(getUsers()) + 1, index))
        sheetUpdate(range=r, data=[config.defaultEquipment])

        if date.weekday() == 0:
            for i in range(1, len(getUsers()) + 1):
                r = sheetRange((i, index + 1))
                value = "Dinamica"
                sheetUpdate(range=r, data=[value])


def getTrainingType(date: datetime, user: str) -> TrainingType:
    if date.weekday() != 0:
        return TrainingType(type="Dinamica")

    row = getUsers().index(user) + 1
    col = getDates().index(date) + 1

    range = sheetRange((row, col + 1))

    value = sheetGet(range)

    return TrainingType(type=value[0][0])


def getEquipment(date: datetime) -> str:
    row = len(getUsers()) + 1
    col = getDates().index(date) + 1

    range = sheetRange((row, col))

    value = sheetGet(range)

    return value[0][0]


def updateAttendance(user: str, date: datetime, response: calendar.Response) -> None:
    row = getUsers().index(user) + 1
    col = getDates().index(date) + 1

    range = sheetRange((row, col))
    sheetUpdate(range=range, data=[calendar.responseToString(response)])


def getDates() -> list[datetime]:
    sheet = sheetGet(sheetRange((0, 1), (0, 1000)))
    result = []
    for x in sheet[0]:
        if len(x) > 0:
            result.append(stringToDatetime(x))
        else:
            result.append(datetime(2000, 1, 1))
    return result


def getUsers() -> list[str]:
    sheet = sheetGet(sheetRange((1, 0), (100, 0)))
    return [x[0] for x in sheet][:-1]
