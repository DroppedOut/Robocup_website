""" email module """
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Sender:
    """ email sender """


    def __init__(self):
        self.enabled = True
        self.body = ""


    def status(self):
        """get status"""
        return self.enabled


    def send_letter(self, file, info):
        """send letter with attachment"""
        subject = "An email with attachment from Python"
        self.body = info
        sender_email = "robocup.tdp@gmail.com"
        receiver_email = "robocup.tdp@gmail.com"
        password = "Robocup2020Russia"

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(self.body, "plain"))

        filename = file  # In same directory as script

        # Open PDF file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            try:
                server.login(sender_email, password)
            except smtplib.SMTPAuthenticationError:
                print("SERVER LOGIN ERROR")
            try:
                server.sendmail(sender_email, receiver_email, text)
                print("message sent successful")
            except FileNotFoundError:
                print("Send error, file not found")
