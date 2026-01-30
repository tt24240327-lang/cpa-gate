
import requests
import time
import json

TOKEN = "7983385122:AAGK4kjCDpmerqfSwQL66ZDPL2MSOEV4An0"
URL = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

print(f"🔍 Checking for updates on Bot: {TOKEN[:5]}...")

try:
    response = requests.get(URL, timeout=10)
    data = response.json()
    
    if not data.get("ok"):
        print(f"❌ Error: {data}")
        exit()
        
    results = data.get("result", [])
    if not results:
        print("⚠️ No messages found. Please send 'Hello' to your bot in Telegram first!")
    else:
        print("\n✅ Found Messages:")
        for update in results:
            if "message" in update and "chat" in update["message"]:
                chat = update["message"]["chat"]
                print(f"   -> Chat ID: {chat['id']} ({chat.get('type')}) - {chat.get('username') or chat.get('first_name')}")
                
except Exception as e:
    print(f"❌ Connection Failed: {e}")
