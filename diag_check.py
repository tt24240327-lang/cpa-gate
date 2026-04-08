import requests
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

url = "https://drain-sanitary-tr08.clean-pro.xyz/?k=c8b22f8a&t=A&cache_bust=DIAG_CHECK"
phone_ua = "Mozilla/5.0 (Linux; Android 13; SM-S918N) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/115.0.0.0 Mobile Safari/537.36"

r = requests.get(url, headers={'User-Agent': phone_ua}, timeout=15, allow_redirects=False)
print(f"Status: {r.status_code}")
print(f"Location Header: {r.headers.get('Location', 'NONE')}")
print(f"Full body:\n{r.text}")
