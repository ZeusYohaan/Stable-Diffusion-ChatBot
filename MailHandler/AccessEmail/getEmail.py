import email
import imaplib


class EmailClient:
    def __init__(self, email_server, username, password):
        self.email_server = email_server
        self.username = username
        self.password = password
        self.connection = None

    def connect(self):
        self.connection = imaplib.IMAP4_SSL(self.email_server)
        self.connection.login(self.username, self.password)
        self.connection.select('INBOX')

    def search_latest_unread_email_from_sender(self, sender):
        search_criteria = f'(UNSEEN FROM "{sender}")'
        status, uids = self.connection.search(None, search_criteria)
        if status == 'OK' and uids[0]:
            latest_uid = uids[0].split()[-1]
            return latest_uid
        return None

    def fetch_email_message(self, uid):
        status, raw_message = self.connection.fetch(uid, '(RFC822)')
        if status == 'OK':
            return email.message_from_bytes(raw_message[0][1])

    def extract_attachments(self, message):
        attachments = []
        for part in message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            filename = part.get_filename()
            if filename:
                attachments.append({
                    'filename': filename,
                    'data': part.get_payload(decode=True)
                })
        return attachments

    def print_email_info(self, message):
        print(f'Subject: {message["Subject"]}')
        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == 'text/plain':
                    print(f'Body: {part.get_payload()}')
                    return {part.get_payload()}
        else:
            print(f'Body: {message.get_payload()}')
        print('\n')

    def get_email_prompt(self, message):
        email_info = f'Subject: {message["Subject"]}\n'
        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == 'text/plain':
                    email_info += f'Body: {part.get_payload()}\n'
                    break
        else:
            email_info += f'Body: {message.get_payload()}\n'
        return email_info

    def logout(self):
        self.connection.close()
        self.connection.logout()



