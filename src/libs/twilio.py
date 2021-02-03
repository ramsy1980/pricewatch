import os
from twilio.rest import Client
from dateutil.parser import parse
from src.common import logger

class TwilioException(Exception):
    def __init__(self, message: str):
        self.message = message


class Twilio:
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
    TWILIO_FROM_PHONE_NUMBER = os.environ.get('TWILIO_FROM_PHONE_NUMBER')

    @classmethod
    def send_sms(cls, to_phone_number: str, message: str) -> str:

        if cls.TWILIO_ACCOUNT_SID is None:
            raise TwilioException('Failed to load TWILIO_ACCOUNT_SID')
        if cls.TWILIO_AUTH_TOKEN is None:
            raise TwilioException('Failed to load TWILIO_AUTH_TOKEN')
        if cls.TWILIO_FROM_PHONE_NUMBER is None:
            raise TwilioException('Failed to load TWILIO_FROM_PHONE_NUMBER')

        client = Client(cls.TWILIO_ACCOUNT_SID, cls.TWILIO_AUTH_TOKEN)

        try:
            message = client.api.account.messages.create(
                to=to_phone_number,
                from_=cls.TWILIO_FROM_PHONE_NUMBER,
                body=message)

            message_id = message.sid
            date = message.date_created
            logger.info(date, "SMS sent:", message_id)

            return date, message_id
        except TwilioException as e:
            logger.error("Error sending SMS message:", e.message)
            return e.message
