# ==================================================================================
# 🚨 [CPA SYSTEM OPERATIONAL PHILOSOPHY - MANDATORY RULES] 🚨
# 1. DUAL-FACE SYSTEM: Guests see Real Landing (D), Bots see Fake Archive (C).
# 2. NO DIRECT REDIRECT: Let guests choose from the 'Category' choice page.
# 3. ANT-HELL LOOP: Bots stay trapped in tech docs.
# 4. ZERO ERROR TOLERANCE: Fallback to Fake Home on any crash.
# ==================================================================================
# 🧠 [HYPER-LEGO CONTROL CENTER v24.0 - DUAL-FACE EDITION]

import os, sys, hashlib
from flask import Flask, request, redirect

# [Path Fix] 
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# [Modular Imports]
from messenger import send_telegram
from guard import get_client_ip, determine_destination
from seo import generate_robots, generate_sitemap
from gene_engine import GeneEngine
from landing_engine import LandingEngine
from cpa_data import CPA_DATA, ALL_COMPANIES

app = Flask(__name__)

# --- CORE SETTINGS ---
TARGET_A = "https://replyalba.co.kr"
BRIDGE_MAP = {
    # [HIGHEST PRIORITY] Specific Hybrid Keywords
    "이사청소": "cleaning",
    "입주청소": "cleaning",
    "원상복구": "demolition",
    "누수탐지": "leak",
    
    # [LEVEL 2] Core Service Keywords
    "이사": "moving", 
    "청소": "cleaning", 
    "수전": "faucet", 
    "싱크대": "faucet", 
    "세면대": "faucet",
    "변기": "faucet", # Original MyHome has 'faucet' cat for toilet/sink replacement
    "배관": "leak",
    "누수": "leak", 
    "하수구": "leak", 
    "철거": "demolition", 
    "복구": "demolition",
    "용접": "welding"
}
ADMIN_IPS = ["61.83.9.20", "127.0.0.1", "61.83.9.15"]

@app.route('/robots.txt')
def robots():
    return generate_robots(request.host)

@app.route('/sitemap.xml')
def sitemap():
    return generate_sitemap(request.host)

@app.route('/api/track')
def track_conversion():
    try:
        target_url = request.args.get('url', TARGET_A)
        name = request.args.get('name', '업체')
        cat = request.args.get('cat', '분류')
        client_ip = get_client_ip(request)
        
        # Notify SUCCESS
        title = "🚀 [상담 전환 발생!]" if client_ip not in ADMIN_IPS else "🧪 [관리자 전환 테스트]"
        send_telegram(title, name, cat, client_ip, target_url)
        
        return redirect(target_url)
    except:
        return redirect(TARGET_A)

@app.route('/api/help_desk', methods=['POST'])
def help_desk():
    try:
        data = request.json
        name = data.get('name', '미상')
        phone = data.get('phone', '미상')
        q_type = data.get('type', '기타')
        message = data.get('message', '내용 없음')
        client_ip = get_client_ip(request)
        
        type_map = {'ad_req': '광고문의', 'partnership': '제휴제안', 'bug': '오류제보', 'other': '기타'}
        kr_type = type_map.get(q_type, q_type)
        
        msg = f"📩 [마이홈 문의접수]\n성함: {name}\n연락처: {phone}\n유형: {kr_type}\n내용: {message}\nIP: {client_ip}"
        send_telegram("📩 [문의/제휴]", name, kr_type, client_ip, f"내용: {message}")
        
        return {"status": "ok"}, 200
    except Exception as e:
        return {"status": "error", "msg": str(e)}, 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy_master_dual_face(path):
    try:
        k = request.args.get('k', '')
        t = request.args.get('t', 'A')
        
        # [1] GUARD: Determine identity and select Logic (C vs D)
        is_bot_user, is_test_mode, fe_cat, company_name, show_landing, companies_list = determine_destination(
            request, k, t, CPA_DATA, ALL_COMPANIES, BRIDGE_MAP, TARGET_A
        )
        
        client_ip = get_client_ip(request)

        # [2] REAL GUEST FLOW (Blueprint Logic D)
        # We check 'logical_path' which handles both /actual/path and /?path=...
        logical_path = request.args.get('path', path) if request.args.get('path') else path
        
        # [V26.3] BLUEPRINT SYNC: Only Guests see Landing. Admins (Test Mode) see Archive for monitoring.
        is_real_guest = (show_landing and not is_test_mode)
        
        # ONLY force landing page on the ROOT path for REAL GUESTS. 
        if is_real_guest and (logical_path == "" or logical_path == "/"):
            # Generate Cloaking URL for user verification (Simulate what bot sees)
            cloaking_url = f"{request.scheme}://{request.host}/archive-{fe_cat}"
            
            # Notify Influx (Real Guest Arrival)
            send_telegram("📡 [상담 페이지 유입]", "진짜손님", fe_cat, client_ip, request.url, is_bot_detect=False, cloaking_url=cloaking_url)
            
            # --- RESTORE ORIGINAL MYHOME PLANNER ---
            # Read the 1,429-line masterpiece originally created by the user
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            html_path = os.path.join(base_path, 'comparison_test.html')
            
            if os.path.exists(html_path):
                with open(html_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # [V11.1] INJECT TARGET CONTEXT (Automatic Leap)
                # This tells the original HTML to skip step 0 and go straight to the relevant category
                pixel_data = f"""
                <script>
                    window.InjectedData = {{
                        category: "{fe_cat}",
                        keyword: "{k}",
                        company_name: "{company_name}"
                    }};
                </script>
                """
                content = content.replace("<head>", f"<head>{pixel_data}")
                return content
            
            # Fallback if file missing (should not happen)
            return "Original Landing Missing", 404

        # [3] BOT/ADMIN CLOAKING FLOW (Blueprint Logic C)
        # Notify Influx (Bot or Test)
        ua_lower = request.headers.get('User-Agent', '').lower()
        is_naver = 'naver' in ua_lower or 'yeti' in ua_lower

        if (is_bot_user or k) and 'telegrambot' not in ua_lower:
            title = "🚨 [!!! 주적 네이버봇 침입 !!!]" if is_naver else "🔍 [봇 탐색 감지]"
            send_telegram(title, "봇/탐색기", fe_cat, client_ip, request.url, is_bot_detect=True)

        # Render Technical Archive
        seed = hashlib.md5(request.host.encode()).hexdigest()
        engine = GeneEngine(request.host, seed, db_cat=fe_cat, company_name=company_name, k=k, t=t)
        return engine.render(logical_path)

    except Exception as e:
        # [CRITICAL SAFETY NET]
        try:
            engine = GeneEngine(request.host, "fallback", "leak")
            return engine.render("/")
        except:
            return "System Stabilizing...", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
