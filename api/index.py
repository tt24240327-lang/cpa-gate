import requests, hashlib, time, json, re, random, base64
import traceback
from flask import Flask, request, Response, redirect, render_template_string, make_response

# Robust Import
try:
    from genesis_db import GENESIS_DATABASE
except ImportError:
    try:
        from api.genesis_db import GENESIS_DATABASE
    except ImportError:
        GENESIS_DATABASE = {"error": {"title": "Error", "fragments": ["Database not found"]}}

app = Flask(__name__)

# [v100.Global] EMPIRE GENESIS-AI: Multi-Layout Logic
TELEGRAM_TOKEN = "7983385122:AAGK4kjCDpmerqfSwQL66ZDPL2MSOEV4An0"
CHAT_ID = "1898653696"

# 🛡️ [CORE PRESERVED: Data & Security]
G_GUARDIAN = {}
G_JAIL = set()

CPA_DATA = {
    # Cleaning (Index 1: A-Code[ReplyAlba], Index 2: B-Code[AlbaRich])
    "8cf12edf": ["이사청소", "WwVCgW9E1R", "z2NytCt42i"], "ca4a68a6": ["사무실청소", "WwVCgW9E1R", "z2NytCt42i"],
    "c8a4cf5a": ["입주청소", "WwVCgW9E1R", "z2NytCt42i"], "d7ea613c": ["집청소", "WwVCgW9E1R", "z2NytCt42i"],
    "cb845113": ["청소업체", "WwVCgW9E1R", "z2NytCt42i"],
    
    # Moving (Index 1: A-Code[ReplyAlba], Index 2: B-Code[AlbaRich])
    "faf45575": ["이사", "LlocSbdUSY", "zdIDBDSzof"], "ce8a5ce4": ["포장이사", "LlocSbdUSY", "zdIDBDSzof"],
    "c8b22f8a": ["이사업체", "LlocSbdUSY", "zdIDBDSzof"], "d108d7a5": ["사무실이사", "LlocSbdUSY", "zdIDBDSzof"],
    "f79702a3": ["이사견적", "LlocSbdUSY", "zdIDBDSzof"], "fa13bc33": ["원룸이사", "LlocSbdUSY", "zdIDBDSzof"],
    "eeaf8186": ["용달이사", "LlocSbdUSY", "zdIDBDSzof"],
    
    # Plumbing (Index 1: A-Code[ReplyAlba], Index 2: B-Code[AlbaRich])
    "8e2996c7": ["배관 누수", "GkVRvxfx1T", "QOaojnBV2v"], "81edc02c": ["변기막힘", "GkVRvxfx1T", "QOaojnBV2v"],
    "8745563e": ["하수구막힘", "GkVRvxfx1T", "QOaojnBV2v"], "617a0005": ["누수탐지", "GkVRvxfx1T", "QOaojnBV2v"],
    "5d19986d": ["변기뚫는업체", "GkVRvxfx1T", "QOaojnBV2v"], "a0ef0c00": ["싱크대막힘", "GkVRvxfx1T", "QOaojnBV2v"],
    "e6d02452": ["배수구 막힘", "GkVRvxfx1T", "QOaojnBV2v"], "35467a5c": ["하수구 역류", "GkVRvxfx1T", "QOaojnBV2v"],
    "9ce613e1": ["변기 물 안 내려감", "GkVRvxfx1T", "QOaojnBV2v"], "68943f44": ["하수구 뚫는 업체", "GkVRvxfx1T", "QOaojnBV2v"],
    "c8abc514": ["변기 뚫는 곳", "GkVRvxfx1T", "QOaojnBV2v"],
    
    # Fixtures (Index 1: A-Code[ReplyAlba], Index 2: B-Code[AlbaRich])
    "ffbfdc28": ["변기수전", "FzYOdTzVNw", "vRUcqPts9r"], "be4adb64": ["수전교체", "FzYOdTzVNw", "vRUcqPts9r"],
    "a01f1db0": ["변기교체", "FzYOdTzVNw", "vRUcqPts9r"], "b1585a85": ["화장실 변기 교체", "FzYOdTzVNw", "vRUcqPts9r"],
    "c2bddbcc": ["세면대 교체", "FzYOdTzVNw", "vRUcqPts9r"], "b6f6c35f": ["변기업체", "FzYOdTzVNw", "vRUcqPts9r"],
    "3e750243": ["수전업체", "FzYOdTzVNw", "vRUcqPts9r"],
    
    # Welding (Index 1: A-Code[ReplyAlba], Index 2: B-Code[AlbaRich])
    "dc19f4ea": ["용접", "XpBx9dZ5aE", "SROHH97olh"], "af5f2375": ["출장용접", "XpBx9dZ5aE", "SROHH97olh"],
    "c4c5ee7e": ["용접업체", "XpBx9dZ5aE", "SROHH97olh"], "4a2f6816": ["배관용접", "XpBx9dZ5aE", "SROHH97olh"],
    "87a3472b": ["알곤용접", "XpBx9dZ5aE", "SROHH97olh"], "63b2da0a": ["용접수리", "XpBx9dZ5aE", "SROHH97olh"],
    "20186798": ["알곤출장용접", "XpBx9dZ5aE", "SROHH97olh"], "ef310430": ["스텐 출장용접", "XpBx9dZ5aE", "SROHH97olh"]
}

TARGET_A = "https://replyalba.co.kr"
TARGET_B = "https://albarich.com"
BOT_SIGS = ['naver', 'yeti', 'bot', 'crawl', 'google', 'spider', 'ahrefs', 'bing']
FORBIDDEN_PATHS = ['admin', '.env', 'wp-login', 'config', 'shell', 'backup']
REGIONS = ['us-east-1', 'ap-northeast-2', 'eu-west-1', 'sa-east-1', 'ap-southeast-1']

class GeneEngine:
    def __init__(self, seed_str):
        self.r = random.Random(int(hashlib.md5(seed_str.encode()).hexdigest(), 16))
        self.lib = list(GENESIS_DATABASE.keys())
        self.niche = self.r.choice(self.lib)
        
        # [Layout & Style Mutation]
        self.layout_type = self.r.choice(['A', 'B', 'C', 'D'])
        self.theme_color = self.r.choice([
            "#003366", "#1a2a6c", "#0d324d", # Corporate Blue
            "#16a085", "#27ae60", # Reliable Green
            "#c0392b", "#8e44ad", # Strong Points
            "#2c3e50" # Dark
        ])
    
    def get_bloat(self, count=40):
        try:
            pool = GENESIS_DATABASE[self.niche]["fragments"]
            return " ".join([self.r.choice(pool) for _ in range(count)])
        except: return "System initializing..."

    def get_backlinks(self):
        links = []
        for _ in range(self.r.randint(3, 6)):
            t_node = f"node-{self.r.randint(100, 999)}.standard-eco.life"
            links.append(f"<a href='#' style='color:inherit;text-decoration:none;opacity:0.5;'>[Ref: {t_node}]</a>")
        return " | ".join(links)

    def get_favicon_url(self):
        shape = self.r.choice(['rect', 'circle', 'poly', 'diamond'])
        svg = f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'>"
        if shape == 'rect':
            svg += f"<rect x='4' y='4' width='56' height='56' rx='{self.r.randint(0,16)}' fill='{self.theme_color}'/>"
        elif shape == 'circle':
            svg += f"<circle cx='32' cy='32' r='28' fill='{self.theme_color}'/>"
        elif shape == 'poly':
            svg += f"<polygon points='32,4 60,56 4,56' fill='{self.theme_color}'/>"
        elif shape == 'diamond':
             svg += f"<polygon points='32,4 60,32 32,60 4,32' fill='{self.theme_color}'/>"
        
        if self.r.choice([True, False]):
             char = self.niche[0].upper()
             svg += f"<text x='50%' y='50%' dy='.35em' font-family='sans-serif' font-weight='bold' font-size='32' fill='white' text-anchor='middle'>{char}</text>"
             
        svg += "</svg>"
        return f"data:image/svg+xml;base64,{base64.b64encode(svg.encode()).decode()}"

# [CORE PRESERVED: Inquiry Form]
def get_inquiry_form():
    return """
    <div class="inquiry-box" style="margin-top:40px; padding:30px; background:rgba(0,0,0,0.03); border:1px solid #ddd; border-radius:8px;">
        <h3 style="margin-top:0;">🚀 전문가 기술 상담 / 견적 요청</h3>
        <p>본 연구소의 기술 제휴, 데이터 사용, 시스템 구축 관련 문의를 남겨주세요.</p>
        <form action="/api/capture" method="POST">
            <input type="text" name="name" placeholder="담당자 성함 / 기업명" style="width:100%; padding:10px; margin-bottom:10px; border:1px solid #ccc; box-sizing:border-box;" required>
            <input type="text" name="contact" placeholder="연락처 (이메일 또는 전화번호)" style="width:100%; padding:10px; margin-bottom:10px; border:1px solid #ccc; box-sizing:border-box;" required>
            <textarea name="content" placeholder="문의 내용 (예: API 연동 견적 요청합니다)" style="width:100%; padding:10px; height:80px; margin-bottom:10px; border:1px solid #ccc; box-sizing:border-box;" required></textarea>
            <button type="submit" style="background:#333; color:#fff; padding:12px 24px; border:none; cursor:pointer; font-weight:bold;">문의 접수하기</button>
        </form>
    </div>
    """

def render_layout(ge, pr, dna):
    layout = ge.layout_type
    
    # Common Components
    # [Staff Login Button Injection]
    staff_btn_text = pr.choice(['Staff', 'Admin', 'Intranet', 'Partner'])
    staff_btn_icon = pr.choice(['🔒', '🔑', '🛡️', '⚙️'])
    staff_btn_style = pr.choice([
        f"color:{ge.theme_color}; border:1px solid {ge.theme_color}; padding:5px 10px; border-radius:4px;", # Bordered
        "color:#555; font-size:12px; opacity:0.7;", # Subtle Text
        f"background:{ge.theme_color}; color:#fff; padding:5px 12px; border-radius:20px; font-size:11px;" # Pill
    ])
    
    staff_btn_html = f"""<a href="#" onclick="alert('🚫 ACCESS DENIED\\n\\n관계자 외 접근이 제한된 구역입니다.\\n(Authorized Personnel Only)'); return false;" style="margin-left:20px; text-decoration:none; cursor:pointer; {staff_btn_style}">{staff_btn_icon} {staff_btn_text}</a>"""
    
    # Random Position Injection
    if pr.random() > 0.5:
        nav = f"""<nav>
            <a href='/?bot=1'>HOME</a>
            <a href='/network?bot=1'>NETWORK</a>
            <a href='/security?bot=1'>SECURITY</a>
            <a href='/data?bot=1'>DATA</a>
            <a href='/support?bot=1'>SUPPORT</a>
            {staff_btn_html}
        </nav>"""
    else:
         nav = f"""<nav>
            {staff_btn_html}
            <a href='/?bot=1'>HOME</a>
            <a href='/network?bot=1'>NETWORK</a>
            <a href='/security?bot=1'>SECURITY</a>
            <a href='/data?bot=1'>DATA</a>
            <a href='/support?bot=1'>SUPPORT</a>
        </nav>"""
    

    
    if layout == 'A': # Enterprise
        html = f"""
        <header style="background:#fff; border-bottom:4px solid {ge.theme_color}; padding:20px 10%; display:flex; justify-content:space-between; align-items:center;">
            <h1 onclick="location.href='/?bot=1'" style="color:{ge.theme_color}; margin:0; cursor:pointer;">{dna['company']}</h1>
            {nav}
        </header>
        <div style="background:{ge.theme_color}; color:#fff; padding:80px 10%; text-align:center;">
            <h2 style="font-size:40px; margin:0;">Global Tech Leadership</h2>
            <p style="opacity:0.8;">{dna['title']} Solutions</p>
        </div>
        <div style="display:grid; grid-template-columns:2fr 1fr; gap:40px; padding:60px 10%; max-width:1200px; margin:0 auto;">
            <main>
                {dna['page_content']}
            </main>
            <aside>
                <div style="background:#f9f9f9; padding:20px; margin-bottom:20px;">
                    <h4>Recent News</h4>
                    <ul style="padding-left:20px; font-size:14px; color:#555;">
                        <li><a href="/network?bot=1" style="text-decoration:none; color:inherit;">System Update: v3.2 Released</a></li>
                        <li><a href="/data?bot=1" style="text-decoration:none; color:inherit;">Security Patch: applied for {ge.niche}</a></li>
                        <li><a href="/support?bot=1" style="text-decoration:none; color:inherit;">Global Partnership Announcement</a></li>
                    </ul>
                </div>
                <div style="background:#f9f9f9; padding:20px;">
                    <h4>Contact</h4>
                    <p style="font-size:13px;">Seoul, Korea<br>Tel: 02-{pr.randint(100,999)}-{pr.randint(1000,9999)}</p>
                </div>
            </aside>
        </div>
        """
    
    elif layout == 'B': # Portal
        html = f"""
        <header style="background:#f5f5f5; padding:15px 5%; border-bottom:1px solid #ddd; display:flex; align-items:center;">
            <strong onclick="location.href='/?bot=1'" style="font-size:20px; margin-right:40px; cursor:pointer;">{dna['company']}</strong>
            {nav}
        </header>
        <div style="display:flex; max-width:1400px; margin:0 auto; min-height:800px;">
            <div style="width:250px; background:#fff; border-right:1px solid #eee; padding:30px 20px;">
                <h4 style="color:{ge.theme_color};">MENU</h4>
                <ul style="list-style:none; padding:0; line-height:2.5;">
                    <li><a href="/network?bot=1" style="color:#555; text-decoration:none;"> > 공지사항</a></li>
                    <li><a href="/data?bot=1" style="color:#555; text-decoration:none;"> > 자료실</a></li>
                    <li><a href="/support?bot=1" style="color:#555; text-decoration:none;"> > API 문서</a></li>
                    <li><a href="/security?bot=1" style="color:#555; text-decoration:none;"> > 보안 정책</a></li>
                </ul>
            </div>
            <div style="flex:1; padding:40px;">
                <h2 style="border-bottom:2px solid {ge.theme_color}; padding-bottom:10px; color:{ge.theme_color};">{dna['title']}</h2>
                {dna['page_content']}
            </div>
        </div>
        """
        
    elif layout == 'D': # Dashboard (Dark)
        html = f"""
        <style>body {{ background: #111; color: #ddd; }} .card {{ background: #222; border: 1px solid #444; }} input, textarea {{ background: #333; color: #fff; border: 1px solid #555; }}</style>
        <header style="background:#000; padding:20px 40px; border-bottom:1px solid #333; display:flex; justify-content:space-between;">
            <div onclick="location.href='/?bot=1'" style="color:{ge.theme_color}; font-weight:bold; font-family:monospace; font-size:24px; cursor:pointer;">{dna['company']} [OPS]</div>
            <div style="font-family:monospace; color:{ge.theme_color};">{nav}</div>
        </header>
        <div style="padding:40px; font-family:monospace;">
            <div style="border:1px solid {ge.theme_color}; color:{ge.theme_color}; padding:20px; margin-bottom:30px;">
                [SYSTEM STATUS] ONLINE | SECURE | ENCRYPTED
            </div>
            {dna['page_content']}
        </div>
        """
        
    else: # Type C (Startup) - Default
        html = f"""
        <header style="padding:20px 5%; display:flex; justify-content:space-between; align-items:center; position:sticky; top:0; background:rgba(255,255,255,0.95); backdrop-filter:blur(10px); z-index:99; box-shadow:0 2px 10px rgba(0,0,0,0.05);">
            <div onclick="location.href='/?bot=1'" style="font-weight:900; font-size:22px; color:{ge.theme_color}; cursor:pointer;">{dna['company']}</div>
            {nav}
        </header>
        <div style="text-align:center; padding:100px 20px; background:linear-gradient(to bottom, #fff, #f4f4f4);">
            <h1 style="font-size:48px; margin-bottom:20px; color:#333;">{dna['title']}</h1>
            <p style="font-size:18px; color:#666; max-width:600px; margin:0 auto 40px;">{ge.get_bloat(15)}</p>
            <button onclick="location.href='/data?bot=1'" style="background:{ge.theme_color}; color:#fff; padding:15px 40px; font-size:18px; border:none; border-radius:30px; cursor:pointer;">Get Started</button>
        </div>
        <div style="max-width:1000px; margin:0 auto; padding:60px 20px;">
            {dna['page_content']}
        </div>
        """
        
    # Wrap in common HTML structure
    full_html = f"""
    <!DOCTYPE html><html lang='ko'><head><meta charset='UTF-8'><link rel="icon" href="{ge.get_favicon_url()}" type="image/svg+xml"><title>{dna['title']} | {dna['company']}</title>
    <style>
        body{{margin:0; font-family:'Segoe UI', Roboto, sans-serif; line-height:1.6;}}
        nav a{{margin-left:20px; text-decoration:none; color:inherit; font-weight:bold; font-size:14px;}}
        .t{{opacity:0.001; position:absolute;}}
    </style></head><body>
    {html}
    <footer style="padding:60px 10%; text-align:center; font-size:13px; opacity:0.7;">
        {dna['footer_info']}<br>
        <div style="margin-top:20px;">{dna['backlinks']}</div>
        <a href="/api/secure/verify" class="t">.</a>
    </footer>
    </body></html>
    """
    return full_html


def render_genesis_imperial(host, k_val, path, info=""):
    try:
        # 1. Initialize Engine with Seed (Domain Name Only for Consistency)
        # e.g. www.link-us.shop -> link-us
        clean_host = host.replace("www.", "").split('.')[0]
        ge = GeneEngine(clean_host)
        pr = random.Random(int(hashlib.md5(clean_host.encode()).hexdigest(), 16))
        
        path_clean = path.lower().strip('/')
        title_main = GENESIS_DATABASE[ge.niche].get("title", "지능형 관제 시스템")
        
        # 2. Content Generation Logic
        if "network" in path_clean:
            page_content = f"""
            <h3>Network Optimization</h3>
            <p>{ge.get_bloat(30)}</p>
            <div style="background:#eee; padding:15px; border-radius:4px; margin:20px 0; font-family:monospace;">
                > Tracing route to node-{pr.randint(10,99)}...<br>
                > {pr.randint(10,50)}ms latency verified.<br>
                > Packet loss: 0%
            </div>
            """
        elif "security" in path_clean:
             page_content = f"""
            <h3>Security Protocols</h3>
            <p>{ge.get_bloat(30)}</p>
            <ul>
                <li>Firewall Status: <span style="color:green">ACTIVE</span></li>
                <li>Encryption: AES-256</li>
                <li>Last Audit: {pr.randint(2024,2025)}-{pr.randint(1,12)}-{pr.randint(1,28)}</li>
            </ul>
            """
        elif "data" in path_clean:
             if "dac-" in path_clean:
                 # Detail View
                 f_id = "DAC-" + str(pr.randint(1000,9999)) + "-" + pr.choice(['A','B','C'])
                 parts = path_clean.split('/')
                 for p in parts:
                     if "dac-" in p: f_id = p.upper()
                 
                 page_content = f"""
                 <h3>Data Detail View</h3>
                 <div style="border:1px solid #ddd; padding:30px; border-radius:8px; box-shadow:0 2px 15px rgba(0,0,0,0.05);">
                    <div style="border-bottom:2px solid {ge.theme_color}; padding-bottom:15px; margin-bottom:20px; display:flex; justify-content:space-between; align-items:center;">
                        <h2 style="margin:0; color:{ge.theme_color};">{f_id}</h2>
                        <span style="background:#eee; padding:5px 10px; border-radius:4px; font-size:12px;">CONFIDENTIAL</span>
                    </div>
                    <table style="width:100%; border-collapse:collapse; margin-bottom:30px;">
                        <tr><th style="text-align:left; padding:15px; border-bottom:1px solid #eee; width:150px;">File Name</th><td style="padding:15px; border-bottom:1px solid #eee;">{ge.niche.upper()} Analysis Data v{pr.randint(3,9)}.0</td></tr>
                        <tr><th style="text-align:left; padding:15px; border-bottom:1px solid #eee;">File Size</th><td style="padding:15px; border-bottom:1px solid #eee;">{pr.randint(100,5000)} MB</td></tr>
                        <tr><th style="text-align:left; padding:15px; border-bottom:1px solid #eee;">Data Type</th><td style="padding:15px; border-bottom:1px solid #eee;">Raw Sensor Data / Logs</td></tr>
                        <tr><th style="text-align:left; padding:15px; border-bottom:1px solid #eee;">Encryption</th><td style="padding:15px; border-bottom:1px solid #eee;">AES-256 (GCM Mode)</td></tr>
                        <tr><th style="text-align:left; padding:15px; border-bottom:1px solid #eee;">Access Level</th><td style="padding:15px; border-bottom:1px solid #eee; color:red;">Level 3 (Restricted)</td></tr>
                    </table>
                    <div style="display:flex; gap:10px;">
                        <button onclick="alert('보안 등급이 부족합니다.\\n담당자에게 접근 권한을 요청하세요.'); location.href='/support?bot=1'" style="background:{ge.theme_color}; color:#fff; padding:12px 25px; border:none; border-radius:4px; cursor:pointer; font-weight:bold;">Download Encrypted File</button>
                        <button onclick="history.back()" style="background:#fff; color:#555; border:1px solid #ddd; padding:12px 25px; border-radius:4px; cursor:pointer;">Go Back</button>
                    </div>
                 </div>
                 """
             else:
                 # List View
                 data_list = []
                 for i in range(1, 16):
                     f_id_raw = f"DAC-{pr.randint(1000,9999)}-{chr(pr.randint(65,90))}"
                     # [Time Logic: Late 2025 ~ Early 2026]
                     if pr.random() > 0.3:
                         f_year = 2026
                         f_month = pr.randint(1, 1) # Jan 2026
                     else:
                         f_year = 2025
                         f_month = pr.randint(10, 12) # Oct-Dec 2025
                     f_day = pr.randint(1, 28)
                     f_date = f"{f_year}-{f_month:02d}-{f_day:02d}"
                     
                     f_size = f"{pr.randint(1, 900)}.{pr.randint(10,99)} MB"
                     f_type = pr.choice(['PDF', 'XLSX', 'CSV', 'ZIP', 'JSON'])
                     f_stat = pr.choice(['<span style="color:green">Available</span>', '<span style="color:red">Restricted</span>', 'Archived'])
                     fname = f"{ge.niche.upper()} Analysis Data v{pr.randint(1,9)}.{i}"
                     
                     data_list.append({
                         "id": f_id_raw, "date": f_date, "size": f_size,
                         "type": f_type, "stat": f_stat, "name": fname,
                         "sort_key": f_year * 10000 + f_month * 100 + f_day
                     })

                 # Sort by Date Descending (Latest First)
                 data_list.sort(key=lambda x: x['sort_key'], reverse=True)

                 rows = ""
                 for item in data_list:
                     rows += f"""
                     <tr style="border-bottom:1px solid #eee; cursor:pointer; transition:background 0.2s;" onmouseover="this.style.background='#f5f5f5'" onmouseout="this.style.background='transparent'" onclick="location.href='/data/{item['id']}?bot=1'">
                        <td style="padding:12px; color:{ge.theme_color}; font-weight:bold;">{item['id']}</td>
                        <td style="padding:12px; text-decoration:underline;">{item['name']}</td>
                        <td style="padding:12px;">{item['type']}</td>
                        <td style="padding:12px;">{item['size']}</td>
                        <td style="padding:12px;">{item['date']}</td>
                        <td style="padding:12px;">{item['stat']}</td>
                     </tr>
                     """
                 
                 page_content = f"""
                 <h3>Data Warehouse</h3>
                 <p>Access authorized research data and technical specifications.</p>
                 <div style="overflow-x:auto;">
                    <table style="width:100%; border-collapse:collapse; font-size:14px;">
                        <thead style="background:#f9f9f9; border-bottom:2px solid {ge.theme_color};">
                            <tr>
                                <th style="padding:12px; text-align:left;">ID</th>
                                <th style="padding:12px; text-align:left;">File Name</th>
                                <th style="padding:12px; text-align:left;">Type</th>
                                <th style="padding:12px; text-align:left;">Size</th>
                                <th style="padding:12px; text-align:left;">Date</th>
                                <th style="padding:12px; text-align:left;">Status</th>
                            </tr>
                        </thead>
                        <tbody>{rows}</tbody>
                    </table>
                 </div>
                 <div style="margin-top:20px; text-align:center;">
                    <span style="cursor:pointer; padding:5px 10px; border:1px solid #ddd; margin:2px;">&lt;</span>
                    <span style="font-weight:bold; padding:5px 10px; background:{ge.theme_color}; color:#fff; margin:2px;">1</span>
                    <span style="cursor:pointer; padding:5px 10px; border:1px solid #ddd; margin:2px;">2</span>
                    <span style="cursor:pointer; padding:5px 10px; border:1px solid #ddd; margin:2px;">3</span>
                    <span style="cursor:pointer; padding:5px 10px; border:1px solid #ddd; margin:2px;">...</span>
                    <span style="cursor:pointer; padding:5px 10px; border:1px solid #ddd; margin:2px;">{pr.randint(50,100)}</span>
                    <span style="cursor:pointer; padding:5px 10px; border:1px solid #ddd; margin:2px;">&gt;</span>
                 </div>
                 """
        elif "support" in path_clean:
             page_content = f"<h3>Technical Support Center</h3><p>{ge.get_bloat(40)}</p>" + get_inquiry_form()
        else: # Home
            page_content = f"""
            <h3>System Dashboard</h3>
            <p>{ge.get_bloat(20)}</p>
            <div style="display:flex; gap:20px; margin-top:30px; flex-wrap:wrap;">
                <div style="flex:1; border:1px solid #ddd; padding:20px; border-radius:8px;">
                    <strong>CPU Load</strong><br><span style="font-size:24px; color:{ge.theme_color}">{pr.randint(10,40)}%</span>
                </div>
                <div style="flex:1; border:1px solid #ddd; padding:20px; border-radius:8px;">
                    <strong>Active Nodes</strong><br><span style="font-size:24px; color:{ge.theme_color}">{pr.randint(500,1000)}</span>
                </div>
                <div style="flex:1; border:1px solid #ddd; padding:20px; border-radius:8px;">
                    <strong>Requests/s</strong><br><span style="font-size:24px; color:{ge.theme_color}">{pr.randint(8000,12000)}</span>
                </div>
            </div>
            <div style="text-align:center; margin-top:40px;">
                <button onclick="location.href='/support?bot=1'" style="background:{ge.theme_color}; color:#fff; padding:15px 30px; border:none; border-radius:5px; font-size:16px; cursor:pointer; font-weight:bold;">
                    전문가 상담 / 견적 요청 &gt;
                </button>
            </div>
            """

        # 3. DNA Assembly
        dna = {
            "title": title_main,
            "company": f"{title_main.replace(' ','')} 기술연구센터",
            "page_content": page_content,
            "footer_info": f"대표: {pr.choice(['김','이','박','정','최'])}철수 | 사업자: {pr.randint(100,999)}-{pr.randint(10,99)}",
            "backlinks": ge.get_backlinks()
        }

        # 4. Render with Multi-Layout Engine
        return render_layout(ge, pr, dna)

    except Exception as e:
        return f"<h1>SYSTEM ERROR</h1><pre>{traceback.format_exc()}</pre>"

def send_telegram(msg):
    try: requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg, "disable_web_page_preview": True}, timeout=10)
    except: pass

@app.route('/api/secure/verify')
def honey_pot_trap():
    ua, ip = request.headers.get('User-Agent', '').lower(), request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    f_print = hashlib.md5(f"{ip}-{ua}".encode()).hexdigest()[:12]
    G_JAIL.add(f_print)
    send_telegram(f"🚨 [격퇴] {f_print} (허니팟 접속 시도 차단)")
    return redirect(f"/?bot=1")

@app.route('/api/capture', methods=['POST', 'GET'])
def capture_and_success():
    data = request.form.to_dict() or request.args.to_dict(); send_telegram(f"🚨 [문의 접수!] {data.get('name')}\n{data.get('content')}"); return "<h1>Data Transmitted</h1><script>alert('접수가 완료되었습니다.'); location.href='/';</script>"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy_master_final(path):
    try:
        ua, host = request.headers.get('User-Agent', '').lower(), request.host
        ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
        # [CORE PRESERVED: Fingerprint Logic]
        f_print = hashlib.md5(f"{ip}-{ua}".encode()).hexdigest()[:12]
        
        pr = random.Random(int(hashlib.md5(f"{host}".encode()).hexdigest(), 16))
        time.sleep(pr.uniform(0.1, 0.6))

        # [CORE PRESERVED: Jail Check]
        if f_print in G_JAIL:
            return render_genesis_imperial(host, None, path, "SOVEREIGN_JAIL_ACTIVE")
        if any(p in path.lower() for p in FORBIDDEN_PATHS):
            G_JAIL.add(f_print)
            send_telegram(f"🚨 [격퇴] Forbidden Path: {path} (IP: {ip} 차단됨)")
            return render_genesis_imperial(host, None, path, "JAIL_LOCKED")

        # [CORE PRESERVED: CPA Session Logic]
        k = request.args.get('k', request.cookies.get('cpa_session', G_GUARDIAN.get(f_print)))
        is_bot = any(sig in ua for sig in BOT_SIGS) or request.args.get('bot') == '1'
        
        if k and k in CPA_DATA and not is_bot:
            G_GUARDIAN[f_print] = k

        # [BOT OR DIRECT ACCESS -> GENESIS AI]
        if is_bot or not k:
            html = render_genesis_imperial(host, k, path)
            resp = make_response(html)
            resp.headers['X-Genesis-Node'] = f"node-{pr.randint(1000, 9999)}"
            return resp

        # [REAL USER -> TARGET CPA SITE]

        is_static = any(path.lower().endswith(ext) for ext in ['.svg', '.png', '.css', '.js', '.ico'])
        if (path == "" or "intro" in path.lower()) and not is_static:
            kw = CPA_DATA.get(k, ["미등록", ""])[0]
            
            # Device Detection
            device = "📱 Mobile" if "mobile" in ua else "💻 PC"
            if "android" in ua: device += " (Android)"
            elif "iphone" in ua: device += " (iOS)"
            elif "windows" in ua: device += " (Win)"
            
            # Domain Info
            domain_clean = host.replace("www.", "")
            
            # One-Line Notification
            msg = f"💰 [{kw}] � {ip} | {device} | 🔗 {domain_clean}"
            send_telegram(msg)

        # [Dual Target Routing]
        t_param = request.args.get('t', 'A')
        
        # Determine Base Target and Code Index
        if t_param == 'B':
            base_target = TARGET_B
            code_idx = 2 # Use B-Code
        else:
            base_target = TARGET_A
            code_idx = 1 # Use A-Code

        target_url = f"{base_target}/pt/{CPA_DATA[k][code_idx]}" if k in CPA_DATA and not path else f"{base_target}/{path}" if path else f"{base_target}/pt/z2NytCt42i"
        
        t_resp = requests.get(target_url, params=request.args, headers={'User-Agent': request.headers.get('User-Agent'), 'Referer': base_target}, timeout=12)
        f_resp = make_response()
        if "text/html" in t_resp.headers.get("Content-Type", ""):
            html = re.sub(r'(src|href|action)="/', f'\\1="{base_target}/', t_resp.text)
            # html = re.sub(r'<form([^>]*)action="[^"]*"', r'<form\1action="/api/capture" method="POST"', html) # [Direct Pass-through]
            f_resp.set_data(html)
        else:
            f_resp.set_data(t_resp.content)
        f_resp.headers["Content-Type"] = t_resp.headers.get("Content-Type")
        f_resp.set_cookie('cpa_session', k or '', max_age=86400, httponly=True)
        return f_resp

    except Exception as e:
        return f"<h1>EMPIRE_SYSTEM_STABLE</h1><p>Syncing... Debug: {str(e)}</p>"

if __name__ == "__main__": app.run()
