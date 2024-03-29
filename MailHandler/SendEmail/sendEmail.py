import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


class EmailSender:
    def __init__(self, sender_email, sender_password):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = 'smtp-mail.outlook.com'
        self.smtp_port = 587

    def send_email_with_image(self, receiver_email, subject, image_bytes):
        # Create message container
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Attach image
        image = MIMEImage(image_bytes)
        image.add_header('Content-Disposition', 'attachment', filename='image.webp')
        msg.attach(image)

        # Connect to SMTP server and send email
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            print("Email sent successfully!")
        except Exception as e:
            print("Error: Unable to send email.")
            print(e)


# # Example usage
# sender_email = 'your_email@example.com'
# sender_password = 'your_password'
# receiver_email = 'recipient@example.com'
# subject = 'Test Email with Image Attachment'
# image_bytes = b'...'  # Replace '...' with your image bytes
#
# # Create EmailSender instance
# email_sender = EmailSender(sender_email, sender_password)
# # Send email with image attachment
# email_sender.send_email_with_image(receiver_email, subject, image_bytes)
