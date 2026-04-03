import requests
from app.core.config import settings

def send_instagram_message(recipient_id: str, message: str):
    url = f"https://graph.facebook.com/v25.0/{settings.PAGE_ID}/messages"

    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message},
        "access_token": settings.PAGE_ACCESS_TOKEN
    }

    res = requests.post(url, json=payload)
    return res.json()