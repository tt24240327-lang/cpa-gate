import requests
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

url = "https://drain-sanitary-tr08.clean-pro.xyz/?k=c8b22f8a&t=A"

tests = [
    # [봇 - 가짜 사이트 보여야 함]
    ("네이버 Yeti", "Mozilla/5.0 (compatible; Yeti/1.1; +http://naver.me/spd)", "BOT"),
    ("구글봇", "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)", "BOT"),
    ("다음봇", "Mozilla/5.0 (compatible; DaumBot/1.0; +http://daum.net/bot)", "BOT"),
    ("카카오 스텔스 (짧은 Mac UA)", "Mozilla/5.0 (Macintosh; Intel Mac OS X)", "BOT"),
    ("네이버 스텔스 (짧은 UA)", "Mozilla/5.0 (compatible; NAVER Blog Rss Reader)", "BOT"),
    
    # [사람 - CPA 리다이렉트 되어야 함]
    ("크롬 PC", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36", "HUMAN"),
    ("크롬 안드로이드", "Mozilla/5.0 (Linux; Android 14; SM-S926N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36", "HUMAN"),
    ("사파리 아이폰", "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1", "HUMAN"),
    ("삼성 인터넷", "Mozilla/5.0 (Linux; Android 13; SM-S918N) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/115.0.0.0 Mobile Safari/537.36", "HUMAN"),
    ("Whale 브라우저", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Whale/4.35.351.16 Safari/537.36", "HUMAN"),
    ("네이버 앱 (모바일)", "Mozilla/5.0 (iPhone; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) NAVER(inapp; search; 1000; 12.8.0)", "HUMAN"),
    ("카카오톡 인앱", "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) KAKAOTALK 10.4.2", "HUMAN"),
    ("파이어폭스", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0", "HUMAN"),
]

print("=== V9.8 전체 검증 ===\n")
passed = 0
failed = 0

for name, ua, expected in tests:
    r = requests.get(url, headers={'User-Agent': ua}, timeout=10, allow_redirects=False)
    
    is_fake = 'naver-site-verification' in r.text or '본부' in r.text or '국제솔루션' in r.text or '센터' in r.text
    is_redirect = r.status_code == 302 or 'window.location.href' in r.text
    
    if expected == "BOT":
        if r.status_code == 200 and is_fake:
            result = "✅ PASS - 가짜 사이트"
            passed += 1
        else:
            result = f"❌ FAIL - {r.status_code} (가짜 사이트여야 하는데!)"
            failed += 1
    else:  # HUMAN
        if r.status_code == 302:
            result = "✅ PASS - 302 CPA 리다이렉트"
            passed += 1
        else:
            result = f"❌ FAIL - {r.status_code} (리다이렉트여야 하는데!)"
            failed += 1
    
    print(f"[{name}] {result}")

print(f"\n=== 결과: {passed}/{passed+failed} 통과 ===")
if failed == 0:
    print("🎉 전체 통과!")
