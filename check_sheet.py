import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

def check():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    key_path = 'service_key.json'
    creds = ServiceAccountCredentials.from_json_keyfile_name(key_path, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1RedTw8l_tdGyXqKL-6WrLosYuu_MGoBFX9dkaiTZdCM").sheet1
    
    vals = sheet.get_all_values()
    print(f"Total rows: {len(vals)}")
    for i, row in enumerate(vals[-5:]):
        print(f"Row {len(vals)-5+i}: {row}")

if __name__ == "__main__":
    check()
