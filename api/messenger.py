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

def send_telegram(title, name, cat, ip, url, is_bot_detect=False, cloaking_url=None):
    """
    [V27.0 SILENCE MODE] Sends detailed notification to Telegram with Overseas Filter.
    """
    try:
        # 1. Get Country First for Filtering
        res_data = requests.get(f"http://ip-api.com/json/{ip}", timeout=1).json()
        country_code = res_data.get('countryCode', '??').upper()
        country_name = res_data.get('country', '알 수 없음')
        
        # Add Flag Emoji
        flag = "".join(chr(127397 + ord(c)) for c in country_code.upper())
        country_info = f"{flag} {country_name}"

        # 2. [V27.0] OVERSEAS SILENCE LOGIC
        # If not Korea (KR) AND it's just a bot/admission (not a conversion/admin test)
        # Skip sending to focus on real revenue signals.
        is_admin_test = title and '🧪' in title
        if country_code != "KR" and not is_admin_test:
            # We still block them at guard.py, we just don't shout about it on Telegram.
            return True

        # 3. Translate Industry
        kr_cat = CAT_MAP.get(cat, cat)
        
        # 4. Message Framing
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
            
        # Dynamic Labeling
        if is_bot_detect:
            msg += f"\n🎭 봇이 보는 화면: {url}\n"
        else:
            msg += f"\n✅ 손님화면: {url}\n"
        
        if cloaking_url:
            msg += f"🎭 위장화면 (보충): {cloaking_url}\n"
        
        # Immediate timeout to prevent blocking
        requests.get(TELEGRAM_BOT_URL, params={"chat_id": CHAT_ID, "text": msg}, timeout=1)
        return True
    except:
        return False
