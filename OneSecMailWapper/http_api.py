from typing import List
from functools import lru_cache
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


@lru_cache(maxsize=None)
def get_domians(*args, **kwargs) -> List[str]:
    """Get list of active domains(cached)

    :param args: additional options for `requests.get`
    :param kwargs: additional options for `requests.get`

    :rtype: List[str]
    """

    response = requests.get(ENDPOINT, params={
        "action": "getDomainList"
    }, *args, **kwargs)

    return response.json()


def get_messages(login: str, domian: str, *args, **kwargs) -> dict:
    """Get list of messages on mailbox

    :param login: mailbox login
    :type login: str
    :param domian: mailbox domian
    :type domian: str
    :param args: additional options for `requests.get`
    :param kwargs: additional options for `requests.get`

    :rtype: dict
    """

    response = requests.get(ENDPOINT, params={
        "action": "getMessages",
        "login": login,
        "domain": domian,
    }, *args, **kwargs)

    return response.json()


@lru_cache(maxsize=None)
def get_message(login: str, domian: str, id: int, *args, **kwargs) -> dict:
    """Get list of messages on mailbox(cached)

    :param login: mailbox login
    :type login: str
    :param domian: mailbox domian
    :type domian: str
    :param id: message id
    :type id: id
    :param args: additional options for `requests.get`
    :param kwargs: additional options for `requests.get`

    :rtype: dict

    :exception MessageNotFound:
    """

    response = requests.get(ENDPOINT, params={
        "action": "readMessage",
        "login": login,
        "domain": domian,
        "id": id
    }, *args, **kwargs)

    if response.text == "Message not found":
        raise MessageNotFound(login=login, domian=domian, id=id)

    return response.json()


def get_attachment(login: str, domian: str, id: int, file: str, *args, **kwargs) -> bytes:
    """Get list of messages on mailbox

    :param login: mailbox login
    :type login: str
    :param domian: mailbox domian
    :type domian: str
    :param id: message id
    :type id: id
    :param file: file name
    :type file: str
    :param args: additional options for `requests.get`
    :param kwargs: additional options for `requests.get`

    :rtype: byte
    """

    response = requests.get(ENDPOINT, params={
        "action": "download",
        "login": login,
        "domain": domian,
        "id": id,
        "file": file
    }, *args, **kwargs)

    return response.content
