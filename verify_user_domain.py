import requests
import sys
import io

# Force UTF-8 for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# User's Domain
user_url = "https://drain-sanitary-tr08.clean-pro.xyz/?k=c8b22f8a&t=A&cache_bust=VERIFY_USER_DOMAIN"
# Bot UA that SHOULD trigger an alert if V9.5 is active
bot_ua = "GenericBot/1.0"

print("--- USER DOMAIN VERIFICATION ---")
print(f"Target: {user_url}")

try:
    r = requests.get(user_url, headers={'User-Agent': bot_ua}, timeout=10)
    print(f"Status: {r.status_code}")
    print("Headers:", r.headers)
    
    if '안내' in r.text or '보안' in r.text:
        print("Result: ✅ Fake Site Found (Domain is Active & Updated)")
    elif 'window.location.href' in r.text:
        print("Result: ❌ Redirect Found (Wait, Bot should be fake site!)") 
    else:
        print("Result: ❓ Unknown Content")
        print("--- RESPONSE SNIPPET (First 500 chars) ---")
        print(r.text[:500])
        
except Exception as e:
    print(f"Error: {e}")
