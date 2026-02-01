import os
import requests
import time

# === Конфигурация ===
firebase_url = os.environ["FIREBASE_URL"]
telegram_token = os.environ["TELEGRAM_TOKEN"]
chat_id = os.environ["TELEGRAM_CHAT_ID"]

# Максимальное допустимое время (в секундах)
threshold_seconds = 15 * 60  # 15 минут

# Получаем данные из Firebase
try:
    resp = requests.get(firebase_url)
    resp.raise_for_status()
    data = resp.json()
    timestamp = data.get("timestamp")
except Exception as e:
    print("Error fetching Firebase data:", e)
    timestamp = None

# Проверяем
if timestamp is None:
    msg = "⚠️ Cannot read heartbeat from Firebase!"
elif time.time() - timestamp > threshold_seconds:
    msg = "⚠️ Electricity might be OFF!"
else:
    print("Heartbeat OK")
    msg = None

# Отправляем Telegram, если нужно
if msg:
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": msg}
    try:
        r = requests.post(url, data=payload)
        r.raise_for_status()
        print("Telegram alert sent")
    except Exception as e:
        print("Failed to send Telegram alert:", e)
