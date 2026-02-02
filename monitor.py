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

def get_firebase_data():
    try:
        resp = requests.get(FIREBASE_URL, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print("Error fetching Firebase data:", e)
        return {}

def update_firebase_data(data):
    try:
        resp = requests.put(FIREBASE_URL, json=data, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print("Error updating Firebase data:", e)
        return {}

def send_telegram_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
        r = requests.get(url, timeout=10)
        print("Telegram response:", r.text)
    except Exception as e:
        print("Error sending Telegram message:", e)

# ======================
# Основной блок
# ======================
def main():
    fb_data = get_firebase_data()
    current_ts = fb_data.get("timestamp", 0)
    missed = fb_data.get("missed", 0)

    print(f"Firebase timestamp: {current_ts}")
    print(f"Firebase missed count: {missed}")

    # Проверяем, обновился ли таймстамп
    last_ts = fb_data.get("last_ts", 0)
    if current_ts == last_ts:
        missed += 1
        print(f"No update detected. Missed count: {missed}")
    else:
        missed = 0
        print("Timestamp updated. Missed count reset.")

    # Если достигли порога, шлем Telegram
    if missed >= MAX_MISSED:
        print("Alert threshold reached, sending Telegram alert!")
        send_telegram_alert("⚠️ Electricity might be OFF!")

    # Обновляем данные в Firebase
    update_data = {
        "timestamp": current_ts,
        "last_ts": current_ts,
        "missed": missed
    }
    update_firebase_data(update_data)

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
