import gspread, json, sys, io
from oauth2client.service_account import ServiceAccountCredentials

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

json_path = r"h:\checkpoint-system\gen-lang-client-0222061612-b7f9fc3ed86a.json"
with open(json_path, 'r', encoding='utf-8') as f:
    service_info = json.load(f)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_info, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1RedTw8l_tdGyXqKL-6WrLosYuu_MGoBFX9dkaiTZdCM").sheet1

all_data = sheet.get_all_values()

print(f"=== 특이 상태 혹은 뚫뚫배관/이사방 관련 로그 검색 ===")
for i, row in enumerate(all_data):
    if len(row) < 3: continue
    status = row[2]
    # Search for anomalies or names
    if "배관" in str(row) or "이사방" in str(row) or status not in ["REDIRECT(CPA)", "CLOAKING(STEALTH)", "상태"]:
        while len(row) < 8: row.append("")
        print(f"Row {i+1} | {row[0]} | {row[1]} | {row[2]} | {row[3]}")
