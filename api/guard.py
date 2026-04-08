import os, random

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
    is_test_mode = 'showmethemoney' in request.args.getlist('bypass')
    
    # Defaults
    fe_cat = "leak"
    company_name = "이사방"
    show_landing = False
    companies_list = []

    # [1] Identify Category from k-value
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
            # Simple logic: A uses first, B uses second (or randomized)
            idx = 1 if t == 'B' and len(companies_list) > 1 else 0
            company_name = companies_list[idx]['name']
            
        # [2] REVENUE SIGNAL: Real humans with k-value
        if not is_bot_user:
            show_landing = True

    # [3] TEST MODE SIGNAL: Force landing
    if is_test_mode:
        show_landing = True

    return is_bot_user, is_test_mode, fe_cat, company_name, show_landing, companies_list
