# OneSecMailWapper
OneSecMailWapper - sync wapper over https://www.1secmail.com API temporary mail service
# Install
```bash
python setup.py insta
```
# Examples
```py
from OneSecMailWapper import get_domians, get_mailbox, Mailbox, Mail, Attachment
```
## Mailbox
### Get domians
```python
domians: List[str] = get_domians()
```
### Get specific mailbox
```python
mailbox: Mailbox = get_mailbox("0ad1ekwui8", "qiott.com")
```
or
```python
mailbox: Mailbox = get_mailbox("0ad1ekwui8@qiott.com")
```
### Get random mailbox
```python
mailbox: Mailbox = get_mailbox()
```

## Mails
Initially, the API returns short mails, in order to receive the mails in full, you need to make an additional request to the API.

[Mail](https://github.com/MrNom4ik/OneSecMailWapper/blob/master/OneSecMailWapper/mailbox.py#L90) fields:
```python
id: int
from_adress: str
subject: str
date: datetime
attachments: List[Attachment]
body: str
textBody: str
htmlBody: str
```
### Get mails
You can get all mails with [Mailbox.get_mails()](https://github.com/MrNom4ik/OneSecMailWapper/blob/master/OneSecMailWapper/mailbox.py#L40):
```python
mails: List[Mail] = mailbox.get_mails()
```
### Wait mail
If you need to receive an mail that is due soon, you can use [Mailbox.wait_mail()](https://github.com/MrNom4ik/OneSecMailWapper/blob/master/OneSecMailWapper/mailbox.py#L59):
```python
def check(mail: Mail) -> bool:
	return mail.from_adress == "example@example.com"

mail: Mail = mailbox.wait_mail(check)
print(mail.body)
```
This method will create a while loop and will check for new mails every 5 seconds(default). Each new mail will be checked through `check` and if the check is successful, the letter will be returned.

## Attachments
[Attachment](https://github.com/MrNom4ik/OneSecMailWapper/blob/master/OneSecMailWapper/mailbox.py#L15) fields:
```python
filename: str
content_type: str
size: int
```

You can get the content of an attachment with [Attachment.get_content()](https://github.com/MrNom4ik/OneSecMailWapper/blob/master/OneSecMailWapper/mailbox.py#L22):
```python
for attachment in mail.attachments:
	print(attachment.get_content(), file=open(attachment.filename, 'wb'))
```