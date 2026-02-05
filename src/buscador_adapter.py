import socket
from imap_tools import MailBox, A
from functools import reduce

def cumple_todo(mail, condiciones):
    return reduce(lambda x, y: x and y.cumple(mail), condiciones, True)


class Buscador_adapter:

        def __init__(self, mailbox):
                self.mailbox = mailbox
        @classmethod
        def login(self ,user, password):
            try:
                mailbox = MailBox('imap.gmail.com').login(user, password, 'Inbox')
                return self(mailbox)
            except socket.gaierror as error:
                self.login(user, password)

        def encontrar(self, asunto , condiciones):
            mails = []
            self.mailbox.folder.set('[Gmail]/All Mail')
            for mail in self.mailbox.fetch():
                if asunto in mail.subject:
                    if cumple_todo(mail, condiciones):
                        mails.append(mail)
                    
            return mails

                  


