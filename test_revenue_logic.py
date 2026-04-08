import base64, json, gspread
from oauth2client.service_account import ServiceAccountCredentials
import traceback
import re
import datetime

def test_revenue_logic():
    with open('api/index.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the SECOND b64_key (Revenue section)
    keys = re.findall(r'b64_key = r\"(.*?)\"', content)
    if len(keys) < 2:
        print("Less than 2 keys found")
        return
    
    b64_key = keys[1]
    print(f"Testing Revenue B64 key of length {len(b64_key)}")
    
    try:
        service_info = json.loads(base64.b64decode(b64_key).decode('utf-8'))
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(service_info, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key("1RedTw8l_tdGyXqKL-6WrLosYuu_MGoBFX9dkaiTZdCM").sheet1
        
        kst_time = (datetime.datetime.now() + datetime.timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")
        print(f"Attempting append for {kst_time}")
        # Use dummy data
        sheet.append_row([kst_time, "DEBUG_TEST", "TEST_VENDOR", "TEST_KEYWORD", "1.1.1.1", "h://test"])
        print("SUCCESS: Append worked!")
        
    except Exception as e:
        print(f"FAILED with error: {repr(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    test_revenue_logic()
