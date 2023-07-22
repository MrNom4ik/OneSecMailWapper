import time
from typing import List, Optional, Callable, Union
from random import choices
from string import ascii_lowercase
from time import sleep
from datetime import datetime

from pydantic import BaseModel, Field, TypeAdapter

from . import http_api

__all__ = ["Mailbox", "Mail", "Attachment", "get_mailbox", "get_domians"]


class Attachment(BaseModel):
    filename: str
    content_type: str = Field(alias='contentType')
    size: int

    mail: "Mail" = None

    def get_content(self) -> bytes:
        """Get attachment content

        :rtype: bytes
        """

        return http_api.get_attachment(
            login=self.mail.mailbox.login,
            domian=self.mail.mailbox.domian,
            id=self.mail.id,
            file=self.filename
        )


class Mailbox(BaseModel):
    login: str
    domian: str

    _checked_mails: List[int] = []

    def get_mails(self) -> List["Mail"]:
        """Get all mails

        :rtype: List[Mail]
        """

        full_mails = []
        short_mails = http_api.get_messages(self.login, self.domian)
        for short_mail in short_mails:
            full_mail = http_api.get_message(self.login, self.domian, short_mail["id"])
            full_mail['mailbox'] = self
            full_mails.append(full_mail)
        return MailList.validate_python(full_mails)

    def wait_mail(self,
                  handler: Callable[["Mail"], bool],
                  delay: int = 5000
                  ) -> "Mail":
        """Wait a specific mail
        Creates a while loop and periodically checks for mails

        :param handler: handler for checking the mail
        :type handler: Callable[[Mail], bool]
        :param delay: Delay between checks new mails in milliseconds
        :type delay: int

        :return: The mail that passed the handler's check
        :rtype: Mail
        """

        while True:
            mails = self.get_mails()

            not_cheched_mails = filter(lambda mail: mail.id not in self._checked_mails, mails)

            for mail in not_cheched_mails:
                self._checked_mails.append(mail.id)
                if handler(mail):
                    return mail

            time.sleep(delay / 1000)


class Mail(BaseModel):
    id: int
    from_address: str = Field(alias='from')
    subject: str
    date: datetime
    attachments: List[Attachment]
    body: str
    textBody: str
    htmlBody: str

    mailbox: "Mailbox" = None

    def model_post_init(self, _):
        for attachment in self.attachments:
            attachment.mail = self


MailList = TypeAdapter(List[Mail])


def get_domians() -> List[str]:
    """Get all available domains

    :rtype: List[str]
    """

    return http_api.get_domians()


def get_mailbox(login: Optional[str] = None, domian: Optional[str] = None) -> Mailbox:
    """Get a specific mailbox

    Example:
    ..code: python
        get_mailbox("example@example.com")     # specific
        get_mailbox("example", "example.com")  # specific
        get_mailbox()                          # random

    :param login: mailbox login
    :type login: str
    :param domian: mailbox domian
    :type domian: str

    :rtype: Mailbox
    """

    if login or domian:
        _login = login if domian else login.split("@")[0]
        _domian = domian or login.split("@")[1]
    else:
        _login = ''.join(choices(ascii_lowercase, k=6))
        _domian = choices(get_domians())[0]

    return Mailbox(login=_login, domian=_domian)
