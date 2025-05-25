from flask import Flask
from threading import Thread
import requests
import time
from logger import logger

app = Flask('')

@app.route('/')
def home():
    return "I’m alive"

def run():
    app.run(host='0.0.0.0', port=8080)
    logger.info("Keep-alive server started.")

def ping():
    while True:
        try:
            # URLs to ping to keep the app alive
            urls_to_ping = [
                "https://your-render-app.onrender.com",  # Replace with your actual Render app URL
                "https://api.telegram.org"
            ]
            for url in urls_to_ping:
                response = requests.get(url)
                response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
                logger.info(f"Successfully pinged {url}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error pinging URLs: {e}")
        time.sleep(600)  # every 10 minutes

def keep_alive():
    t1 = Thread(target=run)
    t1.start()
    t2 = Thread(target=ping)
    t2.start()
    logger.info("Keep-alive threads started.")
