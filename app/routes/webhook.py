from fastapi import APIRouter, Request
from app.services.ai_service import generate_reply
from app.services.messaging_service import send_instagram_message
import os

router = APIRouter()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

# 🔐 Verification endpoint
@router.get("/webhook")
async def verify_webhook(
    hub_mode: str = None,
    hub_challenge: str = None,
    hub_verify_token: str = None
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return int(hub_challenge)
    return {"error": "Verification failed"}


# 📩 Receive messages
@router.post("/webhook")
async def receive_webhook(request: Request):
    body = await request.json()

    print("Webhook received:", body)

    try:
        for entry in body.get("entry", []):

            # ✅ Case 1: Instagram messaging format
            if "messaging" in entry:
                for event in entry["messaging"]:
                    sender_id = event["sender"]["id"]

                    if "message" in event:
                        text = event["message"].get("text")
                        print("Incoming (messaging):", text)

                        if text:
                            ai_reply = generate_reply(text)
                            send_instagram_message(sender_id, ai_reply)

            # ✅ Case 2: Instagram Graph format
            if "changes" in entry:
                for change in entry["changes"]:
                    value = change.get("value", {})

                    if "messages" in value:
                        for msg in value["messages"]:
                            sender_id = msg["from"]
                            text = msg.get("text", {}).get("body")

                            print("Incoming (changes):", text)

                            if text:
                                ai_reply = generate_reply(text)
                                send_instagram_message(sender_id, ai_reply)

        return {"status": "ok"}

    except Exception as e:
        print("Error:", str(e))
        return {"error": str(e)}