import socket
import time
from imap_tools import MailBox, A
from functools import reduce

def cumple_todo(mail, condiciones):
    return reduce(lambda x, y: x and y.cumple(mail), condiciones, True)


class Buscador_adapter:

        def __init__(self, mailbox):
                self.mailbox = mailbox

        @classmethod
        def login(cls, user, password, retries=3, delay_s=1):
            last_error = None
            for _ in range(retries):
                try:
                    mailbox = MailBox('imap.gmail.com').login(user, password, 'Inbox')
                    return cls(mailbox)
                except socket.gaierror as error:
                    last_error = error
                    time.sleep(delay_s)
            raise last_error

        def encontrar(self, asunto , condiciones):
            mails = []
            self.mailbox.folder.set('[Gmail]/All Mail')
            for mail in self.mailbox.fetch():
                subject = mail.subject or ""
                if asunto in subject:
                    if cumple_todo(mail, condiciones):
                        mails.append(mail)
            mails.sort(key=lambda m: m.date)
            return mails

                  

