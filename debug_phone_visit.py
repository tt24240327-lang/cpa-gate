import requests
import time

url = "https://cpa-gate.vercel.app/?k=ce8a5ce4&t=A&cache_bust=DEBUG_PHONE"
# Generic Samsung Phone UA (which the user might be using)
phone_ua = "Mozilla/5.0 (Linux; Android 13; SM-S918N) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/115.0.0.0 Mobile Safari/537.36"

print("--- PHONE VISIT SIMULATION ---")
try:
    print(f"Target: {url}")
    print(f"UA: {phone_ua}")
    
    r = requests.get(url, headers={'User-Agent': phone_ua}, timeout=10)
    print(f"Status: {r.status_code}")
    
    # Check if 'redirect' occurred (since humans should redirect)
    if 'window.location.href' in r.text:
        print("Result: Redirect Script Found (Normal Human Traffic)")
        # Extract redirect target for confirmation
        import re
        match = re.search(r'window\.location\.href\s*=\s*["\']([^"\']+)["\']', r.text)
        if match:
            print(f"Redirect Target: {match.group(1)}")
    elif '안내' in r.text:
        print("Result: Fake Site (Bot Traffic)")
    else:
        print("Result: Unknown Page Content")
        print(r.text[:200]) # First 200 chars for debugging

except Exception as e:
    print(f"Error: {e}")
