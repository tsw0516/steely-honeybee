import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, receiver_email, password, subject, body, smtp_server="smtp.office365.com", port=587):
    # Set up the MIME
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Attach the email body
    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        print("Email sent successfully!")

    except Exception as e:
        print(f"Error: {e}")

# Example usage
send_email(
    sender_email="seniorproj2025@hotmail.com",
    receiver_email="tsw0516@gmail.com",
    password="ppst2025",
    subject="Test Email",
    body="This is a test email sent from Python."
)
