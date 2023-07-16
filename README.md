
# OneSecMailWapper  
OneSecMailWapper - sync wapper over https://www.1secmail.com API temporary mail service
# Install
```bash
python setup.py install
```
# Examples  
```py  
from OneSecMailWapper import get_domians, get_mailbox, get_random_mailbox, MailBox, Mail, ShortMail, Attachment  
```  
## MailBox  
### Get domians  
```python  
domians: List[str] = get_domians()  
```  
### Get specific mailbox  
```python  
mailbox: MailBox = get_mailbox("0ad1ekwui8@qiott.com")  
```  
or  
```python  
mailbox: MailBox = get_mailbox("0ad1ekwui8", "qiott.com")  
```  
### Get random mailbox  
```python  
mailbox: MailBox = get_random_mailbox()  
```  
  
## Mails  
Mails are of 2 types:  
- short  
- full  
  
Initially, the API returns short mails, in order to receive the mails in full, you need to make an additional request to the API.  
  
Short mails fields([ShortMail](https://github.com/MrNom4ik/OneSecMailWapper/blob/master/OneSecMailWapper/mailbox.py#L107)):  
```python  
id: int  
from_adress: str  
subject: str  
date: datetime  
```  
Full mails fields([Mail](https://github.com/MrNom4ik/OneSecMailWapper/blob/master/OneSecMailWapper/mailbox.py#L90)):  
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
You can get all mails (in short form) with [MailBox.get_mails()](https://github.com/MrNom4ik/OneSecMailWapper/blob/master/OneSecMailWapper/mailbox.py#L40):  
```python  
short_mails: List[ShortMail] = mailbox.get_mails()  
```  
  
To receive the mail in full, you can use [ShortMail.get_full()](https://github.com/MrNom4ik/OneSecMailWapper/blob/master/OneSecMailWapper/mailbox.py#L115):  
```python  
short_mail: ShortMail = mailbox.get_mails()[0]  
mail: Mail = short_mail.get_full()  
```  
  
To get all mails at once in the full version, you can use [MailBox.get_mails_full()](https://github.com/MrNom4ik/OneSecMailWapper/blob/master/OneSecMailWapper/mailbox.py#L51):  
```python  
mails: List[Mail] = mailbox.get_mails_full()  
```  
### Wait mail  
If you need to receive an mail that is due soon, you can use [MailBox.wait_mail()](https://github.com/MrNom4ik/OneSecMailWapper/blob/master/OneSecMailWapper/mailbox.py#L59):  
```python  
def check(mail: ShortMail) -> bool:  
return mail.from_adress == "example@example.com"  
  
shot_mail: ShortMail = mailbox.wait_mail(check)  
mail: Mail = shot_mail.get_full()  
  
print(mail.body)  
```  
This method will create a while loop and will check for new mails every 5 seconds. Each new mail will be checked through `check` and if the check is successful, the letter will be returned.  
  
## Attachments  
Attachment fields([Attachment](https://github.com/MrNom4ik/OneSecMailWapper/blob/master/OneSecMailWapper/mailbox.py#L15)):  
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