import requests
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Hit the EXACT same URL the user is using
url = "https://drain-sanitary-tr08.clean-pro.xyz/?k=c8b22f8a&t=A&cache_bust=FINAL_V96_TEST"
phone_ua = "Mozilla/5.0 (Linux; Android 13; SM-S918N) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/115.0.0.0 Mobile Safari/537.36"

print("=== FINAL V9.6 TEST ===")
print(f"URL: {url}")
print(f"UA: {phone_ua}")

r = requests.get(url, headers={'User-Agent': phone_ua}, timeout=15)
print(f"Status: {r.status_code}")
print(f"Content-Length: {len(r.text)}")
print(f"Has redirect JS: {'window.location.href' in r.text}")
print(f"First 300 chars: {r.text[:300]}")

# Now check if Telegram got the alert by checking logs
print("\n=== CHECKING LOGS ===")
import gspread, json
from oauth2client.service_account import ServiceAccountCredentials

json_path = r"h:\checkpoint-system\gen-lang-client-0222061612-b7f9fc3ed86a.json"
with open(json_path, 'r', encoding='utf-8') as f:
    service_info = json.load(f)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_info, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1RedTw8l_tdGyXqKL-6WrLosYuu_MGoBFX9dkaiTZdCM").sheet1

rows = sheet.get_all_values()
print(f"Total rows: {len(rows)}")
print("Last 5 entries:")
for row in rows[-5:]:
    print(row)
