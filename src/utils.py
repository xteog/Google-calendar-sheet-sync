import json
from datetime import datetime
import config


def write(path: str, data: dict) -> None:
    data = json.dumps(data, indent=2)
    with open(path, "w+") as f:
        f.write(data)


def read(path: str) -> dict:
    try:
        with open(path, "r") as f:
            file = f.read()
        return json.loads(file)
    except:
        return None


def stringToDatetime(str: str) -> datetime:
    return datetime.strptime(str, config.dateFormat)


def datetimeToString(date: datetime) -> str:
    return date.strftime(config.dateFormat)

def getEventDescription(database, date: datetime, user: str) -> str:
    equipment = database.getEquipment(date=date)
    type = database.getTrainingType(date=date, user=user)

    if date.weekday() != 0:
        description = f"- {type.type}\n- {equipment}"
    elif type.lock or type.priority != None or date - datetime.utcnow() < config.noticeTime:
        description = f"- {type.type}\n- {equipment}"
    else:
        description = f"- {equipment}"

    return description

class TrainingType:
    def __init__(
        self, type: str = "Dinamica", priority: int = None, lock: bool = False
    ) -> None:
        self.type = type
        self.priority = priority
        self.lock = lock

    def __eq__(self, other: object) -> bool:
        return self.type == other.type

