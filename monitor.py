import time
import requests
import os
import json


TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
FIREBASE_URL = os.environ.get("FIREBASE_URL")  # например: https://heartbeat-kamaleeva-default-rtdb.firebaseio.com/heartbeat.json

# ======================
# Настройки проверки
# ======================
MAX_MISSED = 4                 # Максимальное количество пропущенных heartbeat

# Файл для хранения последнего timestamp и счётчика пропусков
STATE_FILE = "state.json"


# ======================
# Функции
# ======================
def get_firebase_timestamp():
    try:
        resp = requests.get(FIREBASE_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return int(data.get("timestamp", 0))
    except Exception as e:
        print("Error fetching Firebase timestamp:", e)
        return 0

def send_telegram_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
        r = requests.get(url, timeout=10)
        print("Telegram response:", r.text)
    except Exception as e:
        print("Error sending Telegram message:", e)

def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {"last_timestamp": 0, "missed": 0}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

# ======================
# Основной блок
# ======================
def main():
    fb_timestamp = get_firebase_timestamp()
    state = load_state()

    print(f"Timestamp from Firebase: {fb_timestamp}")
    print(f"Last timestamp: {state['last_timestamp']}")

    if fb_timestamp == state["last_timestamp"]:
        state["missed"] += 1
        print(f"No update detected. Missed count: {state['missed']}")
    else:
        state["missed"] = 0
        state["last_timestamp"] = fb_timestamp
        print("Timestamp updated. Missed count reset.")

    if state["missed"] >= MAX_MISSED:
        print("Alert threshold reached, sending Telegram alert!")
        send_telegram_alert("⚠️ Electricity might be OFF!")

    save_state(state)

if __name__ == "__main__":
    main()
