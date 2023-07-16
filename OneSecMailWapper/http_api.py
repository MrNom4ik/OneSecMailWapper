from typing import List
from dataclasses import dataclass

import requests

ENDPOINT = "https://www.1secmail.com/api/v1/"
# See https://www.1secmail.com/api/


@dataclass
class MessageNotFound(Exception):
    login: str
    domian: str
    id: int

    def __str__(self):
        return f"Message with id {self.id} not found on {self.login}@{self.domian}"


def get_domians() -> List[str]:
    response = requests.get(ENDPOINT, params={
        "action": "getDomainList"
    })

    return response.json()


def get_messages(login: str, domian: str) -> dict:
    response = requests.get(ENDPOINT, params={
        "action": "getMessages",
        "login": login,
        "domain": domian,
    })

    return response.json()


def get_message(login: str, domian: str, id: int) -> dict:
    response = requests.get(ENDPOINT, params={
        "action": "readMessage",
        "login": login,
        "domain": domian,
        "id": id
    })

    if response.text == "Message not found":
        raise MessageNotFound(login=login, domian=domian, id=id)

    return response.json()


def get_attachment(login: str, domian: str, id: int, file: str) -> bytes:
    response = requests.get(ENDPOINT, params={
        "action": "download",
        "login": login,
        "domain": domian,
        "id": id,
        "file": file
    })

    return response.content
