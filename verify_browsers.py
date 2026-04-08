import requests
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

url = "https://drain-sanitary-tr08.clean-pro.xyz/?k=c8b22f8a&t=A"

browsers = [
    ("크롬 (PC)", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"),
    ("크롬 (안드로이드)", "Mozilla/5.0 (Linux; Android 14; SM-S926N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"),
    ("사파리 (아이폰)", "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1"),
    ("사파리 (맥)", "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15"),
    ("삼성 인터넷", "Mozilla/5.0 (Linux; Android 13; SM-S918N) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/115.0.0.0 Mobile Safari/537.36"),
    ("파이어폭스 (PC)", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"),
    ("엣지 (PC)", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"),
    ("카카오톡 인앱", "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) KAKAOTALK 10.4.2"),
]

print("=== 일반 브라우저 접속 테스트 ===\n")
for name, ua in browsers:
    r = requests.get(url, headers={'User-Agent': ua}, timeout=10, allow_redirects=False)
    
    if r.status_code == 302:
        loc = r.headers.get('Location', '')
        print(f"[{name}] 👤 사람 → 302 CPA 리다이렉트 ✅")
        print(f"  → {loc}")
    elif 'window.location.href' in r.text:
        print(f"[{name}] 👤 사람 → JS 리다이렉트 ✅")
    elif 'naver-site-verification' in r.text or '본부' in r.text:
        print(f"[{name}] ❌ 가짜 사이트 보임 (오탐지!)")
    else:
        print(f"[{name}] ❓ 알 수 없음 (Status: {r.status_code})")
    print()
