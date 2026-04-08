import base64, json, gspread
from oauth2client.service_account import ServiceAccountCredentials
import traceback
import re

def test_from_file():
    with open('api/index.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = re.search(r'b64_key = r\"(.*?)\"', content)
    if not match:
        print("B64 Key not found in index.py")
        return
    
    b64_key = match.group(1)
    print(f"Testing B64 key of length {len(b64_key)}")
    
    try:
        # Step 1: B64 Decode
        decoded_bytes = base64.b64decode(b64_key)
        print("Step 1: B64 Decode Success")
        
        # Step 2: UTF-8 Decode
        json_str = decoded_bytes.decode('utf-8')
        print("Step 2: UTF-8 Decode Success")
        
        # Step 3: JSON Load
        service_info = json.loads(json_str)
        print("Step 3: JSON Load Success")
        
        # Step 4: Auth
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(service_info, scope)
        print("Step 4: Creds Success")
        
    except Exception as e:
        print(f"FAILED with error: {repr(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    test_from_file()
