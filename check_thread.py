import requests
import json
import os

# === CONFIGURATION ===
THREAD_URL = "https://c.realme.com/in/api/thread/1917897202945052672"
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
LAST_CONTENT_FILE = "last_content.json"

def send_telegram_notification(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=data)

def fetch_thread_content():
    try:
        response = requests.get(THREAD_URL)
        data = response.json()
        if data["status"] == "success":
            return data["data"]["contentRaw"]
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def load_last_content():
    if os.path.exists(LAST_CONTENT_FILE):
        with open(LAST_CONTENT_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("contentRaw")
    return None

def save_current_content(content):
    with open(LAST_CONTENT_FILE, "w", encoding="utf-8") as f:
        json.dump({"contentRaw": content}, f)

def main():
    current_content = fetch_thread_content()
    if not current_content:
        print("Failed to fetch current content.")
        return

    last_content = load_last_content()
    if last_content is None:
        print("No previous content. Saving current.")
        save_current_content(current_content)
        return

    if current_content != last_content:
        print("Content changed!")
        send_telegram_notification(
            "🛠 <b>realme thread content has been edited!</b>\n\n🔗 <a href='https://c.realme.com/in/post-details/1917897202945052672'>View Post</a>"
        )
        save_current_content(current_content)
    else:
        print("No change in content.")

if __name__ == "__main__":
    main()
