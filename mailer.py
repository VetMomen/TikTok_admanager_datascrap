import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import logging

load_dotenv()

def send_report(csv_path=None, subject="TikTok Ads Report", body=None):
    """
    Sends an email with an optional CSV file attachment.
    """
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    email_from = os.getenv("EMAIL_FROM")
    email_to = os.getenv("EMAIL_TO")

    if not all([smtp_host, smtp_user, smtp_pass, email_from, email_to]):
        logging.error("SMTP configuration is missing in .env file.")
        return False

    # Create the message
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = subject

    if body is None:
        body = "Please find the attached TikTok Ads report." if csv_path else "The TikTok Ads scraper run finished."
    
    msg.attach(MIMEText(body, 'plain'))

    # Attach the CSV file if provided
    if csv_path and os.path.exists(csv_path):
        try:
            with open(csv_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {os.path.basename(csv_path)}",
                )
                msg.attach(part)
        except Exception as e:
            logging.error(f"Failed to attach file {csv_path}: {e}")
            return False


    # Send the email
    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        text = msg.as_string()
        server.sendmail(email_from, email_to, text)
        server.quit()
        logging.info(f"Email sent successfully to {email_to}")
        return True
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        return False

if __name__ == "__main__":
    # Test with a dummy file if it exists
    logging.basicConfig(level=logging.INFO)
    test_file = "test_report.csv"
    if os.path.exists(test_file):
        send_report(test_file, "TikTok Ads Report - Test")
    else:
        print(f"File {test_file} not found for testing.")
