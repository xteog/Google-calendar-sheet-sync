from google_api.api import sendRequest, Request
import config


class sheetRange:
    def __init__(self, cell_1: list[int, int], cell_2: list[int, int] = None) -> None:
        self.cell_1 = cell_1
        self.cell_2 = cell_2

    def __str__(self) -> str:
        range = ""

        range += chr(self.cell_1[0] + ord("a"))
        range += f"{self.cell_1[1] + 1}"

        if self.cell_2 != None:
            range += ":"
            range += chr(self.cell_2[0] + ord("a"))
            range += f"{self.cell_2[1] + 1}"


def sheetUpdate(range: sheetRange, data: list) -> None:
    json = {"values": [data]}

    url = config.googleSheetURL.format(
        sheetId=config.sheetId,
        sheetName=config.sheetName,
        range=range,
        resource="update",
    )
    sendRequest(Request.PUT, url, json)


def sheetGet(range: sheetRange) -> None:
    url = config.googleSheetURL.format(
        sheetId=config.sheetId, sheetName=config.sheetName, range=range, resource="get"
    )
    sendRequest(Request.GET, url)
