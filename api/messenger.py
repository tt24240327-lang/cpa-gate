import requests

TELEGRAM_BOT_URL = "https://api.telegram.org/bot7983385122:AAGK4kjCDpmerqfSwQL66ZDPL2MSOEV4An0/sendMessage"
CHAT_ID = "1898653696"

CAT_MAP = {
    "moving": "포장이사/용달",
    "cleaning": "입주/이사청소",
    "faucet": "수전/변기교체",
    "leak": "누수탐지/배관",
    "demolition": "철거/원상복구",
    "welding": "출장용접",
    "faucet_fix": "수도설비"
}

def get_country(ip):
    try:
        # Fast Geo-IP Lookup (No API key needed)
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=1).json()
        country = res.get('country', '알 수 없음')
        code = res.get('countryCode', '??')
        # Add Flag Emoji
        flag = "".join(chr(127397 + ord(c)) for c in code.upper())
        return f"{flag} {country}"
    except:
        return "🌐 정보 없음"

def send_telegram(title, name, cat, ip, url, is_bot_detect=False, cloaking_url=None):
    """
    [V25.0 PREMIUM] Sends detailed notification to Telegram.
    """
    try:
        # 1. Translate Industry
        kr_cat = CAT_MAP.get(cat, cat)
        
        # 2. Get Country
        country_info = get_country(ip)
        
        # 3. Message Framing
        if is_bot_detect:
            stamp = "🔍 [봇 탐색 감지]"
        elif title:
            stamp = title
        else:
            stamp = "📡 [상담 페이지 유입]"

        msg = f"{stamp}\n"
        msg += f"📍 국가: {country_info}\n"
        msg += f"🌐 아이피: {ip}\n"
        msg += f"📦 업종: {kr_cat}\n"
        
        if name:
            msg += f"🏢 업체: {name}\n"
            
        msg += f"\n✅ 손님화면: {url}\n"
        
        if cloaking_url:
            msg += f"🎭 위장화면: {cloaking_url}\n"
        
        # Immediate timeout to prevent blocking
        requests.get(TELEGRAM_BOT_URL, params={"chat_id": CHAT_ID, "text": msg}, timeout=1)
        return True
    except:
        return False
