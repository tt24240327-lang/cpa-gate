from flask import Flask, request, redirect
import datetime
import requests
import os
import sys
import base64
import json

# Mocking parts of index.py to test logic
class MockGeneEngine:
    def __init__(self):
        self.company_name = "Test Company"
        self.target_keyword = "Test Keyword"

def is_bot(ua):
    return "bot" in ua.lower()

CPA_DATA = {
    "c8b22f8a": ["이사업체", "LlocSbdUSY", "zdIDBDSzof"],
    "leak1234": ["누수탐지", "GkVRvxfx1T", "QOaojnBV2v"] # Mock 배관/누수
}
TARGET_A = "https://target-a.com"
TARGET_B = "https://target-b.com"

# Standardizing the key to the one that worked in audit
working_key = r"eyJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsICJwcm9qZWN0X2lkIjogImdlbi1sYW5nLWNsaWVudC0wMjIyMDYxNjEyIiwgInByaXZhdGVfa2V5X2lkIjogImI3ZjlmYzNlZDg2YTZlMWQxNDgyN2U2MDYzMGRjNGQwMTM4ODQzOTYiLCAicHJpdmF0ZV9rZXkiOiAiLS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tXG5NSUlFdlFJQkFEQU5CZ2txaGtpRzl3MEJBUUVGQUFTQ0JLY3dnZ1NqQWdFQUFvSUJBUUM0VFdzMTdTVFB3aWhtXG4yYWoxYW1rQk5IV2tQM0t6SGx1TVRUZzRxYytwTW1DTE1DRThQeG5pRVh6MTF2NmcyZXVEUi9rbWRORGM0RWtzXG5VNzVXSDRHOURhc1JaTW1rMEY3LzAxZnpWc3BsdGI1ZnFGNElEQkJuaE5xK3YyZDBRcTVwT2Y0eC9LL0F4WUxkXG50bjFxRmZJbC9GYWNFTThqYndleG02a1ZzZzdoYmptcHZCeVB5N2I3bmIzbktNWW1OcEpGUHBzem1zeVBPenFOXG4yVzlLd1B0NGtTQU9BL0RYdytqR3k1QldUazVFdU1maG9lVGttY1RyYlliNVpnVlA1bHdMMEoxWDJTdXFFdWpNXG5BTFBFQW5hYUM1THBBalVHbG9WQ0dMNlRyYmtKczVZeElvbTZiWmNUbDExUnp0Tk1HVjhRcE15T0VXSnFMOURyXG5Hd1h3UkZ6ZkFnTUJBQUVDZ2dFQUJ2dGY1RW44dVc5YmpDUzU3UStiQVI1dTFqNDhCSVExcE1nZ000bW9WMyswXG5zTFNDSnZlMy8vZmlDRU9HZ1hSVEZUVVArZXNPNjRHdGRPVk9BMmQ3cWdUZHVQRmh3S2l4UFE0YkRiekVHRzFhXG50N1ZJZDBmck84dGpTUHRUM0syMFJkYU9wRS9ZUEcrV1lKNHBuRXRnQlNTTUdaRk4vT1JiQnF6YzRoOE9Dakc1XG56U0h4OFpJT2cvcTFaVGV0ZmpQRjQwUDI1R0VxU0o1ZEpJS3JPeEdXSUJEcFNkY3JYQVUydkVoR2F1TWw5ajMyXG5scUtxZ3RlUGRTRHdqUW9rWmR6UEpmeU9NbzBSNXZVcllTTENScHJ5aW1yVmszWmFjQ0NIMXFoMlh3czNvM0owXG5MQlZiZmNDYWpLemFQbGRsaGVDOGJrOCtTMWdzUmgwb2dQa1NVRVd4d1FLQmdRRGVWOUE0VWY0dzV3TTVaSXo0XG5kQWV1SkFCemxuWTFULzQyMngvYURJSnRpd2F0bHVLd1U0YjVJOEhpVEJMcTVkbGphU2UrTE1NbW9sL3hYdzM4XG5uekROMGFoNzhBS3hDS01kM3I0Y3BEKy9SQ005OVFISDBMM1UyTmZ3UURPZWR6TkYva0pHYml1enZhdlZtcDFyXG5ibGh3T2tCUkQ2aTFPN2FvMTFudHUrV3g4UUtCZ1FEWXpuaThlR0NWUHo4anpvN2dRQSt5dDN5M1JsUWptSUc2XG5TRmRzbXhPb0YxeGZObVdhWENVTUltZVVBRi8xM3Z4aHF4K2o3TzFYb045NWxRRGRFekIvWlBYQS85UlRCQ1JUXG5vNEF0Tll0a1l3bHBrZ2luaGdWY2JXOTVDM1lIVkIvYVhHN3ppVm1xVDk5c2FObkUzSFpRRWc0SUxkOVhMNVlyXG5BMTFNVVFZcnp3S0JnQnVpNnB5MWhGVHJ3ZmpXU0xkeEpLcytpbGZUc2VtNmdheXIyKytzY21IUFVBc3ZvQW11XG51QzRyaGFQdE5NVEJ3UjJjS25aMjllTE5lQU4yZnpTUlRPMm9TN3JzQUVtayt6RnhTRXdqRmxGZDFNdVVzcDMxXG5ra0xzbVJxaHdFaklKRFZrL3pQbDZjU3pwTEl1UDdia3hsVmN5RFhMTG5zb2F2SGRvcTNzRndiaEFvR0FHcDAxXG42d1RuN2twR1NQSDVUZ1B2S1dRbTFpUzIvV3VpT1NqYU9vWEs0dTZETTFqdEhnYkRzWHFqdG1KWlpVaExPUDRWXG5zenpKWWVGb3JYY2lGUUZmQ2JSdUNwUWREMWZKMGM2WFZIVm5PQnFFTkVadDg0cWJLOTV2T2EremZIRFNQQzd1XG5tOHkzaWhXbCtwdmdaNjhjZ3ZYRWJUS2NZUXFCWjZSUkZxWTNtTGNDZ1lFQW9rRS9xa2FJeldQK2x3UUhHeXh3XG4wTXQveURMUHJieEpNbld4Nm9Gd2pnOXlRUjBua0hSdnFHV1p0YXpDVm5ML0J4NGlhbk1pVWcrczlmZ056WEFPXG5xSmFKSm81K21hbWwxTlZGTlJORWlIOTFLSm9OM0lhYWFSV2Q1Q090eE90eWFaUCtJUGtGb3ZyUlRmcjhkaEJaXG5oZVN0VG1FVmFCamVKbGk4cWJJRnFQST1cbi0tLS0tRU5EIFBSSVZBVEUgS0VZLS0tLS1cbiIsICJjbGllbnRfZW1haWwiOiAiYm90LWxvZ2dlckBnZW4tbGFuZy1jbGllbnQtMDIyMjA2MTYxMi5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsICJjbGllbnRfaWQiOiAiMTA5Nzk5NzM0OTk4OTQxNDAzODkxIiwgImF1dGhfdXJpIjogImh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbS9vL29hdXRoMi9hdXRoIiwgInRva2VuX3VyaSI6ICJodHRwczovL29hdXRoMi5nb29nbGVhcGlzLmNvbS90b2tlbiIsICJhdXRoX3Byb3ZpZGVyX3g1MDlfY2VydF91cmwiOiAiaHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vb2F1dGgyL3YxL2NlcnRzIiwgImNsaWVudF94NTA5X2NlcnRfdXJsIjogImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tI3JvYm90L3YxL21ldGFkYXRhL3g1MDkvYm90LWxvZ2dlciU0MGdlbi1sYW5nLWNsaWVudC0wMjIyMDYxNjEyLmlhbS5nc2VydmljZWFjY291bnQuY29tIiwgInVuaXZlcnNlX2RvbWFpbiI6ICJnb29nbGVhcGlzLmNvbSJ9"

# [Copy of the log_to_sheet from index.py]
def log_to_sheet(row_data):
    try:
        import base64, json
        import gspread
        from oauth2client.service_account import ServiceAccountCredentials
        service_info = json.loads(base64.b64decode(working_key).decode('utf-8'))
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(service_info, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key("1RedTw8l_tdGyXqKL-6WrLosYuu_MGoBFX9dkaiTZdCM").sheet1
        sheet.append_row(row_data)
        print(f"[SUCCESS] Data logged: {row_data[2:4]}")
    except Exception as e:
        print(f"[ERROR] Logging failed: {e}")

def run_test_logic(k, t, ua, test_name):
    print(f"\n--- Running Test: {test_name} (k={k}, t={t}) ---")
    is_bot_user = is_bot(ua)
    is_naver_bot = "naverbot" in ua.lower()
    is_google = "googlebot" in ua.lower()
    is_daum_bot = "daumbot" in ua.lower()
    client_ip = "127.0.0.1"
    ref_url = "http://test-referrer.com"
    request_host = "test-host"

    if k in CPA_DATA:
        cpa_info = CPA_DATA[k]
        kr_keyword = cpa_info[0]
        v_prefix = "B-" if t == 'B' else "A-"
        
        # Vendor detection logic
        if any(word in kr_keyword for word in ["이사", "견적", "용달"]): vendor_name = "모두이사" if t == 'B' else "이사방"
        elif any(word in kr_keyword for word in ["청소", "입주"]): vendor_name = "모두클린" if t == 'B' else "이사방"
        elif any(word in kr_keyword for word in ["누수", "변기", "하수구", "배관", "싱크대", "수전", "세면대"]): vendor_name = "착한환경" if t == 'B' else "뚫뚫배관"
        else: vendor_name = "기타"
        
        vendor = f"{v_prefix}{vendor_name}"
        outcome_status = "REDIRECT(CPA)"
        
        _is_stealth = is_bot_user and not (is_naver_bot or is_google or is_daum_bot)
        if _is_stealth:
            outcome_status = "CLOAKING(STEALTH)"
        
        kst_time = (datetime.datetime.now() + datetime.timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")
        log_to_sheet([kst_time, f"수익유저(TEST-{vendor})", outcome_status, f"{kr_keyword} (TEST)", client_ip, ref_url, request_host, ua])

if __name__ == "__main__":
    # Test 1: 이사방 (Normal)
    run_test_logic("c8b22f8a", "A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0", "이사방_정상유저")
    
    # Test 2: 뚫뚫배관 (Normal)
    run_test_logic("leak1234", "A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0", "뚫뚫배관_정상유저")
