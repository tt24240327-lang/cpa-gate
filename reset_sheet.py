import gspread, json, sys, io
from oauth2client.service_account import ServiceAccountCredentials

# encoding for windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 1. Auth setup
json_path = r"h:\checkpoint-system\gen-lang-client-0222061612-b7f9fc3ed86a.json"
with open(json_path, 'r', encoding='utf-8') as f:
    service_info = json.load(f)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_info, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1RedTw8l_tdGyXqKL-6WrLosYuu_MGoBFX9dkaiTZdCM").sheet1

# 2. Reset with EXTENDED 5-COLUMN FORMAT
print("📊 구글 시트 초기화 시작 (5개 열 형식 - IP 추가)...")
sheet.clear()

# headers
headers = ["날짜/시간", "구분", "상세내용(키워드/업체)", "경로/유입/연락처", "IP 주소"]
sheet.append_row(headers)

# Basic Formatting via native gspread
try:
    sheet.format("A1:E1", {
        "backgroundColor": {"red": 0.1, "green": 0.45, "blue": 0.9},
        "horizontalAlignment": "CENTER",
        "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}, "fontSize": 11}
    })
    sheet.freeze(rows=1)
    
    # Set widths for 5 columns
    # In gspread, we set column metadata via batch_update or similar if available, 
    # but easiest is to just let it be or use set_column_width if it worked (it didn't before).
except Exception as e:
    print(f"[알림] 포맷팅 스킵되었습니다 (에러: {e})")

print("✅ 시트 초기화 완료! 이제 IP 주소를 포함하여 5개 열 형식으로 저장됩니다.")
