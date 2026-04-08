import requests

# 'bot' is usually in the blocklist
ua_generic_bot = 'GenericBot/1.0'

url = 'https://cpa-gate.vercel.app/?k=ce8a5ce4&t=A&cache_bust=GENERIC_BOT_V2'

print('--- GENERIC BOT ALERT CHECK ---')

def check(name, ua):
    try:
        r = requests.get(url, headers={'User-Agent': ua}, timeout=10)
        print(f'[{name}] Status: {r.status_code}')
        if '안내' in r.text or '보안' in r.text or '센터소개' in r.text:
            print(f'[{name}] Result: CAUGHT AS BOT (Fake Site Shown)')
        else:
            print(f'[{name}] Result: TREATED AS HUMAN')
    except Exception as e:
        print(f'[{name}] Error: {e}')

check('GENERIC-BOT', ua_generic_bot)
