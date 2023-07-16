import time
from typing import List, Optional, Callable, Union
from random import choices
from string import ascii_lowercase
from time import sleep
from datetime import datetime

from pydantic import BaseModel, Field, TypeAdapter

from . import http_api

__all__ = ["Mailbox", "Mail", "ShortMail", "Attachment", "get_mailbox", "get_random_mailbox", "get_domians"]


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

    def get_mails(self) -> List["ShortMail"]:
        """Get all mails (in short form)

        :rtype: List[ShortMail]
        """

        mails_raw = http_api.get_messages(self.login, self.domian)
        for mail_raw in mails_raw:
            mail_raw['mailbox'] = self
        return ShortMailList.validate_python(mails_raw)

    def get_mails_full(self) -> List["Mail"]:
        """Get all mails (in full form)

        :rtype: List[Mail]
        """

        mails = []
        for mail in self.get_mails():
            mails.append(mail.get_full())
        return mails

    def wait_mail(self,
                  handler: Callable[["ShortMail"], bool],
                  delay: int = 5000
                  ) -> "ShortMail":
        """Wait a specific mail
        Creates a while loop and periodically checks for mails

        :param handler: handler for checking the mail
        :type handler: Callable[[ShortMail], bool]
        :param delay: Delay between checks new mails in milliseconds
        :type delay: int

        :return: The mail that passed the handler's check
        :rtype: ShortMail
        """

        check_failed: List[int] = []

        while True:
            mails = self.get_mails()

            not_cheched_mail = filter(lambda mail: mail.id not in check_failed, mails)

            for mail in not_cheched_mail:
                if handler(mail):
                    return mail
                check_failed.append(mail.id)

            time.sleep(delay / 1000)


class Mail(BaseModel):
    id: int
    from_adress: str = Field(alias='from')
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


class ShortMail(BaseModel):
    id: int
    from_adress: str = Field(alias='from')
    subject: str
    date: datetime

    mailbox: "Mailbox" = None

    def get_full(self) -> Mail:
        """Get the mail in full form

        :rtype: Mail
        """

        mail_raw = http_api.get_message(
            login=self.mailbox.login,
            domian=self.mailbox.domian,
            id=self.id
        )

        mail_raw['mailbox'] = self.mailbox
        return Mail.model_validate(mail_raw)


MailList = TypeAdapter(List[Mail])
ShortMailList = TypeAdapter(List[ShortMail])


def get_domians() -> List[str]:
    """Get all available domains

    :return: available domains
    :rtype: List[str]
    """

    return http_api.get_domians()


def get_random_mailbox() -> Mailbox:
    """Get a random mailbox

    :return: mailbox with random login and domain
    :rtype: Mailbox
    """

    login = ''.join(choices(ascii_lowercase, k=6))
    domian = choices(http_api.get_domians())[0]

    return Mailbox(login=login, domian=domian)


def get_mailbox(login: str, domian: str) -> Mailbox:
    """Get a specific mailbox

    :param login: mailbox login
    :type login: str
    :param domian: mailbox domian
    :type domian: str

    :return: specific mailbox
    :rtype: Mailbox
    """

    return Mailbox(login=login, domian=domian)
