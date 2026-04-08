import requests

TELEGRAM_BOT_URL = "https://api.telegram.org/bot7983385122:AAGK4kjCDpmerqfSwQL66ZDPL2MSOEV4An0/sendMessage"
CHAT_ID = "1898653696"

def send_telegram(title, name, cat, ip, url, is_bot_detect=False):
    """
    Sends notification to Telegram.
    Wrapped in try-except to never block the main web process.
    """
    try:
        if is_bot_detect:
            stamp = "🔍 [봇 탐색 감지]"
        else:
            stamp = title if title else "📡 [시스템 접속 알림]"
            
        msg = f"{stamp}\n 업체: {name}\n 업종: {cat}\n IP: {ip}\n 🔗 경로: {url}"
        
        # Immediate timeout to prevent blocking
        requests.get(TELEGRAM_BOT_URL, params={"chat_id": CHAT_ID, "text": msg}, timeout=1)
        return True
    except:
        return False
