import requests

# Hardcoded details from index.py
BOT_TOKEN = "7983385122:AAGK4kjCDpmerqfSwQL66ZDPL2MSOEV4An0"
CHAT_ID = "1898653696"

def send_test_message():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": "🔔 [테스트] 형님, 이 메시지가 텔레그램에서 보입니까?\n(URL: https://web.telegram.org/a/#7983385122)"
    }
    try:
        r = requests.get(url, params=payload, timeout=5)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text}")
        if r.status_code == 200:
            print("Message sent successfully!")
        else:
            print("Failed to send.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    send_test_message()
