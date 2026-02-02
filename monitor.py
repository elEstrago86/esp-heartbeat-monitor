import time
import requests
import os


TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
FIREBASE_URL = os.environ.get("FIREBASE_URL")  # например: https://heartbeat-kamaleeva-default-rtdb.firebaseio.com/heartbeat.json

# ======================
# Настройки проверки
# ======================
# Считаем, что ESP должна обновлять timestamp каждые N секунд
HEARTBEAT_INTERVAL = 30        # ESP отправляет heartbeat каждые 30 секунд
MAX_MISSED = 4                 # Максимальное количество пропущенных heartbeat
ALERT_THRESHOLD = HEARTBEAT_INTERVAL * MAX_MISSED  # секунд

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

# ======================
# Основной блок
# ======================
def main():
    fb_timestamp = get_firebase_timestamp()
    current_time = int(time.time())
    diff = current_time - fb_timestamp

    print(f"Timestamp from Firebase: {fb_timestamp}")
    print(f"Current time: {current_time}")
    print(f"Diff: {diff}")

    if diff > ALERT_THRESHOLD:
        print("Timestamp too old, sending Telegram alert!")
        send_telegram_alert("⚠️ Electricity might be OFF!")
    else:
        print("Heartbeat is fresh, everything OK.")

if __name__ == "__main__":
    main()
