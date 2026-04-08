import gspread, json, sys, io, requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 1. Check sheet
json_path = r"h:\checkpoint-system\gen-lang-client-0222061612-b7f9fc3ed86a.json"
with open(json_path, 'r', encoding='utf-8') as f:
    service_info = json.load(f)

from oauth2client.service_account import ServiceAccountCredentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_info, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1RedTw8l_tdGyXqKL-6WrLosYuu_MGoBFX9dkaiTZdCM").sheet1

all_data = sheet.get_all_values()
print(f"=== 시트 전체 ({len(all_data)}행) ===\n")
for row in all_data:
    while len(row) < 8: row.append("")
    print(f"{row[0]} | {row[1]:10s} | {row[2]:20s} | {row[3][:25]:25s} | {row[4]:16s} | {row[5][:35]}")

# 2. Directly test: what does a Kakao stealth bot ACTUALLY see?
print("\n=== 봇이 실제로 보는 화면 검증 ===\n")

url = "https://drain-sanitary-tr08.clean-pro.xyz/?k=c8b22f8a&t=A"

# Kakao stealth bot (the exact same as what's showing in Telegram)
ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X)"
r = requests.get(url, headers={'User-Agent': ua}, timeout=10, allow_redirects=False)

is_fake = '국제솔루션' in r.text or '본부' in r.text or 'naver-site-verification' in r.text or '센터' in r.text
is_redirect = r.status_code == 302
has_cpa_link = 'replyalba' in r.text or 'albarich' in r.text

print(f"[카카오 스텔스 봇 - 짧은 Mac UA]")
print(f"  Status: {r.status_code}")
print(f"  가짜사이트 보이는가?: {'✅ YES' if is_fake else '❌ NO'}")
print(f"  CPA로 리다이렉트?: {'❌ YES (문제!)' if is_redirect else '✅ NO (정상)'}")
print(f"  CPA 링크 포함?: {'❌ YES (문제!)' if has_cpa_link else '✅ NO (정상)'}")
print(f"  응답 첫 200자: {r.text[:200]}")
