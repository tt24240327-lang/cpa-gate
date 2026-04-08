import os, random, requests

def get_client_ip(request):
    return request.headers.get('CF-Connecting-IP', request.headers.get('X-Forwarded-For', request.remote_addr))

def is_bot(ua):
    if not ua: return False
    ua = ua.lower()
    # [V24.0] High Precision Bot Detection
    # DO NOT match 'naver' alone (prevents Naver App users from being treated as bots)
    bot_keywords = [
        'bot', 'crawl', 'spider', 'slurp', 'yeti', 'naverbot', 'googlebot', 
        'bingbot', 'inspection', 'lighthouse', 'headless', 'telegrambot'
    ]
    return any(k in ua for k in bot_keywords)

def determine_destination(request, k, t, CPA_DATA, ALL_COMPANIES, BRIDGE_MAP, TARGET_A):
    ua = request.headers.get('User-Agent', '')
    is_bot_user = is_bot(ua)
    
    # [V26.0] GEO-FENCING & SECURITY ENHANCEMENT
    client_ip = get_client_ip(request)
    country_code = "?? "
    try:
        # Re-use the lookup logic or just flag non-KR as high-risk
        res = requests.get(f"http://ip-api.com/json/{client_ip}", timeout=1).json()
        country_code = res.get('countryCode', '??').upper()
    except:
        pass

    # [Rule 1] OVERSEAS TRAFFIC IS ALWAYS BOTS (For Korea CPA)
    # If not KR, force bot status
    if country_code != "KR" and not is_bot_user:
        is_bot_user = True
    
    # [Rule 2] ADMIN BYPASS (Restored 'showmethemoney' for 형님)
    is_test_mode = 'showmethemoney' in request.args.getlist('bypass')
    
    # Defaults
    fe_cat = "leak"
    company_name = "이사방"
    show_landing = False
    companies_list = []

    # [3] Identify Category from k-value
    if k and k in CPA_DATA:
        kr_keyword = CPA_DATA[k][0]
        # Map KR keyword to category slug
        for kw, slug in BRIDGE_MAP.items():
            if kw in kr_keyword:
                fe_cat = slug
                break
        
        # Determine Company Name based on Category and 't' (A/B)
        companies_list = ALL_COMPANIES.get(fe_cat, [])
        if companies_list:
            idx = 1 if t == 'B' and len(companies_list) > 1 else 0
            company_name = companies_list[idx]['name']
            
        # [4] REVENUE SIGNAL: Real humans with k-value AND must be from KR
        if not is_bot_user and country_code == "KR":
            show_landing = True

    return is_bot_user, is_test_mode, fe_cat, company_name, show_landing, companies_list
