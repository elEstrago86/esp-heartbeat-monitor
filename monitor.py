import time
import requests
import os

FIREBASE_URL = "https://heartbeat-kamaleeva-default-rtdb.firebaseio.com/heartbeat.json"

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

MAX_DELAY_SECONDS = 15 * 60  # 15 минут

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

def main():
    r = requests.get(FIREBASE_URL)
    data = r.json()

    timestamp = data.get("timestamp")
    now = int(time.time())

    diff = now - timestamp

    print("Timestamp from Firebase:", timestamp)
    print("Current time:", now)
    print("Diff:", diff)

    if diff > MAX_DELAY_SECONDS:
        print("Timestamp too old, sending Telegram alert!")
        send_telegram("⚠️ Electricity might be OFF!")
    else:
        print("Everything is OK")

if __name__ == "__main__":
    main()
