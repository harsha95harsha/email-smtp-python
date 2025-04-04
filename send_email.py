import smtplib
import os
import logging
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Fetch email credentials
EMAIL_ADDRESS = "harsha.vardhan16795@gmail.com"
EMAIL_PASSWORD = "bhbkzleinyaxojsn"

# SMTP Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # Ensure it's an integer
USE_SSL = SMTP_PORT == 465  # Determine if SSL should be used

def send_email(to_email, subject):
    try:
        logging.info("Starting email sending process...")

        # Debug SMTP config
        logging.debug(f"SMTP Server: {SMTP_SERVER}")
        logging.debug(f"SMTP Port: {SMTP_PORT}")
        logging.debug(f"Sender Email: {EMAIL_ADDRESS}")

        # Create HTML email
        html_content = f"""
        <html>
        <head><title>Welcome</title></head>
        <body><h2>Hello, Welcome!</h2><p>This is a test email.</p></body>
        </html>
        """
        
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(html_content, "html"))

        logging.info("Email message created successfully.")

        # Connect to SMTP server
        logging.info(f"Connecting to SMTP server: {SMTP_SERVER}:{SMTP_PORT}...")

        if USE_SSL:
            server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)  # Fix for port 465
        else:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()  # Required for port 587

        logging.info("SMTP connection established.")

        # Login to SMTP server
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        logging.info("SMTP authentication successful.")

        # Send email
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        logging.info("Email sent successfully!")

        # Close connection
        server.quit()
        logging.info("SMTP connection closed.")

    except smtplib.SMTPAuthenticationError:
        logging.error("SMTP Authentication Error: Check your email/password or enable App Passwords.")
    except smtplib.SMTPConnectError:
        logging.error("SMTP Connection Error: Unable to connect to the server.")
    except smtplib.SMTPServerDisconnected:
        logging.error("SMTP Server Disconnected: The server closed the connection unexpectedly.")
    except Exception as e:
        logging.error(f"Unexpected Error: {e}")

# Lambda Function
def lambda_handler(event, context):
    logging.info("Lambda function invoked.")
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Lambda executed successfully!"})
    }

# Example usage
if __name__ == "__main__":
    recipient_email = "sriharshavardhan1995.tk@gmail.com"
    email_subject = "Welcome Email 4!"
    send_email(recipient_email, email_subject)
