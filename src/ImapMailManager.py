import imaplib
import email


class Message:
    def __init__(self):
        self.to = None
        self.msgFrom = None
        self.attachments = []
        self.subject = None
        self.body = None
        self.htmlBody = None
        self.date = None


class File:
    name = None
    content = None

    def __init__(self, name, content):
        self.name = name
        self.content = content


class MailReader:
    conn = None
    server = None
    login = None
    token = None
    messages = []

    def __init__(self, server, login, token):
        self.server = server
        self.login = login
        self.token = token

    def Connect(self):
        auth_string = 'user={}\1auth=Bearer {}\1\1'.format(self.login, self.token)
        self.conn = imaplib.IMAP4_SSL(self.server)
        self.conn.authenticate('XOAUTH2', lambda x: auth_string.encode("utf-8"))
        self.conn.select("inbox")

    def getUnreadMails(self):
        typ, data = self.conn.search(None, 'UNSEEN')
        for num in data[0].split():
            typ, data = self.conn.fetch(num, '(RFC822)')
            message = email.message_from_string(data[0][1].decode("utf-8"))
            typ, data = self.conn.store(num, '-FLAGS', 'SEEN')
            self.parseMessage(message)

    def parseMessage(self, message):
        new_message = Message()
        idx = 0
        for part in message.walk():
            if idx == 0:
                new_message.to = part["To"]
                new_message.msgFrom = part["From"]
                new_message.date = part["Date"]
                new_message.subject = part["Subject"]
            if idx > 0:
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    new_message.body = part.get_payload(decode=1)
                elif content_type == "text/html":
                    new_message.htmlBody = part.get_payload(decode=1)
                elif content_type == "multipart/mixed" or content_type == "multipart/alternative":
                    pass
                else:
                    new_message.attachments.append(File(part.get_filename(), part.get_payload(decode=1)))
            idx += 1
        self.messages.append(new_message)