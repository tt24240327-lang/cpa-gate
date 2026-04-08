import requests
import time
import sys
import io

# Force UTF-8 for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

url = "https://cpa-gate.vercel.app/?k=ce8a5ce4&t=A&cache_bust="

scenarios = [
    {
        "name": "TEST-GENERIC-BOT",
        "ua": "GenericBot/1.0",
        "desc": "듣보잡 봇 (알림+시트+가짜사이트)"
    },
    {
        "name": "TEST-NAVER-BOT",
        "ua": "Mozilla/5.0 (compatible; Yeti/1.1; +http://naver.me/bot)",
        "desc": "네이버 봇 (알림+시트+가짜사이트)"
    },
    {
        "name": "TEST-HUMAN-PHONE",
        "ua": "Mozilla/5.0 (Linux; Android 13; SM-S918N) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/115.0.0.0 Mobile Safari/537.36",
        "desc": "사람 (폰 접속) (알림+시트+리다이렉트)"
    }
]

print("--- FULL TRAFFIC SIMULATION ---")
for s in scenarios:
    full_url = url + s['name'] + "_V9.4"
    print(f"\n[Scenario: {s['desc']}]")
    print(f"UA: {s['ua']}")
    try:
        r = requests.get(full_url, headers={'User-Agent': s['ua']}, timeout=10)
        print(f"Status: {r.status_code}")
        
        if 'window.location.href' in r.text:
            print("Result: ✅ Redirect Found (HUMAN)")
        elif '안내' in r.text or '보안' in r.text:
            print("Result: ✅ Fake Site Found (BOT)")
        else:
            print("Result: ❓ Unknown Content")
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(1) # Brief pause
