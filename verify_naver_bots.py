import requests
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

url = "https://drain-sanitary-tr08.clean-pro.xyz/?k=c8b22f8a&t=A"

# 네이버가 사용하는 모든 알려진 봇 UA 변형
naver_bots = [
    ("Yeti (메인 크롤러)", "Mozilla/5.0 (compatible; Yeti/1.1; +http://naver.me/spd)"),
    ("Yeti (다른 변형)", "Mozilla/5.0 (Linux; Android 6.0.1) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 (compatible; Yeti/1.1; +http://naver.me/spd)"),
    ("NaverBot (레거시)", "NaverBot"),
    ("Naver Yeti Robot", "Yeti/1.0 (NHN Corp.; http://help.naver.com/support/robots.html)"),
    ("네이버 검색 수집봇", "Mozilla/5.0 (compatible; NaverBot/1.0; http://naver.me/bot)"),
    ("네이버 블로그 미리보기", "Mozilla/5.0 (compatible; NAVER Blog Rss Reader)"),
    ("네이버 앱 (모바일 - 사람)", "Mozilla/5.0 (iPhone; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) NAVER(inapp; search; 1000; 12.8.0)"),
    ("Whale 브라우저 (사람)", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Whale/4.35.351.16 Safari/537.36"),
    ("네이버 앱 블로그 (모바일 - 사람)", "Mozilla/5.0 (Linux; Android 14; SM-S926N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36 NAVER(inapp; blog; 900)"),
]

print("=== 네이버 봇 허점 검사 ===\n")
for name, ua in naver_bots:
    r = requests.get(url, headers={'User-Agent': ua}, timeout=10, allow_redirects=False)
    
    is_fake = 'naver-site-verification' in r.text or '본부' in r.text or '국제솔루션' in r.text
    is_redirect_302 = r.status_code == 302
    is_redirect_js = 'window.location.href' in r.text
    
    if r.status_code == 200 and is_fake:
        status = "🛡️ 가짜 사이트 (봇 차단 OK)"
    elif is_redirect_302:
        status = "👤 302 리다이렉트 (사람 취급)"
    elif is_redirect_js:
        status = "👤 JS 리다이렉트 (사람 취급)"
    else:
        status = f"❓ 알 수 없음 ({r.status_code})"
    
    print(f"[{name}]")
    print(f"  UA: {ua[:70]}...")
    print(f"  결과: {status}")
    print()
