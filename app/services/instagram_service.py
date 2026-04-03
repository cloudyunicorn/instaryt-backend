import requests
from app.core.config import settings

BASE_URL = "https://graph.facebook.com/v25.0"

def create_container(media_url: str, caption: str, is_video: bool):
    url = f"{BASE_URL}/{settings.IG_USER_ID}/media"

    payload = {
        "caption": caption,
        "access_token": settings.IG_ACCESS_TOKEN
    }

    if is_video:
        payload["video_url"] = media_url
        payload["media_type"] = "REELS"
    else:
        payload["image_url"] = media_url

    res = requests.post(url, data=payload)
    return res.json()


def publish_container(container_id: str):
    url = f"{BASE_URL}/{settings.IG_USER_ID}/media_publish"

    payload = {
        "creation_id": container_id,
        "access_token": settings.IG_ACCESS_TOKEN
    }

    res = requests.post(url, data=payload)
    return res.json()