from flask import Flask, request, Response
import requests
import os
import threading
from main import process_update
from logger import logger
from constants import BOT_TOKEN

app = Flask(name)
URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

@app.route("/webhook", methods=["POST"])
def webhook():
    """
    Handles incoming webhook requests from Telegram.
    """
    try:
        update = request.get_json()
        logger.info("Received update: %s", update)
        threading.Thread(target=process_update, args=(update,)).start()
        return Response(status=200)
    except Exception as e:
        logger.error("Webhook error: %s", str(e))
        return Response(status=500)

if name == "main":
    webhook_url = os.getenv("WEBHOOK_URL", "https://BGGO-render-app.onrender.com/webhook")
    try:
        response = requests.get(f"{URL}setWebhook?url={webhook_url}")
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        logger.info("Webhook set: %s", response.text)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error setting webhook: {e}")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
 
