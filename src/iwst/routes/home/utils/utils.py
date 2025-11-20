import logging
from flask import current_app
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
import smtplib

def send_email(recipient_list, subject, body): 
        config = current_app.config.get("IWST") 
        email_config = config.emailsettings

        if not email_config: 
            logger.info("Email sending is empty.")
            return False

        if not email_config.active:
            logger.info("Email sending is disabled.") 
            return False

        sender_email = email_config.from_address
        sender_password = email_config.password
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = ", ".join(recipient_list)  # Comma-separated string for header
        msg['Subject'] = subject
        msg['Date'] = formatdate(localtime=True)
        msg.attach(MIMEText(body, 'plain'))
        try:
            with smtplib.SMTP_SSL(email_config.domain, email_config.port) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_list, msg.as_string())
            return True
        except smtplib.SMTPConnectError as e:
            logger.error(f"Failed to connect to the SMTP server: {e}")
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP authentication failed: {e}")
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error occurred during email sending: {e}")
        
        return False