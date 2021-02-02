import requests
import io
from django.conf import settings
from enum import Enum

class PushoverException(Exception):
    pass

class PushoverPriority(Enum):
    LOWEST = -2
    LOW = -1
    NORMAL = 0
    HIGH = 1
    EMERGENCY = 2

# message and title should be strings, attachment should be a file-like object
def pushover_notification(user_key, message, title = None, attachment = None, priority = PushoverPriority.NORMAL):
    API_URL = "https://api.pushover.net/1/messages.json"

    if len(message) > 1024:
        raise PushoverException("Maximum message size of 1024 characters exceeded!")

    if title and len(title) > 250:
        raise PushoverException("Maximum title size of 250 characters exceeded!")


    payload = {
        "token": settings.PUSHOVER_APP_TOKEN,
        "user": user_key,
        "priority": priority.value,
        "message": message
    }

    if title:
        payload["title"] = title

    files = None
    if attachment:
        if attachment is bytes:
            files = {
                "attachment": io.BytesIO(attachment)
            }
        else:
            files = {
                "attachment": attachment
            }

    req = requests.post(API_URL, data=payload, files = files)

    if req.status_code != requests.codes.ok:
        raise req.raise_for_status

    return True
