import requests

ua_whale_mac = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Whale/2.10.124.26 Safari/537.36'
ua_ipad_naver = 'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) NAVER(inapp; search; 1000; 10.20.30)'

url = 'https://cpa-gate.vercel.app/?k=ce8a5ce4&t=A&cache_bust=SAFECHECK_V3'

print('--- NAVER MAC/APP SAFETY CHECK ---')

def check(name, ua):
    try:
        r = requests.get(url, headers={'User-Agent': ua}, timeout=5)
        if '"status": "' in r.text:
            status = r.text.split('"status": "')[1].split('"')[0]
        else:
            status = 'FAIL_PARSE'
        print(f'[{name}] Status: {status}')
    except Exception as e:
        print(f'[{name}] Error: {e}')

check('WHALE-MAC', ua_whale_mac)
check('IPAD-NAVER', ua_ipad_naver)
