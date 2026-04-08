import gspread
import base64
import json
from oauth2client.service_account import ServiceAccountCredentials

json_path = r"h:\checkpoint-system\gen-lang-client-0222061612-b7f9fc3ed86a.json"

with open(json_path, 'r', encoding='utf-8') as f:
    service_info = json.load(f)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_info, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1RedTw8l_tdGyXqKL-6WrLosYuu_MGoBFX9dkaiTZdCM").sheet1

rows = sheet.get_all_values()
print("--- LAST 30 LOG ENTRIES ---")
for row in rows[-30:]:
    print(row)
