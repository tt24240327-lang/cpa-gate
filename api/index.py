import hashlib, time, random, json, re, os, requests
from flask import Flask, request, redirect, make_response
from urllib.parse import urlencode

try:
    from cpa_data import CPA_DATA, KEYWORD_MAP, ALL_COMPANIES
    from domain_pool import DOMAIN_POOL
except ImportError:
    try:
        from api.cpa_data import CPA_DATA, KEYWORD_MAP, ALL_COMPANIES
        from api.domain_pool import DOMAIN_POOL
    except ImportError:
        CPA_DATA = {}
        KEYWORD_MAP = {}
        ALL_COMPANIES = {}
        DOMAIN_POOL = []


app = Flask(__name__)

# ==================================================================================
# [HYPER-LEGO ASSEMBLY ENGINE v9] - RESTORED FROM BACKUP
# ==================================================================================

class GeneEngine:
    def __init__(self, seed_str):
        self.raw_seed = seed_str
        self.r = random.Random(seed_str)
        self.main_types = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        self.major_type = self.r.choice(self.main_types)
        self.sub_type = self.r.randint(1, 3)
        self.skeleton_id = self.r.randint(1, 24)
        self.archive_style = self.r.randint(1, 10)
        
        self.menu_pool = {
            "home": ["MAIN", "HUB", "종합현황", "HOME", "START"],
            "about": ["STORY", "PROFILE", "센터소개", "인사말", "ABOUT"],
            "archive": ["DATA", "GUIDE", "자료실", "기술문서", "ARCHIVE"],
            "service": ["FIELD", "PROJECT", "주요업무", "전문분야", "BUSINESS"],
            "contact": ["Q&A", "FORUM", "HELP", "ASK", "고객센터"]
        }
        self.nav = {k: self.r.choice(v) for k, v in self.menu_pool.items()}
        
        self.theme_h = self.r.randint(0, 360)
        self.is_dark_bg = (self.major_type in ['D', 'J']) or (self.r.random() > 0.7)
        
        if self.is_dark_bg:
            self.bg_color = f"hsl({self.theme_h}, 25%, 8%)"
            self.text_color = "#ffffff"
            self.primary_color = f"hsl({self.theme_h}, 100%, 75%)"
            self.accent_color = f"hsl({(self.theme_h + 180) % 360}, 100%, 70%)"
        else:
            self.bg_color = "#ffffff"
            self.text_color = "#111111"
            self.primary_color = f"hsl({self.theme_h}, 100%, 28%)"
            self.accent_color = f"hsl({(self.theme_h + 180) % 360}, 100%, 35%)"
            
        self.btn_shadow = f"0 {self.r.randint(4, 12)}px {self.r.randint(10, 25)}px rgba(0,0,0,0.12)"
        self.has_sidebar = (self.skeleton_id in [1, 9, 10, 15, 20])
        self.has_widgets = (self.skeleton_id in [2, 10, 16, 21])
        self.is_minimal = (self.skeleton_id in [3, 6, 8, 11, 14, 19])
        self.is_feed = (self.skeleton_id in [5, 13, 17, 22])
        self.is_dashboard = (self.skeleton_id in [7, 18, 23, 24])

        default_keys = [v[0] for v in CPA_DATA.values()] + ["데이터 분석", "기술 표준", "시스템 가이드"]
        self.target_keyword = self.r.choice(default_keys)
        self.niche_key = "universal"
        
        k_val = request.args.get('k', '')
        if k_val in CPA_DATA:
            self.target_keyword = CPA_DATA[k_val][0]
            category = CPA_DATA[k_val][4] if len(CPA_DATA[k_val]) > 4 else "universal"
            self.niche_key = "universal" # Simplified pool check

        self.company_name = self._gen_company_name()
        
        self.lego_blocks = [
            "본 시방서는 2026년 개정된 {KEY} 표준 공법을 준수하여 작성되었습니다.",
            "유체 역학적 부하 계산 데이터는 ISO-9001 기준을 {NUM}% 상회하는 정밀도를 보입니다.",
            "현장에서 수집된 {NUM_BIG}건의 샘플 데이터를 기반으로 최적화된 결과값입니다.",
            "이에 따라 본 문서는 단순한 참고용 자료가 아니며, 실제 시공 및 감리 과정에서 법적 효력을 갖는 기술 증빙 자료로 활용될 수 있습니다.",
            "모든 데이터는 AES-256 암호화 프로토콜을 통해 보호되며, 무단 복제 시 산업기술보호법에 의거하여 처벌받을 수 있습니다.",
            "정밀 안전 진단 결과 부적합 판정 시 즉시 가동을 중단하고 {KEY} 전담 팀에게 리포트해야 합니다."
        ]

    def gen_lego_text(self, count=3):
        selected = self.r.sample(self.lego_blocks, min(count, len(self.lego_blocks)))
        result = []
        for sent in selected:
            s = sent.replace("{KEY}", self.target_keyword)
            s = s.replace("{NUM}", str(self.r.randint(1, 99)))
            s = s.replace("{NUM_BIG}", str(self.r.randint(1000, 9999)))
            result.append(s)
        return " ".join(result)

    def _gen_company_name(self):
        p = ["국제", "미래", "에이스", "다이나믹", "스마트", "비전", "중앙", "한국", "글로벌"]
        b = ["기술", "산업", "정보", "안전", "환경", "데이터", "시스템"]
        s = ["연구소", "센터", "아카이브", "네트웍스", "허브"]
        return f"{self.r.choice(p)}{self.r.choice(b)} {self.target_keyword} {self.r.choice(s)}"

    def gen_chart(self, chart_type='bar'):
        col = [self.primary_color, self.accent_color, "#4caf50", "#2196f3"]
        items = "".join([f'<div style="margin-bottom:8px;"><div style="background:{self.r.choice(col)}; width:{self.r.randint(40,95)}%; height:10px; border-radius:5px;"></div></div>' for _ in range(4)])
        return f'<div style="padding:15px; background:#eee; border-radius:10px;">{items}</div>'

    def get_data(self, count=10):
        docs = []
        for i in range(count):
            title = f"2026 {self.target_keyword} 기술 표준 시방서 V{self.r.randint(1,9)}.0"
            doc_id = f"GENESIS-{self.r.randint(1000,9999)}-{i}"
            snippet = f"{self.target_keyword} 분야 연구 데이터 무결성 검증 자료입니다."
            docs.append({"title": title, "doc_id": doc_id, "snippet": snippet, "date": "2026.01.20"})
        return docs

def block_header(ge):
    bg = ge.primary_color if not ge.is_dark_bg else "#222"
    txt = "#fff"
    k_param = f"&k={request.args.get('k','')}" if request.args.get('k') else ""
    links = [
        f'<a href="/?bypass=showmethemoney{k_param}" style="color:inherit; text-decoration:none; margin:0 10px;">{ge.nav["home"]}</a>',
        f'<a href="/about?bypass=showmethemoney{k_param}" style="color:inherit; text-decoration:none; margin:0 10px;">{ge.nav["about"]}</a>',
        f'<a href="/archive?bypass=showmethemoney{k_param}" style="color:inherit; text-decoration:none; margin:0 10px;">{ge.nav["archive"]}</a>'
    ]
    return f'''
    <header style="background:{bg}; color:{txt}; padding:15px 5%; border-bottom:1px solid rgba(0,0,0,0.1); position:sticky; top:0; z-index:1000;">
        <div style="display:flex; justify-content:space-between; align-items:center; max-width:1200px; margin:0 auto;">
            <b style="font-size:1.2rem;">{ge.company_name}</b>
            <nav style="font-size:13px; font-weight:bold;">{" ".join(links)}</nav>
        </div>
    </header>
    '''

def block_hero(ge):
    return f'''
    <section style="background:linear-gradient(135deg, {ge.primary_color}, {ge.accent_color}); color:#fff; padding:100px 5%; text-align:center;">
        <h1 style="font-size:3rem; margin:0;">{ge.target_keyword} 기술 아카이브</h1>
        <p style="font-size:1.2rem; margin:30px auto; max-width:700px; opacity:0.9;">국가 표준 가이드라인에 따른 {ge.target_keyword} 분야 연구 데이터 통합 센터입니다.</p>
        <div style="margin-top:40px;">
            <a href="/archive?bypass=showmethemoney&k={request.args.get('k','')}" style="background:#fff; color:#111; padding:15px 30px; border-radius:10px; font-weight:bold; text-decoration:none;">자료실 입장</a>
        </div>
    </section>
    '''

def block_home_overview(ge):
    docs = ge.get_data(3)
    items = "".join([f'<div style="padding:20px; border:1px solid #eee; border-radius:10px; margin-bottom:15px;"><h4>{d["title"]}</h4><p style="font-size:14px; opacity:0.7;">{d["snippet"]}</p></div>' for d in docs])
    return f'<section style="padding:60px 5%; max-width:1200px; margin:0 auto;"><h3>최신 기술 업데이트</h3>{items}</section>'

def block_footer(ge):
    return f'''
    <footer style="padding:60px 5%; background:#f8fafc; border-top:1px solid #eee; text-align:center; font-size:13px; opacity:0.6;">
        <b>{ge.company_name}</b><br>
        COPYRIGHT (C) 2026 {ge.company_name.upper()}. ALL RIGHTS RESERVED.
    </footer>
    '''

def render_page(ge, content_blocks, title_suffix=""):
    page_title = f"{ge.target_keyword} {title_suffix or '국가 표준 기술 아카이브'}"
    css = f"""<style>
        body {{ margin:0; font-family:sans-serif; background:{ge.bg_color}; color:{ge.text_color}; }}
        section {{ padding: 60px 5%; }}
        h1, h2, h3 {{ color: {ge.primary_color}; }}
    </style>"""
    body = f'{block_header(ge)}<main>{" ".join(content_blocks)}</main>{block_footer(ge)}'
    return f"<!DOCTYPE html><html lang='ko'><head><meta charset='utf-8'><title>{page_title}</title>{css}</head><body>{body}</body></html>"

# ==================================================================================
# [MASTER CONTROLLER]
# ==================================================================================

def is_bot(user_agent):
    if not user_agent: return False
    # Refined list to allow Naver/Google App users but block crawlers
    bots = ['bot', 'crawl', 'slurp', 'spider', 'naverbot', 'yeti', 'googlebot', 'lighthouse', 'preview', 'capture']
    ua = user_agent.lower()
    return any(bot in ua for bot in bots)

@app.route('/api/track')
def track_click():
    target_url = request.args.get('url', 'https://replyalba.co.kr')
    name = request.args.get('name', '업체')
    cat = request.args.get('cat', '일반')
    region = request.args.get('region', '전국')
    client_ip = request.headers.get('CF-Connecting-IP', request.headers.get('X-Forwarded-For', request.remote_addr))
    
    # [V12.1] Country Info via Cloudflare Header
    country_code = request.headers.get('CF-IPCountry', 'Unknown').upper()
    country_map = {'KR': '대한민국', 'US': '미국', 'JP': '일본', 'CN': '중국', 'HK': '홍콩', 'TW': '대만', 'VN': '베트남', 'TH': '태국', 'PH': '필리핀', 'SG': '싱가포르', 'GB': '영국', 'CA': '캐나다', 'AU': '호주'}
    country_name = country_map.get(country_code, country_code)
    
    # Send conversion notification to Telegram
    try:
        msg = (f"🎯 [상담 전환 발생]\n"
               f"업체: {name}\n"
               f"업종: {cat}\n"
               f"지역: {region}\n"
               f"국가: {country_name}\n"
               f"IP: {client_ip}\n"
               f"🔗 이동: {target_url}")
        requests.get(f"https://api.telegram.org/bot7983385122:AAGK4kjCDpmerqfSwQL66ZDPL2MSOEV4An0/sendMessage", 
                     params={"chat_id": "1898653696", "text": msg}, timeout=2)
    except:
        pass
        
    return redirect(target_url)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy_master_final(path):
    try:
        user_agent = request.headers.get('User-Agent', '')

        client_ip = request.headers.get('CF-Connecting-IP', request.headers.get('X-Forwarded-For', request.remote_addr))
        country_code = request.headers.get('CF-IPCountry', 'Unknown').upper()
        country_map = {'KR': '대한민국', 'US': '미국', 'JP': '일본', 'CN': '중국', 'HK': '홍콩', 'TW': '대만', 'VN': '베트남', 'TH': '태국', 'PH': '필리핀', 'SG': '싱가포르', 'GB': '영국', 'CA': '캐나다', 'AU': '호주'}
        country_name = country_map.get(country_code, country_code)
        
        k = request.args.get('k', '')
        t = request.args.get('t', 'A').upper()
        referer = request.headers.get('Referer', '직접 유입(Direct)')
        
        # [1. IDENTITY & BOT DETECTION]
        ge = GeneEngine(request.host)
        is_bot_user = is_bot(user_agent)
        is_admin_preview = (request.args.get('bypass') == 'showmethemoney')

        # [2. TELEGRAM ALERTS] - Full Restore
        try:
            report_msg = ""
            if is_bot_user and not is_admin_preview:
                bot_name = "봇(Bot)"
                if 'naver' in user_agent.lower() or 'yeti' in user_agent.lower(): bot_name = "네이버 봇"
                elif 'google' in user_agent.lower(): bot_name = "구글 봇"
                
                report_msg = (f"🤖 [{bot_name} 유입]\n"
                              f"📍 경로: {request.url}\n"
                              f"🔗 유입처: {referer}\n"
                              f"🌍 국가: {country_name}\n"
                              f"🌍 IP: {client_ip}\n"
                              f"📝 주제: {ge.target_keyword}\n"
                              f"👁️ 가면: {request.base_url}?k={k}&t={t}&bypass=showmethemoney")
            elif k and not is_bot_user and not is_admin_preview:
                if k in CPA_DATA:
                    kr_keyword = CPA_DATA[k][0]
                    vendor = CPA_DATA[k][3] if len(CPA_DATA[k]) > 3 else "알 수 없음"
                    report_msg = (f"💰 [실제 손님 유입]\n"
                                  f"키워드: {kr_keyword}\n"
                                  f"업체: {vendor}({t})\n"
                                  f"🔗 유입처: {referer}\n"
                                  f"국가: {country_name}\n"
                                  f"IP: {client_ip}\n"
                                  f"👁️ 가짜사이트: {request.base_url}?k={k}&t={t}&bypass=showmethemoney")
            
            if report_msg:
                requests.get(f"https://api.telegram.org/bot7983385122:AAGK4kjCDpmerqfSwQL66ZDPL2MSOEV4An0/sendMessage", 
                             params={"chat_id": "1898653696", "text": report_msg}, timeout=2)
        except: pass

        # [3. CLOAKING MODE (Bots or Admin Preview)]
        if is_bot_user or is_admin_preview:
            clean_path = path.lower().strip('/')
            if not clean_path or clean_path == "":
                content = [block_hero(ge), block_home_overview(ge)]
            elif clean_path == "about":
                content = [f"<section><h1>{ge.nav['about']}</h1><p>{ge.gen_lego_text(5)}</p></section>"]
            elif clean_path == "archive":
                docs = "".join([f"<li>{d['title']}</li>" for d in ge.get_data(10)])
                content = [f"<section><h1>{ge.nav['archive']}</h1><ul>{docs}</ul></section>"]
            else:
                content = [block_hero(ge), block_home_overview(ge)]
            
            return render_page(ge, content), 200

        # [4. REVENUE MODE (Humans)]
        if k and k in CPA_DATA:
            try:
                file_path = os.path.join(os.getcwd(), 'comparison_test.html')
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Dynamic Data Injection
                    db_keyword = CPA_DATA[k][0] if len(CPA_DATA[k]) > 0 else ""
                    db_category = CPA_DATA[k][4] if len(CPA_DATA[k]) > 4 else ""
                    cat_map = {"이사": "moving", "청소": "cleaning", "누수/설비": "leak", "배관/누수": "leak", "배관": "leak", "하수구": "leak", "하수구뚫음": "leak", "철거": "demolition", "plumbing": "leak", "faucet": "faucet"}
                    fe_category = cat_map.get(db_category, db_category)
                    
                    # [V11.9] Keyword Override: '수전', '변기', '세면대'가 포함된 키워드는 수전 카테고리로 강제 전환
                    if any(kw in db_keyword for kw in ["수전", "변기", "세면대"]) and fe_category == "leak":
                        fe_category = "faucet"
                    
                    all_companies = {}
                    for cat_name, companies in ALL_COMPANIES.items():
                        cat_slug = cat_map.get(cat_name, cat_name)
                        if cat_slug not in all_companies: all_companies[cat_slug] = []
                        for p in companies:
                            base_url = p["url_a"] if t != 'B' else (p["url_b"] or p["url_a"])
                            track = p["track_a"] if t != 'B' else (p["track_b"] or p["track_a"])
                            
                            # Intelligent URL handling: If URL already contains '/pt/' or is a full landing page, use as-is.
                            if '/pt/' in base_url or '?' in base_url or '.html' in base_url:
                                final_url = base_url
                            else:
                                final_url = f"{base_url.rstrip('/')}/pt/{track}"

                            all_companies[cat_slug].append({
                                "name": p["name"],
                                "url": final_url,
                                "rating": "4.8", "reviews": "500+", "desc1": "실시간 견적", "desc2": "전문 상담사 배정"
                            })


                    injected_data = {"category": fe_category, "region": "", "allCompanies": all_companies}
                    content = content.replace("<head>", f"<head><script>window.InjectedData = {json.dumps(injected_data, ensure_ascii=False)};</script>")
                    return content, 200

            except: pass

        # Fallback to direct redirect or base facade
        if k and k in CPA_DATA:
            cpa_info = CPA_DATA[k]
            base = cpa_info[5] if (t != 'B' and len(cpa_info) > 5) else (cpa_info[6] if len(cpa_info) > 6 else "https://replyalba.co.kr")
            code = cpa_info[1 if t != 'B' else 2]
            return redirect(f"{base}/pt/{code}")

        return render_page(ge, [block_hero(ge), block_home_overview(ge)]), 200

    except Exception as e:
        return "Internal Proxy Error", 500

if __name__ == "__main__": 
    app.run(host='0.0.0.0', port=5000, debug=True)
