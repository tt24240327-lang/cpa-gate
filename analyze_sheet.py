import gspread, json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

json_path = r"h:\checkpoint-system\gen-lang-client-0222061612-b7f9fc3ed86a.json"
with open(json_path, 'r', encoding='utf-8') as f:
    service_info = json.load(f)

from oauth2client.service_account import ServiceAccountCredentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_info, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1RedTw8l_tdGyXqKL-6WrLosYuu_MGoBFX9dkaiTZdCM").sheet1

# Get all data
all_data = sheet.get_all_values()
print(f"총 행수: {len(all_data)}")
print(f"열 수: {len(all_data[0]) if all_data else 0}")

# Show first row (headers if any)
print(f"\n=== 1행 (헤더?) ===")
if all_data:
    for i, val in enumerate(all_data[0]):
        print(f"  열{i+1}: [{val}]")

# Show last 20 rows with column analysis
print(f"\n=== 마지막 20개 데이터 ===")
for row in all_data[-20:]:
    # Pad to 8 columns
    while len(row) < 8:
        row.append("")
    print(f"시간: {row[0]} | 타입: {row[1]} | 상태: {row[2]} | 키워드: {row[3][:25]} | IP: {row[4]} | 유입: {row[5][:40]} | 호스트: {row[6][:25]} | UA: {row[7][:30]}")

# Check for inconsistencies
print(f"\n=== 열 개수 분석 ===")
col_counts = {}
for row in all_data:
    n = len(row)
    col_counts[n] = col_counts.get(n, 0) + 1
for n, count in sorted(col_counts.items()):
    print(f"  {n}열: {count}행")

# Check unique types
print(f"\n=== 타입(2열) 종류 ===")
types = {}
for row in all_data:
    if len(row) >= 2:
        t = row[1]
        types[t] = types.get(t, 0) + 1
for t, count in sorted(types.items(), key=lambda x: -x[1]):
    print(f"  [{t}]: {count}건")

# Check unique statuses
print(f"\n=== 상태(3열) 종류 ===")
statuses = {}
for row in all_data:
    if len(row) >= 3:
        s = row[2]
        statuses[s] = statuses.get(s, 0) + 1
for s, count in sorted(statuses.items(), key=lambda x: -x[1]):
    print(f"  [{s}]: {count}건")
