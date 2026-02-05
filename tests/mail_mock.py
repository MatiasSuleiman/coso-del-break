class Mail_Mock:

        @classmethod
        def con(self, sender, receiver, text, subject, date):
            return self(sender, receiver, text, subject, date)

        def __init__(self, sender, receiver, text, subject, date):
            self.from_ = sender
            self.to = receiver
            self.text = text
            self.subject = subject
            self.date = date

