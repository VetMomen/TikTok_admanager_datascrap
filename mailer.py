from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from dotenv import load_dotenv
import os
from email.mime.base import MIMEBase
from datetime import datetime
from email import encoders

from logger import setup_logger

logger = setup_logger(__name__)

load_dotenv()


def tiktok_sd_mail(file_dir: str, run_time: datetime):
    try:
        logger.info(
            f"Preparing to send TikTok report for {run_time.strftime('%d-%m-%y')}"
        )
        # Importing environmental variables
        host = os.getenv("smtp_host")
        port = int(os.getenv("smtp_port"))
        user = os.getenv("smtp_user")
        password = os.getenv("smtp_password")
        fromMail = os.getenv("smtp_from")
        toMail = os.getenv("smtp_to")

        # setting email the basic info
        msg = MIMEMultipart()
        msg["from"] = fromMail
        msg["to"] = toMail
        msg["subject"] = f"Dail TikTok report for {run_time.strftime('%d-%m-%y')}"

        # attaching body
        body = f"Please find the attached daily tiktok scraped data file for {run_time.strftime('%d-%m-%y')} "
        msg.attach(MIMEText(body))

        # attaching file
        logger.info(f"Attaching file: {file_dir}")
        with open(file_dir, "rb") as file:
            attachment = MIMEBase(
                "application", "vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            attachment.set_payload(file.read())
            encoders.encode_base64(attachment)
            attachment.add_header(
                "content-Disposition",
                "attachement",
                file_name=os.path.basename(file_dir),
            )
            msg.attach(attachment)

        logger.info(f"Connecting to SMTP server {host}:{port}")
        with smtplib.SMTP(host, port) as server:
            server.starttls()
            server.login(user, password)
            server.send_message(msg)
            logger.info("Email message sent successfully.")

    except FileNotFoundError:
        logger.error(
            f"File not found: {file_dir}. Please ensure the file is written first."
        )
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
