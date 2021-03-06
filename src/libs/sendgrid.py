import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from typing import List
from dateutil.parser import parse
from src.common import logger


class SendGridException(Exception):
    def __init__(self, message: str):
        self.message = message


class SendGrid:
    SENDGRID_FROM_EMAIL = os.environ.get('SENDGRID_FROM_EMAIL')
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

    @classmethod
    def send_email(cls, to_emails: List[str], subject: str, text_content: str, html_content: str):

        if cls.SENDGRID_API_KEY is None:
            raise SendGridException('Failed to load SENDGRID_API_KEY')
        if cls.SENDGRID_FROM_EMAIL is None:
            raise SendGridException('Failed to load SENDGRID_FROM_EMAIL')

        message = Mail(
            from_email=cls.SENDGRID_FROM_EMAIL,
            to_emails=to_emails,
            subject=f"[PriceWatch] {subject}",
            html_content=html_content,
            plain_text_content=text_content
        )
        sg = SendGridAPIClient(cls.SENDGRID_API_KEY)
        response = sg.send(message)

        if response.status_code != 202:
            logger.error("An error occurred while sending e-mail.", response.status_code, response.body, response.headers)
            raise SendGridException("An error occurred while sending e-mail.")

        message_id = response.headers.get('X-Message-Id')
        date = parse(response.headers.get('Date'))

        logger.info(date, "Email sent:", message_id)

        return date, message_id
