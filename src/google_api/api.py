from enum import Enum
import requests
import utils
import logging
import config


class Request(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"


def sendRequest(request: Request, url: str, data: dict = None) -> any:
    headers = getHeaders()

    done = 0
    while done < 3:
        if request == Request.GET:
            response = requests.get(url=url, headers=headers, json=data)
        elif request == Request.POST:
            response = requests.post(url=url, headers=headers, json=data)
        elif request == Request.PUT:
            response = requests.put(url=url, headers=headers, json=data)
            
        if response.status_code == 200:
            done = 4
        else:
            done += 1

    if done != 4:
        logging.error(f"{request} {url} {data} {response.content}")
        return None

    return response.json()

def getHeaders() -> dict:
    token = refreshToken()

    return {"Authorization": f"Bearer {token}"}


def refreshToken() -> str | None:
    credentials = utils.read(config.googleCredentialsPath)

    response = requests.post(
        url=config.refreshTokenURL.format(
            refreshToken=credentials["refresh_token"],
            clientId=credentials["client_id"],
            clientSecret=credentials["client_secret"],
        )
    )

    if response.status_code == 200:
        return response.json()["access_token"]

    logging.error("Couldn't get new Google token")
    return None
