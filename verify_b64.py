import base64, json, gspread
from oauth2client.service_account import ServiceAccountCredentials
import traceback

def final_verify():
    with open('verified_b64.txt', 'r') as f:
        b64_key = f.read().strip()
    
    try:
        service_info = json.loads(base64.b64decode(b64_key).decode('utf-8'))
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(service_info, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key("1RedTw8l_tdGyXqKL-6WrLosYuu_MGoBFX9dkaiTZdCM").sheet1
        print("SUCCESS: Credentials authorized and sheet opened!")
    except Exception as e:
        print("FAILED: Verification failed")
        traceback.print_exc()

if __name__ == "__main__":
    final_verify()
