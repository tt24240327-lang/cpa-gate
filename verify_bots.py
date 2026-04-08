import requests
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

url = "https://drain-sanitary-tr08.clean-pro.xyz/?k=c8b22f8a&t=A"

bots = [
    ("네이버 봇", "Mozilla/5.0 (compatible; Yeti/1.1; +http://naver.me/bot)"),
    ("구글 봇", "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"),
    ("다음 봇", "Mozilla/5.0 (compatible; DaumBot/1.0; +http://daum.net/bot)"),
]

for name, ua in bots:
    r = requests.get(url, headers={'User-Agent': ua}, timeout=10, allow_redirects=False)
    is_fake = '국제솔루션' in r.text or '본부' in r.text or 'naver-site-verification' in r.text
    is_redirect = r.status_code == 302 or 'window.location.href' in r.text
    
    if r.status_code == 200 and is_fake and not is_redirect:
        result = "✅ 가짜 사이트 (정상)"
    elif is_redirect:
        result = "❌ 리다이렉트 됨 (비정상!)"
    else:
        result = f"❓ 알 수 없음 (Status: {r.status_code})"
    
    print(f"[{name}] {result}")
