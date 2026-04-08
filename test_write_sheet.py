import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import datetime
import traceback

def test_write():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    key_path = 'service_key.json'
    
    print("Testing Google Sheet Write Access...")
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(key_path, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key("1RedTw8l_tdGyXqKL-6WrLosYuu_MGoBFX9dkaiTZdCM").sheet1
        
        kst_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([kst_time, "LOCAL_TEST", "Antigravity", "API_CHECK", "127.0.0.1", "SUCCESS"])
        print(f"Successfully wrote to sheet at {kst_time}")
    except Exception as e:
        print(f"Write test failed: {repr(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    test_write()
