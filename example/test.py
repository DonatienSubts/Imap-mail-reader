from ImapMailManager import MailReader

reader = MailReader("serverImap", "login", "token")
reader.Connect()
reader.getUnreadMails()

for message in reader.messages:
    print(message.subject)
    print(message.body)
    for file in message.attachments:
        with open("/Storage path/" + file.name, "wb") as binary_file:
            binary_file.write(file.content)