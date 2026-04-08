import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

def search_songam():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    key_path = 'h:\\checkpoint-system\\service_key.json'
    creds = ServiceAccountCredentials.from_json_keyfile_name(key_path, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1RedTw8l_tdGyXqKL-6WrLosYuu_MGoBFX9dkaiTZdCM").sheet1
    
    vals = sheet.get_all_values()
    print(f"Total rows in sheet: {len(vals)}")
    
    # Header: [Time, Type, Status, Keyword/Path, IP, Referrer, Host, UA]
    matches = []
    for i, row in enumerate(vals):
        row_str = " ".join(row)
        if "송암동" in row_str:
            matches.append((i + 1, row))
            
    if not matches:
        print("No matches for '송암동' found in the sheet.")
        # Let's also print the last 10 rows just in case encoding is the issue
        print("\nLast 10 rows for reference:")
        for i, row in enumerate(vals[-10:]):
            print(f"Row {len(vals)-9+i}: {row}")
    else:
        print(f"Found {len(matches)} matches for '송암동':")
        for line_no, row in matches:
            print(f"Row {line_no}: {row}")

if __name__ == "__main__":
    search_songam()
