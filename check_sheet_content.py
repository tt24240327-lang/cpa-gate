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

rows = sheet.get_all_values()
print(f"Total Rows: {len(rows)}")
for i, row in enumerate(rows[:10]):
    print(f"Row {i}: {row}")
