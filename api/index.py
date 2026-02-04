# ==================================================================================
# 🚨 [HYPER-LEGO ASSEMBLY ENGINE v9] 🚨
# 25 ARCHETYPES | INFINITE COMBINATIONS | HIGH DATA DENSITY
# ==================================================================================
import hashlib, time, random, base64, requests
from flask import Flask, request, redirect, make_response
from urllib.parse import urlencode

# Robust Import or Mock
try:
    from genesis_db import GENESIS_DATABASE
except ImportError:
    try:
        from api.genesis_db import GENESIS_DATABASE
    except ImportError:
        GENESIS_DATABASE = {}

# [Safety Patch] Ensure Universal Key Exists
if "universal" not in GENESIS_DATABASE:
    GENESIS_DATABASE["universal"] = {"title": "System", "fragments": [
        "시스템이 정상 가동 중입니다.", "노드 동기화가 완료되었습니다.", "프로토콜 검증 성공.", 
        "암호화 연결이 수립되었습니다.", "응답 지연이 최소화되었습니다.",
        "데이터 무결성이 확인되었습니다.", "백업이 규정을 준수합니다.", "접근이 승인되었습니다."
    ]}

# CPA REVENUE ENGINE CONFIG (V2.6)
SALT = "yejin_love_2026"
KEYWORD_MAP = {
    "moving": "이사업체", "pack-moving": "포장이사", "office-moving": "사무실이사", 
    "move-est": "이사견적", "clean-move": "이사청소", "clean-home": "입주청소",
    "welding": "용접", "leak": "누수탐지", "loan": "개인회생", "interior": "인테리어"
}

# SECRET LEDGER: Hash <-> Keyword <-> Target Codes (V4.4 Force-Sync)
CPA_DATA = {
    # --- 이사 관련 (이사방 / 모두이사) ---
    "c8b22f8a": ["이사업체", "LlocSbdUSY", "zdIDBDSzof"],
    "d108d7a5": ["사무실이사", "LlocSbdUSY", "zdIDBDSzof"],
    "f79702a3": ["이사견적", "LlocSbdUSY", "zdIDBDSzof"],
    "fa13bc33": ["원룸이사", "LlocSbdUSY", "zdIDBDSzof"],
    "eeaf8186": ["용달이사", "LlocSbdUSY", "zdIDBDSzof"],
    "faf45575": ["이사", "LlocSbdUSY", "zdIDBDSzof"],
    "ce8a5ce4": ["포장이사", "LlocSbdUSY", "zdIDBDSzof"],

    # --- 청소 관련 (모두클린 / 이사방) ---
    "8cf12edf": ["이사청소", "WwVCgW9E1R", "z2NytCt42i"],
    "ca4a68a6": ["사무실청소", "WwVCgW9E1R", "z2NytCt42i"],
    "c8a4cf5a": ["입주청소", "WwVCgW9E1R", "z2NytCt42i"],
    "d7ea613c": ["집청소", "WwVCgW9E1R", "z2NytCt42i"],
    "cb845113": ["청소업체", "WwVCgW9E1R", "z2NytCt42i"],

    # --- 누수/배관/변기 관련 (모두클린 / 이사방) ---
    "8e2996c7": ["배관 누수", "WwVCgW9E1R", "z2NytCt42i"],
    "81edc02c": ["변기막힘", "WwVCgW9E1R", "z2NytCt42i"],
    "8745563e": ["하수구막힘", "WwVCgW9E1R", "z2NytCt42i"],
    "617a0005": ["누수탐지", "WwVCgW9E1R", "z2NytCt42i"],
    "5d19986d": ["변기뚫는업체", "WwVCgW9E1R", "z2NytCt42i"],
    "a0ef0c00": ["싱크대막힘", "WwVCgW9E1R", "z2NytCt42i"],
    "e6d02452": ["배수구 막힘", "WwVCgW9E1R", "z2NytCt42i"],
    "35467a5c": ["하수구 역류", "WwVCgW9E1R", "z2NytCt42i"],
    "9ce613e1": ["변기 물 안 내려감", "WwVCgW9E1R", "z2NytCt42i"],
    "68943f44": ["하수구 뚫는 업체", "WwVCgW9E1R", "z2NytCt42i"],
    "c8abc514": ["변기 뚫는 곳", "WwVCgW9E1R", "z2NytCt42i"],
    "ffbfdc28": ["변기수전", "WwVCgW9E1R", "z2NytCt42i"],
    "be4adb64": ["수전교체", "WwVCgW9E1R", "z2NytCt42i"],
    "a01f1db0": ["변기교체", "WwVCgW9E1R", "z2NytCt42i"],
    "b1585a85": ["화장실 변기 교체", "WwVCgW9E1R", "z2NytCt42i"],
    "c2bddbcc": ["세면대 교체", "WwVCgW9E1R", "z2NytCt42i"],
    "b6f6c35f": ["변기업체", "WwVCgW9E1R", "z2NytCt42i"],
    "3e750243": ["수전업체", "WwVCgW9E1R", "z2NytCt42i"],

    # --- 용접 관련 (모두클린 / 이사방) ---
    "dc19f4ea": ["용접", "WwVCgW9E1R", "z2NytCt42i"],
    "af5f2375": ["출장용접", "WwVCgW9E1R", "z2NytCt42i"],
    "c4c5ee7e": ["용접업체", "WwVCgW9E1R", "z2NytCt42i"],
    "4a2f6816": ["배관용접", "WwVCgW9E1R", "z2NytCt42i"],
    "87a3472b": ["알곤용접", "WwVCgW9E1R", "z2NytCt42i"],
    "63b2da0a": ["용접수리", "WwVCgW9E1R", "z2NytCt42i"],
    "20186798": ["알곤출장용접", "WwVCgW9E1R", "z2NytCt42i"],
    "ef310430": ["스텐 출장용접", "WwVCgW9E1R", "z2NytCt42i"]
}

app = Flask(__name__)

# [SEO AUTOMATION V5.0 - DYNAMIC ROBOTS & SITEMAP]
# ==================================================================================
@app.route('/robots.txt')
def robots():
    """Generates dynamic robots.txt for ANY subdomain."""
    host = request.host
    content = f"User-agent: *\nAllow: /\nSitemap: https://{host}/sitemap.xml"
    response = make_response(content)
    response.headers["Content-Type"] = "text/plain"
    return response

@app.route('/sitemap.xml')
def sitemap():
    """Generates dynamic sitemap.xml with strategic keyword injection."""
    host = request.host
    scheme = "https"
    base_url = f"{scheme}://{host}"
    
    # 1. XML Header
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    # 2. Main Page priority
    xml.append(f'<url><loc>{base_url}/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>')
    
    # 3. Dynamic Service Pages (Derived from Keyword Map)
    # Generate ~50 strategic URLs based on KEYWORD_MAP keys to look rich
    for key in KEYWORD_MAP.keys():
        slug = f"service-{key}-{hashlib.md5(key.encode()).hexdigest()[:4]}"
        xml.append(f'<url><loc>{base_url}/{slug}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>')
        
    # 4. Randomized Archive Pages (To simulate depth)
    # Using deterministic seeds based on host to keep sitemap stable per domain
    local_seed = int(hashlib.md5(host.encode()).hexdigest(), 16)
    random.seed(local_seed)
    
    for i in range(1, 21): # 20 Archive pages
        archive_id = random.randint(1000, 9999)
        xml.append(f'<url><loc>{base_url}/archive/doc-{archive_id}</loc><changefreq>monthly</changefreq><priority>0.6</priority></url>')

    xml.append('</urlset>')
    
    response = make_response("".join(xml))
    response.headers["Content-Type"] = "application/xml"
    return response
# ==================================================================================

def _get_cpa_encoded_code(keyword):
    """Implementing the MD5 encoding logic with fixed salt as per the Master Spec."""
    import hashlib
    combined = (keyword + SALT).encode('utf-8')
    return hashlib.md5(combined).hexdigest()[:8]

DOMAIN_POOL = [
    "logistics-dynamics.kr", "polymer-cleaning.co.kr", "net-scan.cloud", "data-archive.info",
    "tech-vault.org", "research-hub.io", "protocol-link.net", "system-core.biz",
    "infra-maintenance.kr", "fluid-flow.xyz", "standard-eco.life", "system-gate.xyz"
]

TARGET_A = "https://replyalba.co.kr"
TARGET_B = "https://albarich.com"

# [V4.29] Hybrid Security & Analytics Constants
# ==================================================================================
FORBIDDEN_PATHS = ['wp-admin', 'wp-login', '.env', 'setup-config', 'xmlrpc', 'install.php', 'config.php']
G_JAIL = set()  # In-Memory Jail (Reset on restart is fine for now)

# GA4 Configuration (Values placeholders, user needs to update if changed)
GA_MEASUREMENT_ID = "G-XXXXXXXXXX" 
GA_API_SECRET = "XXXXXXXXXX"

class GeneEngine:
    def __init__(self, seed_str):
        if request.args.get('auto_random'): seed_str = str(time.time())
        test_seed = request.args.get('test_seed')
        if test_seed: seed_str = test_seed
        self.raw_seed = seed_str
        self.r = random.Random(seed_str)
        
        # 1. Archetype Matrix & Structural Skeleton (V4.25)
        # 10 Main Genres -> 30 Sub Genres Matrix
        self.main_types = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        self.major_type = self.r.choice(self.main_types)
        self.sub_type = self.r.randint(1, 3) # 10x3 = 30 Themes
        self.layout_id = f"{self.major_type}-{self.sub_type}"
        
        # [V4.25] Extreme Structural Skeletons (1-24)
        self.skeleton_id = self.r.randint(1, 24)
        if request.args.get('test_skel'): self.skeleton_id = int(request.args.get('test_skel'))
        
        # [V4.25] Diverse Archive Styles (1-10)
        self.archive_style = self.r.randint(1, 10)
        if request.args.get('archive_style'): self.archive_style = int(request.args.get('archive_style'))
        
        # 2. Navigation Shuffler
        self.menu_pool = {
            "home": ["MAIN", "HUB", "LOBBY", "DASHBOARD", "종합현황", "HOME", "START"],
            "about": ["STORY", "PROFILE", "VISION", "센터소개", "인사말", "걸어온길", "ABOUT"],
            "archive": ["DATA", "GUIDE", "REFERENCE", "자료실", "기술문서", "정보센터", "ARCHIVE"],
            "service": ["FIELD", "PROJECT", "WORK", "주요업무", "전문분야", "지원영역", "BUSINESS"],
            "contact": ["Q&A", "FORUM", "HELP", "ASK", "통합민원", "문의", "고객센터"]
        }
        self.nav = {k: self.r.choice(v) for k, v in self.menu_pool.items()}
        
        # 3. CSS DNA & Contrast Engine
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
            
        # [Design Matrix Hints V4.21]
        self.btn_radius = {"A": "4px", "B": "0px", "C": "40px", "D": "0px", "F": "20px", "G": "2px", "H": "0px"}.get(self.major_type, f"{self.r.randint(0, 15)}px")
        self.btn_shadow = f"0 {self.r.randint(4, 12)}px {self.r.randint(10, 25)}px rgba(0,0,0,0.12)"
        
        # [V4.25] Layout Engine Logic
        self.has_sidebar = (self.skeleton_id in [1, 9, 10, 15, 20])
        self.has_widgets = (self.skeleton_id in [2, 10, 16, 21])
        self.is_minimal = (self.skeleton_id in [3, 6, 8, 11, 14, 19])
        self.is_feed = (self.skeleton_id in [5, 13, 17, 22])
        self.is_dashboard = (self.skeleton_id in [7, 18, 23, 24])
        
        self.layout_hint = {"B": "portal", "H": "gallery", "I": "shop", "E": "wiki", "D": "hacker"}.get(self.major_type, "standard")
        if self.major_type == 'D' and self.sub_type == 1: self.layout_hint = "hacker_terminal"
        
        # [CONTEXT INJECTION V4.12 - NEUTRAL AUTHORITY]
        # Randomize default keyword for site-wide diversity even without 'k'
        default_keys = [v[0] for v in CPA_DATA.values()] + ["데이터 분석", "기술 표준", "시스템 가이드"]
        self.target_keyword = self.r.choice(default_keys)
        self.niche_key = "universal"
        
        # 4. Hash Override (Reverse Lookup for Revenue Links)
        k_val = request.args.get('k', '')
        if k_val in CPA_DATA:
            self.target_keyword = CPA_DATA[k_val][0]
            if any(x in self.target_keyword for x in ["이사"]): self.niche_key = "moving"
            elif any(x in self.target_keyword for x in ["청소", "막힘", "누수"]): self.niche_key = "cleaning"
            elif any(x in self.target_keyword for x in ["용접"]): self.niche_key = "plumbing"
        
        # 5. Identity & SEO (Global Standard)
        self.company_name = self._gen_company_name()
        self.seo_keywords = [v[0] for v in CPA_DATA.values()]

        # [V4.26] Infinite Lego Text Engine (Combinatorics)
        # 100+ Professional Sentence Fragments
        self.lego_blocks = [
            "본 시방서는 2026년 개정된 {KEY} 표준 공법을 준수하여 작성되었습니다.",
            "유체 역학적 부하 계산 데이터는 ISO-9001 기준을 {NUM}% 상회하는 정밀도를 보입니다.",
            "현장에서 수집된 {NUM_BIG}건의 샘플 데이터를 기반으로 최적화된 결과값입니다.",
            "이에 따라 본 문서는 단순한 참고용 자료가 아니며, 실제 시공 및 감리 과정에서 법적 효력을 갖는 기술 증빙 자료로 활용될 수 있습니다.",
            "모든 데이터는 AES-256 암호화 프로토콜을 통해 보호되며, 무단 복제 시 산업기술보호법에 의거하여 처벌받을 수 있습니다.",
            "정밀 안전 진단 결과 부적합 판정 시 즉시 가동을 중단하고 {KEY} 전담 팀에게 리포트해야 합니다.",
            "데이터 노드의 동기화 지연율은 0.{NUM}ms 미만으로 유지되어야 하며, 이를 초과할 경우 시스템 경보가 발령됩니다.",
            "사용자 환경에 따른 가변적 부하 테스트를 {NUM}회 이상 실시하였으며 무결성이 검증되었습니다.",
            "해당 공정은 KSC-{NUM_BIG} 표준에 의거하여 설계되었으며, 환경 영향 평가에서 적합 판정을 받았습니다.",
            "실시간 모니터링 시스템은 24시간 {KEY} 데이터 흐름을 감시하며, 이상 징후 발생 시 자동 제어 로직이 가동됩니다.",
            "본 보고서에 포함된 수치 데이터는 국제 {KEY} 협회의 인증을 받은 계측 장비로 측정되었습니다.",
            "작업 전 안전 수칙 준수 여부를 {NUM}단계로 점검하고, 관리 감독자의 서명을 득해야 합니다.",
            "폐기물 처리 절차는 환경부 고시 제{YEAR}-{NUM}호를 엄격히 따르고 있습니다.",
            "설비의 내구 연한은 {NUM}년으로 설계되었으며, 정기적인 유지 보수를 통해 연장 가능합니다.",
            "비상 사태 발생 시 {KEY} 대응 매뉴얼 Level-{NUM}에 따라 즉각적인 조치를 취해야 합니다.",
            "고객의 개인 정보는 {KEY} 보안 서버에 암호화되어 저장되며, 보존 기간 경과 후 자동 파기됩니다.",
            "서비스 품질 향상을 위해 {KEY} 관련 빅데이터 분석 알고리즘이 실시간으로 적용됩니다.",
            "네트워크 대역폭 최적화를 통해 {KEY} 데이터 전송 속도를 기존 대비 {NUM}% 향상시켰습니다.",
            "클라우드 기반의 {KEY} 협업 플랫폼을 통해 언제 어디서나 안전하게 데이터에 접근할 수 있습니다.",
            "AI 기반의 {KEY} 예측 모델은 9{NUM}.{NUM}% 의 정확도로 미래 수요를 예측합니다."
        ]


        
        # 6. Niche Templates (Technical Blocks - V4.14 Expanded)
        self.niche_templates = {
            "cleaning": [
                "살균 소독 적합성 판정 데이터 세트", "피톤치드 휘발성 유기화합물 도표 분석", "배관 내시경 정밀 판독 결과 보고서", 
                "초고압 세척 노즐 압력 평형 지표", "정화 프로세스 ISO-2026 규정 승인", "박테리아 억제 농도 시계열 분석",
                "수질 오염도 자동 감지 노드 동기화", "미세 먼지 포집 필터 무결성 검증", "친환경 약제 반응성 메타 리포트",
                "정밀 클리닝 로봇 궤적 최적화 로그"
            ],
            "moving": [
                "물품 하중 밸런싱 알고리즘 시뮬레이션", "운송 트래픽 실시간 최적화 리포트", "포장 자재 내충격성 실험 데이터", 
                "적재 공간 기하학적 배치 분석서", "충격 흡수 서스펜션 로그 지표", "ISO-2026 표준 운송 매뉴얼 준수율",
                "물류 노드 동적 할당 결과 보고서", "진동 감쇄 장치 정밀 측정 시방서", "운행 경로 탄소 배출량 저감 지표",
                "중량물 이동 경로 안정성 시각화 데이터"
            ],
            "plumbing": [
                "압계 정밀 측정 및 압력 강하 분석", "수압 테스트 구간별 유량 동기화", "관로 통수 주파수 스캔 분석", 
                "누수 탐지 초음파 감도 보정 리포트", "관로 내부 산화 스트레스 지수 측정", "통수 저항 계수 정밀 계산서",
                "비파괴 검사(NDT) 초음파 이미지 로그", "배관 내부 조도 및 거칠기 측정 지표", "유체 역학 기반 압력 손실 모델링",
                "정렬 밸브 개폐 압력 임계값 리포트"
            ],
            "universal": [
                "데이터 암호화 저장 및 무결성 확인", "표준 운영 매뉴얼 V5.12 준수 가이드", "인프라 보안 프로토콜 기술 지표", 
                "시스템 응답 지연 시간 시계열 분석", "노드 간 트래픽 밸런싱 실시간 지표", "클라우드 스토리지 리팩토링 결과서",
                "네트워크 패킷 손실률 감리 보고서", "서버 과부하 방지 임계치 설정 로그", "API 응답 코드 필터링 무결성 검증",
                "글로벌 표준 기술 문서 관리 규정"
            ]
        }

    def gen_lego_text(self, count=5):
        # [Combinatorics] Pick random blocks and shuffle
        selected = self.r.sample(self.lego_blocks, min(count, len(self.lego_blocks)))
        
        # [Variable Injection] Replace {KEY}, {NUM}, {YEAR} with dynamic values
        result = []
        for sent in selected:
            s = sent.replace("{KEY}", self.target_keyword)
            s = s.replace("{NUM}", str(self.r.randint(1, 99)))
            s = s.replace("{NUM_BIG}", str(self.r.randint(1000, 9999)))
            s = s.replace("{YEAR}", str(self.r.randint(2024, 2026)))
            result.append(s)
            
        return " ".join(result)

    def _gen_company_name(self):
        p = ["국제", "미래", "에이스", "다이나믹", "스마트", "비전", "중앙", "한국", "글로벌", "디지털", "통합", "기술"]
        b = ["기술", "산업", "정보", "안전", "환경", "공학", "데이터", "시스템", "솔루션"]
        s = ["연구소", "센터", "아카이브", "재단", "본부", "네트웍스", "허브", "뱅크"]
        # Randomly decide to add {target_keyword} to the name for authority
        if self.r.random() > 0.5:
            return f"{self.r.choice(p)}{self.r.choice(b)} {self.target_keyword} {self.r.choice(s)}"
        return f"{self.r.choice(p)}{self.r.choice(b)} {self.r.choice(s)}"

    def filter_commercial(self, text):
        for w in ["견적", "비용", "가격", "요금", "결제", "상담신청", "￦", "원"]:
            text = text.replace(w, "자료")
        return text

    def gen_chart(self, chart_type='bar'):
        col = [self.primary_color, self.accent_color, "#4caf50", "#2196f3"]
        if chart_type == 'bar':
            items = "".join([f'<div style="margin-bottom:8px;"><div style="background:{self.r.choice(col)}; width:{self.r.randint(40,95)}%; height:10px; border-radius:5px;"></div></div>' for _ in range(4)])
            return f'<div style="padding:15px; background:#eee; border-radius:10px;">{items}</div>'
        return ""

    def gen_class(self, base):
        # [V4.25] DNA Obfuscation: Generate unique class names per site
        sig = hashlib.md5(f"{self.raw_seed}_{base}".encode()).hexdigest()[:4]
        return f"{base}-{sig}"

    def gen_id(self, base):
        sig = hashlib.md5(f"{self.raw_seed}_{base}_{self.r.random()}".encode()).hexdigest()[:8]
        return f"{base}-{sig}"

    def get_data(self, count=20):
        pool = self.niche_templates.get(self.niche_key, self.niche_templates["universal"])
        docs = []
        titles = [
            f"표준 {self.target_keyword} 기술 시방서 V{self.r.randint(1,9)}.0",
            f"{self.target_keyword} 안전 가이드라인 (2026)",
            f"{self.target_keyword} 데이터 무결성 리포트",
            f"차세대 {self.target_keyword} 인프라 분석서",
            f"글로벌 {self.target_keyword} 벤치마킹 데이터",
            f"{self.target_keyword} 시뮬레이션 결과 보고서",
            f"{self.target_keyword} 정밀 감리 일지",
            f"{self.target_keyword} 공정 프로토콜 설계도",
            f"{self.target_keyword} 표준화 데이터 통계 연보",
            f"{self.target_keyword} 유지보수 정밀 매뉴얼",
            f"{self.target_keyword} 성능 지표 측점 데이터",
            f"{self.target_keyword} 시스템 설계 및 구축 보고서",
            f"{self.target_keyword} 기술 표준원 권고 사항",
            f"{self.target_keyword} 인프라 최적화 백서",
            f"{self.target_keyword} 운영 효율성 분석 결과",
            f"{self.target_keyword} 관련 법적 규제 준수 리포트"
        ]
        for i in range(count):
            title = self.r.choice(titles) if i > 0 else f"2026 {self.target_keyword} 기술 핵심 시방서"
            doc_id = f"GENESIS-{self.r.randint(1000,9999)}-{i}"
            frag = self.r.choice(pool)
            docs.append({"title": title, "doc_id": doc_id, "snippet": frag, "date": f"2026.01.{self.r.randint(10,30)}"})
        return docs

# ==================================================================================
# [THE LEGO BLOCK LIBRARY]
# ==================================================================================

def block_header(ge):
    h_type = ge.r.choice(['top', 'side', 'minimal'])
    bg = ge.primary_color if not ge.is_dark_bg else "#222"
    txt = "#fff"
    
    k_param = f"&k={request.args.get('k','')}" if request.args.get('k') else ""
    links = [
        f'<a href="/?bypass=1{k_param}" style="color:inherit; text-decoration:none;">{ge.nav["home"]}</a>',
        f'<a href="/about?bypass=1{k_param}" style="color:inherit; text-decoration:none;">{ge.nav["about"]}</a>',
        f'<a href="/archive?bypass=1{k_param}" style="color:inherit; text-decoration:none;">{ge.nav["archive"]}</a>',
        f'<a href="/service?bypass=1{k_param}" style="color:inherit; text-decoration:none;">{ge.nav["service"]}</a>',
        f'<a href="/contact?bypass=1{k_param}" style="color:inherit; text-decoration:none;">{ge.nav["contact"]}</a>'
    ]
    
    if ge.skeleton_id in [1, 9, 10]: # [SIDEBAR Skeletons]
        width = "280px" if ge.skeleton_id != 9 else "220px"
        return f'''
        <aside class="sidebar" style="width:{width}; height:100vh; position:fixed; left:0; top:0; background:{bg}; color:{txt}; padding:50px 30px; z-index:1000; border-right:1px solid rgba(255,255,255,0.1); display:flex; flex-direction:column;">
            <div style="font-size:24px; font-weight:900; line-height:1.2; margin-bottom:60px;">{ge.company_name}</div>
            <nav style="display:flex; flex-direction:column; gap:20px; font-size:15px; font-weight:bold;">
                { "".join([l.replace('color:inherit', f'color:{txt}') for l in links]) }
            </nav>
            <div style="margin-top:auto; font-size:11px; opacity:0.5;">
                { f'TREE_ID: {ge.r.randint(100,999)}<br>' if ge.skeleton_id == 9 else '' }
                STATUS: <span style="color:#0f0;">ONLINE</span><br>
                SEC_LEVEL: AA+
            </div>
        </aside>
        '''
    
    # [Arch 2, 3, 4, 5, 6, 7, 8, 11, 12: Top Menu or Hidden]
    if ge.skeleton_id == 8: return "" # [Arch 8: No Header for Infinite Grid]
    
    max_w = "1200px"
    if ge.skeleton_id == 3: max_w = "800px"
    if ge.skeleton_id == 6: max_w = "1000px"
    if ge.skeleton_id == 12: max_w = "1400px"
    
    return f'''
    <header style="background:{bg}; color:{txt}; padding:15px 5%; border-bottom:1px solid rgba(0,0,0,0.1); position:sticky; top:0; z-index:1000;">
        <div style="display:flex; justify-content:space-between; align-items:center; max-width:{max_w}; margin:0 auto; flex-wrap:wrap; gap:10px;">
            <b style="font-size:1.2rem; white-space:nowrap;">{ge.company_name}</b>
            <nav style="display:flex; gap:15px; font-size:13px; font-weight:bold; flex-wrap:wrap; justify-content:center;">{" ".join(links)}</nav>
        </div>
    </header>
    '''

def block_breadcrumbs(ge, current_name):
    return f'''
    <div style="padding:20px 5%; font-size:12px; opacity:0.6; max-width:1200px; margin:0 auto; display:flex; gap:10px;">
        <a href="/?bypass=1" style="color:inherit; font-weight:normal;">🏠 {ge.nav["home"]}</a> 
        <span>&rsaquo;</span> 
        <a href="/archive?bypass=1" style="color:inherit; font-weight:normal;">📂 {ge.nav["archive"]}</a> 
        <span>&rsaquo;</span> 
        <span style="color:{ge.primary_color}; font-weight:bold;">{ge.target_keyword} {current_name}</span>
    </div>
    '''

def block_hero(ge):
    if ge.skeleton_id in [3, 5, 6]: return "" # [V4.24: Hide Hero for Feed/Minimal/Search]
    
    sub_title = f"{ge.target_keyword} 분야 기술 지표를 선도하고 실시간 데이터를 투명하게 공개하는 전문 정보 허브입니다."
    if True: 
        sub_title = f"범용 기술 가이드라인에 따른 {ge.target_keyword} 분야 연구 데이터 센터입니다."
        
    return f'''
    <section style="background:linear-gradient(135deg, {ge.primary_color}, {ge.accent_color}); color:#fff; padding:120px 5%; text-align:center;">
        <h1 style="font-size:3.5rem; margin:0; line-height:1.2; word-break:keep-all;">{ge.target_keyword}<br>디지털 기술 아카이브</h1>
        <p style="font-size:1.25rem; margin:40px auto; max-width:800px; color:#ffffff; line-height:1.8; font-weight:500;">{sub_title}</p>
        <div style="display:flex; justify-content:center; gap:20px; margin-top:40px;">
            <a href="/archive?bypass=1&k={request.args.get('k','')}" class="btn" style="background:#ffffff; color:#111111 !important; font-weight:bold; box-shadow:0 10px 20px rgba(0,0,0,0.2);">보관 자료실 입장</a>
            <a href="/about?bypass=1&k={request.args.get('k','')}" class="btn" style="background:transparent; border:2.5px solid #ffffff; color:#ffffff !important; font-weight:bold;">연구소 히스토리</a>
        </div>
    </section>
    '''

def block_footer(ge):
    return f'''
    <footer style="padding:100px 5%; background:{ge.bg_color}; border-top:1px solid rgba(0,0,0,0.1); text-align:center; font-size:14px; color:#444;">
        <b style="color:#000;">{ge.company_name}</b><br>
        본 사이트는 {ge.target_keyword} 기술 자료를 제공하는 공공 아카이브입니다.<br>
        모든 데이터는 비영리 목적으로 제공되며 상업적 재배포를 금합니다.<br>
        <div style="margin-top:20px; font-weight:bold;">COPYRIGHT (C) 2026 {ge.company_name.upper()}. ALL RIGHTS RESERVED.</div>
    </footer>
    '''

# ==================================================================================
# [ASSEMBLY ENGINE]
# ==================================================================================

def render_page(ge, content_blocks, title_suffix=""):
    # [V4.28] Fix: Define page_title to prevent NameError
    page_title = f"{ge.target_keyword} {title_suffix or '국가 표준 기술 아카이브'}"
    
    # [V4.29] SEO Enhancement: Dynamic Meta Description
    meta_desc = f"{ge.company_name}에서 제공하는 {ge.target_keyword} 분야 연구 데이터 및 실시간 기술 지표 통합 아카이브입니다. 무결성 검증을 거친 최신 표준 문서를 확인하세요."
    
    main_style = "min-height: 80vh; transition: 0.3s;"
    # [V4.25] Extreme Structural CSS
    if ge.skeleton_id in [1, 9, 10]: # Side Menu Types
        width = "280px" if ge.skeleton_id != 9 else "220px"
        main_style += f"margin-left: {width};"
    elif ge.skeleton_id in [3, 11, 12]: # Focused Content
        main_style += "max-width: 1000px; margin: 0 auto; padding-top: 50px;"
    elif ge.skeleton_id == 8: # Full Screen Grid
        main_style += "padding: 0;"
    elif ge.skeleton_id in [10, 16]: # Double Sidebar Space (Pseudo-margin)
        main_style += "margin: 0 50px;"
    
    # [Type Specific CSS Injection]
    type_css = ""
    if ge.major_type == 'D': # Dashboard
        type_css = "font-family: 'Courier New', monospace; letter-spacing:-0.5px;"
    elif ge.major_type == 'G': # Industrial
        type_css = "text-transform: uppercase; font-weight:800;"
    elif ge.major_type == 'E': # Academic
        type_css = "font-family: 'Georgia', serif; line-height:1.9;"
    elif ge.major_type == 'F': # Clinic (Mint/Clean)
        type_css = f"background: linear-gradient(to bottom, {ge.bg_color}, #e0f2f1);"
    elif ge.major_type == 'H': # Gallery/Art
        type_css = "letter-spacing: 5px; font-weight:200;"
    elif ge.major_type == 'B': # Portal
        type_css = "font-size: 15px; border-top: 5px solid " + ge.primary_color
    elif ge.major_type == 'C': # SaaS
        type_css = "font-family: 'Outfit', sans-serif; letter-spacing:-0.2px;"
    elif ge.major_type == 'I': # Shop
        type_css = "background-image: radial-gradient(#eee 1px, transparent 1px); background-size: 20px 20px;"
    
    page_title = f"{title_suffix} | {ge.company_name}" if title_suffix else ge.company_name
    emoji = ge.r.choice(["📊", "📈", "🛡️", "🏗️", "📋", "📁", "🏢", "🚛", "🧹", "🔬"])
    favicon = f'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">{emoji}</text></svg>'
    
    # [MOBILE OPTIMIZATION V5.1 - PRO UX & ACCESSIBILITY]
    # Viewport: Allow zoom for accessibility score, but set initial scale
    viewport_meta = "<meta name='viewport' content='width=device-width, initial-scale=1.0'>"
    
    css = f"""<style>
        * {{ box-sizing: border-box; -webkit-tap-highlight-color: transparent; }}
        body {{ 
            margin:0; 
            font-family:'Inter', -apple-system, system-ui, sans-serif; 
            background:{ge.bg_color}; 
            color:{ge.text_color}; 
            overflow-x:hidden; 
            line-height:1.7; 
            font-size:17px; 
            {type_css} 
        }}
        h1 {{ font-size: 2.2rem; line-height: 1.2; word-break: keep-all; }}
        h2, h3, h4 {{ color: {ge.primary_color}; margin-top:0; font-weight:900; letter-spacing:-0.5px; word-break: keep-all; }}
        
        /* Mobile-First Button Design */
        .btn {{ 
            display:block; 
            width:100%; 
            max-width:400px;
            margin: 10px auto;
            padding:18px 20px; 
            border-radius:12px; 
            box-shadow:{ge.btn_shadow}; 
            background:{ge.primary_color}; 
            color:#fff !important; 
            text-decoration:none; 
            font-weight:800; 
            font-size: 18px;
            text-align:center;
            transition:0.2s; 
            border:none; 
            cursor:pointer; 
        }}
        .btn:active {{ transform:scale(0.98); opacity:0.9; }}
        
        section {{ padding: 60px 5%; position:relative; z-index:1; border-bottom:1px solid rgba(0,0,0,0.05); }}
        
        /* Responsive Card Layout */
        .card {{ 
            background:{'rgba(255,255,255,0.06)' if ge.is_dark_bg else '#ffffff'}; 
            padding:30px; 
            border-radius:16px; 
            box-shadow:{ge.btn_shadow}; 
            border:1px solid rgba(0,0,0,0.05); 
            transition:0.3s; 
            margin-bottom: 20px;
        }}
        
        img {{ max-width: 100%; height: auto; border-radius: 12px; }}
        
        a {{ color: {ge.primary_color}; font-weight:bold; text-decoration:none; }}

        @media (max-width: 768px) {{
            /* Mobile Sidebar -> Top Block */
            .sidebar {{
                position: static !important;
                width: 100% !important;
                height: auto !important;
                padding: 30px 20px !important;
                border-right: none !important;
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }}
            .sidebar nav {{
                flex-direction: row !important;
                flex-wrap: wrap;
                gap: 15px !important;
                margin-bottom: 20px;
            }}
            .sidebar > div:last-child {{ display: none; }} /* Hide status on mobile */
            
            /* Remove Main Margin on Mobile */
            .main-content {{
                margin-left: 0 !important;
                margin-right: 0 !important;
                width: 100% !important;
            }}
        }}

        @media (min-width: 768px) {{
            body {{ font-size: 16px; }}
            .btn {{ display:inline-block; width:auto; margin:0; }}
            section {{ padding: 80px 10%; }}
        }}
    </style>"""
    
    body = f'{block_header(ge)}<main class="main-content" style="{main_style}">{" ".join(content_blocks)}</main>{block_footer(ge)}'
    filtered_body = ge.filter_commercial(body)
    
    # [V4.29 Fix] Restore missing variable
    naver_verification = '<meta name="naver-site-verification" content="b02dfbc6f1939f588601789d9cc1ea1977ce845f" />'
    
    meta_tags = f"""
        <meta charset='utf-8'>
        <meta name="description" content="{ge.filter_commercial(meta_desc)}">
        {naver_verification}
        {viewport_meta}
    """
    
    return f"<!DOCTYPE html><html lang='ko'><head>{meta_tags}<title>{ge.filter_commercial(page_title)}</title><link rel='icon' href='{favicon}'>{css}</head><body>{filtered_body}</body></html>"

def block_about(ge):
    # [Imperial About Block V4.0]
    location_text = "국가 표준 통합 데이터 허브"
    
    history_items = [
        ("2024.03", f"{ge.target_keyword} 국가 표준 시방서 초안 공포"),
        ("2025.06", "스마트 {ge.target_keyword} 통합 센터 구축"),
        ("2026.01", f"V{ge.r.randint(3,5)}.0 {ge.target_keyword} 데이터 무결성 검증 완료")
    ]
    timeline = "".join([f'<div style="margin-bottom:15px; border-left:3px solid {ge.primary_color}; padding-left:15px;"><b style="color:{ge.primary_color};">{d}</b><br><span style="font-size:14px; opacity:0.8;">{t}</span></div>' for d, t in history_items])

    return f'''
    <section>
        <div style="max-width:1200px; margin:0 auto; display:flex; gap:60px; flex-wrap:wrap; align-items:center;">
            <div style="flex:1; min-width:300px;">
                <img src="https://picsum.photos/seed/{ge.raw_seed}_about/600/400" style="width:100%; border-radius:20px; box-shadow:0 10px 30px rgba(0,0,0,0.1);">
            </div>
            <div style="flex:1; min-width:300px;">
                <div style="font-weight:bold; color:{ge.primary_color}; margin-bottom:10px;">PRO-HISTORY // DOCUMENTED</div>
                <h1 style="margin-bottom:20px;">{ge.nav["about"]}</h1>
                <p style="font-size:1.1rem; line-height:1.8; margin-bottom:40px;">{ge.company_name}은 {location_text}, {ge.target_keyword} 분야에서 발생하는 기술적 데이터를 수집/분석하여 공신력 있는 <b>기술 아카이브</b>를 구축하는 전문 기관입니다. 본 연구소는 {ge.target_keyword} 공정의 정밀도 향상을 목표로 실시간 데이터 노드를 운영하고 있습니다.</p>
                {timeline}
                <div style="margin-top:40px; border-top:1px solid rgba(0,0,0,0.1); padding-top:20px; font-style:italic; opacity:0.8;">"디지털 데이터 보존이 {ge.target_keyword} 미래의 핵심 경쟁력입니다." - 기술영업본부장 {ge.r.choice(['김', '이', '박', '최'])}철수</div>
            </div>
        </div>
    </section>
    '''

def block_archive_main(ge, page=1):
    # [Massive Archive Grid V4.17 - Pagination Support]
    items_per_page = 24
    # Ensure stable randomness for the page
    ge.r.seed(f"{ge.raw_seed}_archive_p{page}")
    docs = ge.get_data(items_per_page)
    primary = ge.primary_color
    
    grid_items = ""
    # [V4.21] Style Switching Logic
    # [V4.25] Extreme Style Switching Logic (10 Patterns)
    content_html = ""
    
    if ge.archive_style == 1: # Grid
        for d in docs:
            grid_items += f'<a href="/archive/doc-{d["doc_id"]}?bypass=1&k={request.args.get("k","")}" style="text-decoration:none; color:inherit;"><div class="card" style="padding:25px; border-top:5px solid {primary}; height:100%;"><div style="font-size:11px; opacity:0.6; margin-bottom:10px;">{d["doc_id"]}</div><h3 style="font-size:1.1rem; margin:0; line-height:1.4; height:3em; overflow:hidden;">{d["title"]}</h3><div style="font-size:13px; opacity:0.8; margin-top:15px; border-left:2px solid {primary}33; padding-left:10px; height:4.8em; overflow:hidden;">{d["snippet"]}</div></div></a>'
        content_html = f'<div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:30px;">{grid_items}</div>'

    elif ge.archive_style == 2 or ge.archive_style == 7: # Table / Spreadsheet
        rows = "".join([f'<tr style="border-bottom:1px solid #eee; cursor:pointer;" onclick="location.href=\'/archive/doc-{d["doc_id"]}?bypass=1&k={request.args.get("k","")}\'"><td style="padding:15px; opacity:0.5;">{i+1+(page-1)*24}</td><td style="padding:15px; font-weight:bold;">{d["title"]}</td><td style="padding:15px; font-family:monospace; font-size:12px;">{d["doc_id"]}</td><td style="padding:15px; font-size:12px;">{d["date"]}</td></tr>' for i, d in enumerate(docs)])
        border = "1px solid #ddd" if ge.archive_style == 7 else "none"
        content_html = f'<div class="card" style="padding:0; overflow:hidden; border:{border};"><table style="width:100%; border-collapse:collapse; text-align:left;"><thead style="background:rgba(0,0,0,0.02); border-bottom:2px solid {primary};"><tr><th style="padding:15px;">NO</th><th style="padding:15px;">TITLE</th><th style="padding:15px;">CODE</th><th style="padding:15px;">DATE</th></tr></thead><tbody>{rows}</tbody></table></div>'

    elif ge.archive_style == 3: # Strip
        for d in docs:
            grid_items += f'<a href="/archive/doc-{d["doc_id"]}?bypass=1&k={request.args.get("k","")}" style="text-decoration:none; color:inherit;"><div class="card" style="display:flex; gap:30px; padding:30px; margin-bottom:20px; align-items:center;"><div style="width:80px; height:80px; background:{primary}11; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:30px;">📄</div><div style="flex:1;"><h3 style="margin:0;">{d["title"]}</h3><p style="opacity:0.7; font-size:14px; margin:5px 0 0 0;">{d["snippet"][:100]}...</p></div></div></a>'
        content_html = f'<div>{grid_items}</div>'

    elif ge.archive_style == 4: # Compact List
        rows = "".join([f'<div style="padding:15px; border-bottom:1px solid #eee; display:flex; justify-content:space-between; align-items:center;"><a href="/archive/doc-{d["doc_id"]}?bypass=1&k={request.args.get("k","")}" style="font-size:14px; font-weight:bold;">{d["title"]}</a><span style="font-size:11px; opacity:0.4;">{d["doc_id"]}</span></div>' for d in docs])
        content_html = f'<div class="card" style="padding:20px;">{rows}</div>'

    elif ge.archive_style == 5: # Timeline
        for d in docs:
            grid_items += f'<div style="position:relative; padding-left:40px; margin-bottom:40px; border-left:2px solid {primary}22;"><div style="position:absolute; left:-11px; top:0; width:20px; height:20px; background:{primary}; border-radius:50%; border:4px solid #fff; box-shadow:0 0 10px {primary}44;"></div><div style="font-size:12px; font-weight:bold; color:{primary};">{d["date"]}</div><a href="/archive/doc-{d["doc_id"]}?bypass=1&k={request.args.get("k","")}" style="text-decoration:none; color:inherit;"><h3 style="margin:10px 0;">{d["title"]}</h3><p style="font-size:14px; opacity:0.6;">{d["snippet"]}</p></a></div>'
        content_html = f'<div style="max-width:800px; margin:0 auto;">{grid_items}</div>'

    else: # Fallback / Others (Showcase/Tiles/etc.)
        for d in docs:
            grid_items += f'<a href="/archive/doc-{d["doc_id"]}?bypass=1&k={request.args.get("k","")}" style="text-decoration:none; color:inherit;"><div class="card" style="padding:20px; text-align:center;"><div style="font-size:40px; margin-bottom:15px;">{ge.r.choice(["📑","💾","📊","🔍"])}</div><h4 style="margin:0; font-size:14px;">{d["title"][:20]}...</h4></div></a>'
        content_html = f'<div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(200px, 1fr)); gap:20px;">{grid_items}</div>'

    return f'''
    <section>
        <div style="max-width:1400px; margin:0 auto;">
            <div style="text-align:center; margin-bottom:60px;">
                <div style="display:inline-block; padding:5px 15px; background:{primary}22; color:{primary}; border-radius:50px; font-size:12px; font-weight:bold; margin-bottom:15px;">NATIONAL DATA REPOSITORY</div>
                <h1 style="margin-bottom:15px; font-size:3rem;">{ge.nav["archive"]}</h1>
                <p style="opacity:0.6; max-width:700px; margin:0 auto;">본 센터에서는 {ge.target_keyword} 관련 총 1,024건 이상의 공인 기술 시방서 및 데이터 로그를 실시간으로 아카이빙하고 있습니다. 256비트 암호화 노드를 통해 데이터 무결성을 보장합니다.</p>
            </div>
            
            {content_html}
            
            <div style="margin-top:50px; display:flex; justify-content:center; gap:10px;">
                <a href="/archive?page={max(1, page-1)}&bypass=1&k={request.args.get('k','')}" class="btn" style="padding:10px 20px; font-size:14px; background:{'rgba(0,0,0,0.1)' if page==1 else primary}; color:{'#666' if page==1 else '#fff'} !important; pointer-events:{'none' if page==1 else 'auto'};">이전 페이지</a>
                <div style="display:flex; align-items:center; padding:0 20px; font-weight:bold;">PAGE {page} / 43</div>
                <a href="/archive?page={page+1}&bypass=1&k={request.args.get('k','')}" class="btn" style="padding:10px 20px; font-size:14px;">다음 페이지</a>
            </div>

            <div style="margin-top:80px; text-align:center;">
                <div style="background:{primary}0a; padding:40px; border-radius:20px; border:1px solid {primary}11;">
                    <h3 style="margin-bottom:20px;">📦 대용량 아카이브 서버 상태</h3>
                    <div style="display:flex; justify-content:center; gap:50px; flex-wrap:wrap;">
                        <div><b style="font-size:24px; color:{primary};">{ge.r.randint(850,999)}TB</b><br><span style="font-size:12px; opacity:0.6;">전체 데이터 용량</span></div>
                        <div><b style="font-size:24px; color:{primary};">{ge.r.randint(99,100)}%</b><br><span style="font-size:12px; opacity:0.6;">데이터 무결성 지수</span></div>
                        <div><b style="font-size:24px; color:{primary};">{ge.r.randint(10,50)}ms</b><br><span style="font-size:12px; opacity:0.6;">동기화 응답 속도</span></div>
                        <div><b style="font-size:24px; color:{primary};">AES-256</b><br><span style="font-size:12px; opacity:0.6;">암호화 보안 레벨</span></div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    '''

def block_home_overview(ge):
    # [Home-Specific Spotlight V4.18]
    # Differentiated from Archive to avoid cloning feel
    ge.r.seed(f"{ge.raw_seed}_v4_home")
    latest_doc = ge.get_data(1)[0]
    samples = ge.get_data(3)
    primary = ge.primary_color
    
    sample_items = ""
    for d in samples:
        sample_items += f'''
        <a href="/archive/doc-{d['doc_id']}?bypass=1&k={request.args.get('k','')}" style="text-decoration:none; color:inherit;">
            <div class="card" style="padding:20px; border-left:4px solid {primary}; display:flex; flex-direction:column; gap:10px; background:rgba(0,0,0,0.01); height:100%;">
                <div style="font-size:10px; opacity:0.5;">DOC ID: {d["doc_id"]}</div>
                <h4 style="margin:0; font-size:1rem;">{d["title"]}</h4>
                <p style="font-size:13px; opacity:0.7; margin:0;">{d["snippet"][:60]}...</p>
                <span style="font-size:11px; margin-top:5px; color:{primary}; font-weight:bold;">상세 보기 →</span>
            </div>
        </a>
        '''

    # [Arch 5, 13, 17, 22: News Pipeline (Feed Mode)]
    if ge.is_feed:
        feed_items = "".join([f'<div style="padding:25px; border-bottom:1px solid rgba(0,0,0,0.05); display:flex; gap:20px; align-items:center;"><div style="font-size:12px; background:{primary}11; color:{primary}; padding:5px 10px; border-radius:3px; font-weight:bold;">{d["date"]}</div><a href="/archive/doc-{d["doc_id"]}?bypass=1&k={request.args.get("k","")}" style="text-decoration:none; color:inherit; flex:1;"><h3 style="margin:0; font-size:1.1rem;">{d["title"]}</h3></a><div style="font-size:11px; opacity:0.5;">{d["doc_id"]}</div></div>' for d in samples + ge.get_data(5)])
        return f'<section style="padding:0;"><div style="max-width:1000px; margin:0 auto; background:#fff; min-height:100vh; border-left:1px solid #eee; border-right:1px solid #eee;"><div style="padding:40px; border-bottom:3px solid {primary};"><h2>{ge.target_keyword} 리얼타임 기술 피드</h2></div>{feed_items}</div></section>'

    # [Arch 6: Search-Centric Hub]
    if ge.skeleton_id == 6:
        return f'''
        <section style="padding:150px 5%; text-align:center;">
            <div style="max-width:800px; margin:0 auto;">
                <h1 style="font-size:3.5rem; margin-bottom:40px;">{ge.target_keyword} 통합 검색</h1>
                <div style="position:relative; margin-bottom:50px;">
                    <input type="text" placeholder="문서 일련번호 또는 키워드 분석..." style="width:100%; padding:30px 40px; border-radius:100px; border:2px solid {primary}; font-size:1.2rem; box-shadow:0 15px 30px {primary}11;">
                    <div style="position:absolute; right:30px; top:50%; transform:translateY(-50%); font-size:24px;">🔍</div>
                </div>
                <div style="display:flex; justify-content:center; gap:30px; color:#555; font-size:14px; font-weight:bold;">
                    <span>인기: 시방서</span><span>정밀분석</span><span>ISO지표</span>
                </div>
                <div style="margin-top:100px; text-align:left;">
                    <h3 style="margin-bottom:30px;">📂 시스템 추천 자료</h3>
                    {sample_items}
                </div>
            </div>
        </section>
        '''

    # [Arch 7, 18, 23, 24: Stats Dashboard]
    if ge.is_dashboard:
        stats = "".join([f'<div style="flex:1; background:#fff; padding:30px; border-radius:20px; border:1px solid #eee;"><div style="font-size:12px; opacity:0.5;">{t}</div><div style="font-size:2rem; font-weight:900; color:{primary};">{v}</div></div>' for t, v in [("무결성 지수", f"{ge.r.randint(990,999)/10}%"), ("활성 노드", f"{ge.r.randint(100,500)}ea"), ("보안 단계", "AA+")]])
        return f'''
        <section style="padding:100px 5%; background:rgba(0,0,0,0.02);">
            <div style="max-width:1200px; margin:0 auto;">
                <h2 style="margin-bottom:40px;">{ge.target_keyword} 실시간 관제 현황</h2>
                <div style="display:flex; gap:30px; margin-bottom:60px;">{stats}</div>
                <div style="background:#fff; padding:50px; border-radius:30px; border:1px solid #eee;">
                    <h3 style="margin-bottom:30px;">📈 기술 트래픽 추이</h3>
                    <div style="height:200px; background:linear-gradient(to right, {primary}22 20%, {primary}44 40%, {primary}11 60%, {primary}33 80%); border-radius:10px; display:flex; align-items:flex-end; padding:20px; gap:10px;">
                        <div style="flex:1; background:{primary}; height:40%;"></div>
                        <div style="flex:1; background:{primary}; height:70%;"></div>
                        <div style="flex:1; background:{primary}; height:55%;"></div>
                        <div style="flex:1; background:{primary}; height:90%;"></div>
                        <div style="flex:1; background:{primary}; height:65%;"></div>
                    </div>
                    <div style="margin-top:50px;">{sample_items}</div>
                </div>
            </div>
        </section>
        '''

    # [Arch 8: Infinite Grid]
    if ge.skeleton_id == 8:
        grid = "".join([f'<div class="card" style="padding:20px;"><div style="font-size:10px; opacity:0.4;">{d["doc_id"]}</div><h4 style="margin:10px 0;">{d["title"]}</h4><p style="font-size:13px; opacity:0.6;">{d["snippet"][:40]}...</p></div>' for d in ge.get_data(24)])
        return f'<section style="padding:50px;"><div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:20px;">{grid}</div></section>'

    # [Arch 9-12 removed: Mapped to Standard Block Below]

    # [Arch 4: Modular Zig-Zag]
    if ge.skeleton_id == 4:
        return f'''
        <section style="padding:100px 5%; background:rgba(0,0,0,0.02);">
            <div style="max-width:1200px; margin:0 auto; display:flex; gap:80px; align-items:center;">
                <div style="flex:1;">
                    <div style="background:{primary}; color:#fff; padding:8px 15px; display:inline-block; border-radius:50px; font-size:10px; font-weight:bold; margin-bottom:20px;">SYSTEM SPOTLIGHT</div>
                    <h2 style="font-size:2.8rem; line-height:1.1;">{latest_doc["title"]}</h2>
                    <p style="font-size:1.1rem; opacity:0.7; margin:30px 0;">{latest_doc["snippet"]} 분야의 정밀 기술 지표 분석이 완료되었습니다. 무결성 검증을 거친 최신 리포트입니다.</p>
                    <a href="/archive/doc-{latest_doc['doc_id']}?bypass=1&k={request.args.get('k','')}" class="btn">상세 리포트 확인</a>
                </div>
                <div style="flex:1; background:{primary}11; height:400px; border-radius:30px; display:flex; align-items:center; justify-content:center; font-size:80px;">💾</div>
            </div>
        </section>
        <section style="padding:100px 5%;">
            <div style="max-width:1200px; margin:0 auto;">
                <h3 style="text-align:center; margin-bottom:60px;">기타 주요 데이터 샘플</h3>
                <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(350px, 1fr)); gap:40px;">
                    {sample_items}
                </div>
            </div>
        </section>
        '''

    # [Standard/Split/Minimal Fallback for all others]
    layout_w = '1400px' if ge.has_widgets else '1200px'
    if ge.is_minimal: layout_w = '900px'
    
    return f'''
    <section style="background:rgba(0,0,0,0.02); padding:100px 5%;">
        <div style="max-width:{layout_w}; margin:0 auto;">
            <div style="display:flex; gap:50px; flex-wrap:wrap;">
                <div style="flex:{'2' if ge.has_widgets else '1.5' if not ge.is_minimal else '1'}; min-width:350px;">
                    <div style="background:{primary}22; color:{primary}; padding:10px 20px; display:inline-block; border-radius:10px; font-size:14px; margin-bottom:25px; border:1px solid {primary}44; font-weight:bold;">🚀 LATEST UPDATE</div>
                    <a href="/archive/doc-{latest_doc['doc_id']}?bypass=1&k={request.args.get('k','')}" style="text-decoration:none; color:inherit;">
                        <div class="card" style="padding:40px; border-top:8px solid {primary};">
                            <div style="display:flex; justify-content:space-between; margin-bottom:20px; font-size:14px; color:#555; font-weight:bold;">
                                <b>CODE: {latest_doc["doc_id"]}</b>
                                <span>ISSUE DATE: {latest_doc["date"]}</span>
                            </div>
                            <h2 style="font-size:2rem; margin-bottom:20px; color:#111;">{latest_doc["title"]}</h2>
                            <div style="font-size:1.1rem; line-height:2; color:#333; margin-bottom:30px; border-left:4px solid {primary}; padding-left:20px;">
                                {latest_doc["snippet"]} 분야의 최신 기술 지표를 분석한 결과, 시스템 무결성 및 성능 최적화가 완료되었음을 보고합니다.
                            </div>
                            <div class="btn" style="text-align:center; background:{primary}; color:#ffffff !important; font-weight:bold;">전체 리포트 열람하기</div>
                        </div>
                    </a>
                </div>
                
                <div style="flex:1; min-width:300px;">
                    { '<!-- Sidebar Widgets Arch -->' if ge.has_widgets else '' }
                    <h3 style="margin-bottom:30px;">📂 주요 샘플 자료</h3>
                    <div style="display:flex; flex-direction:column; gap:20px;">
                        {sample_items}
                    </div>
                    { f'<div style="margin-top:40px; padding:30px; background:{primary}08; border-radius:15px; border:1px solid {primary}22;"><h4 style="font-size:14px;">실시간 무결성 지수</h4><div style="font-size:24px; font-weight:bold; color:{primary};">{ge.r.randint(990,999)/10}%</div><div style="font-size:11px; opacity:0.5; margin-top:5px;">V2.14-ALPHA ENFORCED</div></div>' if ge.has_widgets else '' }
                    <div style="margin-top:30px; text-align:right;">
                        <a href="/archive?bypass=1&k={request.args.get('k','')}" style="font-size:15px; color:{primary}; font-weight:bold; text-decoration:none; border-bottom:2px solid {primary}44; padding-bottom:3px;">전체 1,024개 자료 보기 →</a>
                    </div>
                </div>
            </div>
        </div>
    </section>
    '''

def block_detail_view(ge, doc_id):
    # [V4.22] Unique Document Detail Engine
    # Seed the engine with doc_id for unique content per page
    ge.r.seed(f"{ge.raw_seed}_{doc_id}")
    primary = ge.primary_color
    
    # Generate unique metrics
    integrity = ge.r.randint(990, 999) / 10
    security_level = ge.r.choice(["S", "AA", "A+", "TOP-SECRET"])
    audit_id = f"SYS-{ge.r.randint(1000, 9999)}"
    
    # Select unique snippets from the pool
    pool = ge.niche_templates.get(ge.niche_key, ge.niche_templates["universal"])
    main_snippet = ge.r.choice(pool)
    secondary_snippets = ge.r.sample(pool, 2)
    
    return f'''
    <section>
        <div style="max-width:1000px; margin:0 auto;">
            <div class="card" style="padding:60px; border-top:12px solid {primary};">
                <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:40px; border-bottom:1px solid rgba(0,0,0,0.1); padding-bottom:30px;">
                    <div>
                        <div style="display:inline-block; padding:5px 12px; background:{primary}22; color:{primary}; font-size:11px; font-weight:bold; border-radius:3px; margin-bottom:15px;">TECHNICAL REPORT</div>
                        <h1 style="font-size:3rem; line-height:1.1; margin:0;">{doc_id}<br>연구 분석 보고서</h1>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:24px; font-weight:900; color:{primary};">{integrity}%</div>
                        <div style="font-size:11px; opacity:0.5;">무결성 지수</div>
                    </div>
                </div>

                <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:40px; margin-bottom:50px;">
                    <div>
                        <h4 style="margin-bottom:20px; font-size:14px; opacity:0.6;">[1] 분석 개요</h4>
                        <p style="font-size:17px; line-height:2; opacity:0.8;">
                            본 문서는 {ge.target_keyword} 분야 연구 데이터 {doc_id}의 무결성을 증명하는 상세 기술서입니다. 
                            {main_snippet} 및 관련 공정을 ISO-2026 표준에 따라 심층 분석한 결과를 포함하고 있습니다.
                        </p>
                    </div>
                    <div style="background:rgba(0,0,0,0.02); padding:30px; border-radius:15px;">
                        <h4 style="margin-bottom:20px; font-size:14px; opacity:0.6;">[2] 기술 가드레인</h4>
                        <ul style="padding-left:20px; font-size:14px; line-height:2; margin:0; opacity:0.7;">
                            <li>{secondary_snippets[0]}</li>
                            <li>{secondary_snippets[1]}</li>
                            <li>실시간 노드 동기화 상태: <span style="color:#00aa00;">VERIFIED</span></li>
                        </ul>
                    </div>
                </div>

                <div style="margin-bottom:50px;">
                    <h4 style="margin-bottom:20px; font-size:14px; opacity:0.6;">[3] 정밀 데이터 그래프</h4>
                    {ge.gen_chart('bar')}
                    <div style="margin-top:15px; font-size:12px; text-align:center; opacity:0.5;">{ge.target_keyword} 하중 밸런싱 및 시계열 트래픽 추이 (ALPHA-9)</div>
                </div>

                <div style="margin-bottom:50px;">
                    <h4 style="margin-bottom:20px; font-size:14px; opacity:0.6;">[4] 기술 분석 요약 (Technical Abstract)</h4>
                    <p style="font-size:16px; line-height:1.9; opacity:0.8; text-align:justify; margin-bottom:30px;">
                        본 시방서는 2026년 개정된 <b>{ge.target_keyword}</b> 표준 공법을 준수하여 작성되었습니다. 
                        <b>{ge.gen_lego_text(3)}</b>
                        특히 제3섹션에서 다루는 데이터 처리 및 유체 역학적 부하 계산은 ISO-9001 기준을 {ge.r.randint(10,20)}% 상회하는 정밀도를 보이며, 
                        <b>{ge.gen_lego_text(2)}</b>
                        현장에서 수집된 {ge.r.randint(1000,5000)}건의 샘플 데이터를 기반으로 최적화된 결과값입니다. 
                        <b>{ge.gen_lego_text(3)}</b>
                        모든 데이터는 AES-256 암호화 프로토콜을 통해 보호되며, 무단 복제 시 산업기술보호법에 의거하여 처벌받을 수 있습니다.
                    </p>
                    
                    <div style="background:#f5f5f5; padding:25px; border-left:5px solid #666; font-size:13px; color:#555; line-height:1.8; margin-bottom:40px;">
                        <b>[근거 법령 및 표준 규격 명시]</b><br>
                        - 산업안전보건법 제23조 (안전조치 의무) 및 시행령 제18조<br>
                        - KCS {ge.r.randint(1000,9999)} : {ge.target_keyword} 표준 시공 기준<br>
                        - 데이터 보존 등급 : <b>Class-A (영구 보존)</b><br>
                        - 최종 승인 기관 : 국가기술표준원 산하 {ge.niche_key.upper()} 연구소
                    </div>
                </div>

                <div style="text-align:right; margin-top:60px; padding-top:40px; border-top:1px solid #eee;">
                    <div style="display:inline-block; text-align:center;">
                        <div style="font-size:14px; margin-bottom:10px;"><b>책임연구원 김철수</b></div>
                        <div style="border:3px solid #cc0000; color:#cc0000; font-weight:bold; font-size:18px; padding:8px 20px; display:inline-block; transform:rotate(-5deg); letter-spacing:3px;">승인</div>
                        <div style="font-size:10px; color:#999; margin-top:5px;">Digital Signed: {time.strftime("%Y.%m.%d")}</div>
                    </div>
                </div>

                <div style="margin-top:60px; display:flex; justify-content:space-between; align-items:center;">
                    <a href="/archive?bypass=1&k={request.args.get('k','')}" class="btn" style="background:rgba(0,0,0,0.1); color:#333 !important;">&larr; 목록으로 돌아가기</a>
                    <div style="font-size:11px; opacity:0.3;">ISSUE_DATE: {ge.r.randint(20,30)}.01.2026</div>
                </div>
            </div>
        </div>
    </section>
    '''

def block_service_grid(ge):
    # [High Density Service Grid V4.11]
    items = [
        (f"정밀 {ge.target_keyword} 시뮬레이션", "고해상도 데이터 아카이브를 통한 실시간 가상 추론 서비스."),
        (f"국가 공인 {ge.target_keyword} 감리", "ISO 규격에 따은 공정 전수 조사 및 무결성 검증 서비스."),
        (f"통합 {ge.target_keyword} 데이터 뱅크", f"{ge.target_keyword} 관련 전 세계 시방서 통합 관리 및 배포."),
        (f"AI 기반 {ge.target_keyword} 예측분석", "과거 시계열 데이터를 바탕으로 미래 인프라 수요 자동 감지."),
        (f"전문가용 {ge.target_keyword} 교육 세션", f"기술 지원 센터 소속 기술자들을 위한 심화 공학 세미나."),
        ("글로벌 기술 표준 동기화", f"해외 선진 {ge.target_keyword} 아카이브와 실시간 노드 동기화."),
        (f"실시간 {ge.target_keyword} 품질 모니터링", "현장 센서 데이터의 실시간 수집 및 이상 징후 자동 알림."),
        (f"차세대 {ge.target_keyword} 인프라 컨설팅", "지속 가능한 인프라 구축을 위한 전문가 기술 자문 서비스."),
        (f"디지털 트윈 기반 {ge.target_keyword} 분석", "가상 공간 내 실시간 공정 시뮬레이션 및 데이터 시각화.")
    ]
    cards = "".join([f'<div class="card" style="text-align:left; border-bottom:5px solid {ge.primary_color}1a;"><img src="https://picsum.photos/seed/{ge.raw_seed}{i}/400/250" style="width:100%; border-radius:15px; margin-bottom:20px; filter:grayscale(0.5) contrast(1.2);"><h3>{t}</h3><p style="font-size:14px; opacity:0.7; line-height:1.6;">{d}</p></div>' for i, (t, d) in enumerate(items)])
    
    return f'''
    <section style="background:linear-gradient(to bottom, #fff, {ge.primary_color}05);">
        <div style="max-width:1200px; margin:0 auto;">
            <div style="text-align:center; margin-bottom:60px;">
                <h1 style="margin-bottom:15px;">{ge.nav["service"]}</h1>
                <p style="opacity:0.6;">가장 공신력 있는 {ge.target_keyword} 전문 기술 지원 영역입니다.</p>
            </div>
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:40px;">
                {cards}
            </div>
        </div>
    </section>
    '''

def block_contact_info(ge):
    faqs = [
        ("연구소 방문이 가능한가요?", "현재 보안 구역은 예약제로 운영되며, 일반 자료실은 상시 개방입니다."),
        ("기술 표준 데이터는 유료인가요?", "공익 아카이브로서 모든 기초 데이터는 무료로 공개됩니다."),
        ("추가 센터 설립 계획이 있나요?", "2026년 하반기 신규 데이터 센터 개소 예정입니다.")
    ]
    faq_html = "".join([f'<div class="card" style="margin-bottom:20px;"><b style="color:{ge.primary_color}; font-weight:900;">Q. {q}</b><br><p style="margin-top:10px; font-size:14px; opacity:0.8;">A. {a}</p></div>' for q, a in faqs])
    
    return f'''
    <section style="background:{ge.primary_color}0a;">
        <div style="max-width:1200px; margin:0 auto; display:flex; gap:60px; flex-wrap:wrap;">
            <div style="flex:1; min-width:300px;">
                <h1>{ge.nav["contact"]}</h1>
                <div style="margin-top:40px; background:#eee; height:300px; border-radius:20px; display:flex; align-items:center; justify-content:center; color:#888;">
                    [ 국가 통합 센터 지도 미리보기 ]
                </div>
                <div style="margin-top:20px; opacity:0.7;">
                    📍 국가 기술지원센터 본부<br>
                    📧 tech-support@{ge.raw_seed}.org
                </div>
            </div>
            <div style="flex:1; min-width:300px;">
                <h3 style="margin-bottom:30px;">자주 묻는 질문 (FAQ)</h3>
                {faq_html}
            </div>
        </div>
    </section>
    '''

@app.route('/board')
def route_board():
    ge = get_ge()
    board = block_board(ge)
    # MASSIVE LOGS
    more_logs = "".join([f'<div style="border-bottom:1px solid #333; padding:10px;">[{time.strftime("%H:%M:%S")}] SYSTEM_AUDIT: {x}</div>' for x in ge.get_data(30)])
    content = f'<section><h2>시스템 감사 로그</h2><div style="background:#111; color:#0f0; padding:20px; font-family:monospace; height:800px; overflow-y:scroll;">{more_logs}</div></section>'
    return make_response(render_page(ge, [board, content]))

@app.route('/stats')
def route_stats():
    ge = get_ge()
    
    # [KEYWORD EXTRACTION]
    target_keyword = request.args.get('k', None)
    if target_keyword and target_keyword in CPA_DATA:
        target_keyword = CPA_DATA[target_keyword][0]
    
    # [PAGINATION]
    page = int(request.args.get('p', 1))
    items_per_page = 20
    total_items = 100
    start_idx = (page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, total_items)
    
    # [CONTENT GENERATION]
    data = []
    for i in range(total_items):
        if target_keyword and i < 30:
            templates = [
                f"{target_keyword} 전문 분석 시스템 {i+1}차 검증 완료",
                f"{target_keyword} 데이터 수집 및 정리 프로세스 최적화",
                f"{target_keyword} 품질 지표 안전 기준 측정",
                f"{target_keyword} 서비스 솔루션 고도화 단계",
                f"{target_keyword} 전담팀의 정밀 모니터링 보고서",
                f"{target_keyword} 관련 법적 규제 준수 확인",
                f"{target_keyword} 표준화 데이터 마이닝 완료"
            ]
            data.append(ge.r.choice(templates))
        else:
            data.append(ge.get_data(1)[0])
    
    page_data = data[start_idx:end_idx]
    
    # [MODE FILTERING]
    mode = request.args.get('mode', 'all')
    
    # [10 ARCHETYPES]
    if mode == 'analytics':
        archetypes = ['api_usage', 'data_sync', 'ranking_top']
        subtitle_context = "Data Analytics & Performance Metrics"
    elif mode == 'status':
        # Removed 'faq_list' per user preference for visual data
        archetypes = ['network_map', 'live_ticker', 'access_log', 'sys_calendar', 'terminal_hack', 'admin_inbox']
        subtitle_context = "System Status & Operational Monitoring"
    else:
        # Fallback / Mixed
        archetypes = [
            'access_log', 'live_ticker', 
            'data_sync', 'ranking_top', 
            'admin_inbox', 'sys_calendar', 'network_map', 
            'api_usage', 'terminal_hack'
        ]
        subtitle_context = "Comprehensive System Overview"
        
    layout = ge.r.choice(archetypes)
    
    # [CONTEXT HEADER GENERATOR]
    # Adds a professional header block to explain 'Why is this chart here?'
    titles = ["SYSTEM DASHBOARD", "NETWORK VISION", "SECURITY CENTER", "DATA INSIGHTS", "OPS CONTROL"]
    header_title = ge.r.choice(titles)
    
    context_header = f'''
    <div style="background:#fff; padding:30px 40px; border-bottom:1px solid #eee; margin-bottom:0; display:flex; justify-content:space-between; align-items:end;">
        <div>
            <div style="font-size:12px; font-weight:bold; color:{ge.theme_color}; margin-bottom:5px;">{subtitle_context.upper()}</div>
            <h1 style="margin:0; font-size:28px; color:#111;">{header_title} // <span style="font-weight:300;">{layout.replace('_', ' ').upper()}</span></h1>
        </div>
        <div style="text-align:right;">
            <div style="font-size:14px; color:#555;"><strong>Server Time:</strong> {time.strftime("%Y-%m-%d %H:%M:%S")} UTC</div>
            <div style="font-size:12px; color:#999; margin-top:5px;">SESSION ID: {ge.r.randint(100000, 999999)}</div>
        </div>
    </div>
    <div style="padding:40px 5%;">
    '''
    
    # [LAYOUT GENERATORS]
    content_html = ""
    
    # 1. Visitor Access Log
    if layout == 'access_log':
        rows = ""
        for i in range(15):
            user_id = f"User_{ge.r.randint(100,999)}***"
            action = ge.r.choice(["문서 열람", "자료 다운로드", "접속 시도", "검색 요청", "프로필 갱신"])
            target = f"DOC-{ge.r.randint(1000,9999)}"
            rows += f'''
            <div style="display:flex; justify-content:space-between; padding:15px; border-bottom:1px solid #eee; font-size:14px;">
                <div><span style="font-weight:bold; color:{ge.dark_accent};">{user_id}</span> 님이 <span style="color:#555;">{target}</span>에 {action}했습니다.</div>
                <div style="color:#999; font-size:12px;">{ge.r.randint(1,59)}분 전</div>
            </div>'''
        content_html = f'<div style="background:#fff; padding:30px; border-radius:15px; box-shadow:0 5px 20px rgba(0,0,0,0.05);"><h3 style="margin-bottom:20px;">👥 실시간 방문자 로그</h3>{rows}</div>'

    # 2. Live Request Ticker
    elif layout == 'live_ticker':
        rows = ""
        regions = ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종", "경기", "강원"]
        for i in range(20):
            region = ge.r.choice(regions)
            status = "접수완료" if ge.r.random() > 0.3 else "처리중"
            color = ge.theme_color if status == "처리중" else "#999"
            rows += f'''
            <div style="padding:15px; border-bottom:1px dashed #eee; font-size:14px; display:flex; align-items:center;">
                <span style="background:{ge.sub_color}22; padding:3px 8px; border-radius:5px; font-size:11px; margin-right:10px; color:{ge.dark_accent};">{region}</span>
                <span style="flex-grow:1; color:#555;">{data[i][:40]}...</span>
                <span style="font-weight:bold; color:{color}; font-size:12px;">{status}</span>
            </div>'''
        content_html = f'<div style="background:#fff; padding:30px; border-radius:15px; box-shadow:0 5px 20px rgba(0,0,0,0.05);"><h3 style="margin-bottom:20px;">📡 실시간 요청 현황</h3><div style="max-height:600px; overflow-y:auto;">{rows}</div></div>'

    # 3. FAQ List
    elif layout == 'faq_list':
        rows = ""
        questions = [f"데이터 열람은 어떻게 하나요?", f"보안 인증서는 어디서 발급받나요?", f"{target_keyword if target_keyword else '시스템'} 관련 문의처가 있나요?", "정기 점검 시간은 언제인가요?", "회원 가입 절차를 알려주세요."]
        for i, q in enumerate(questions):
            rows += f'''
            <div style="border:1px solid #eee; border-radius:10px; margin-bottom:15px; overflow:hidden;">
                <div style="padding:15px; background:#f9f9f9; font-weight:bold; cursor:pointer; color:#333;">Q. {q}</div>
                <div style="padding:20px; background:#fff; color:#555; line-height:1.6; border-top:1px solid #eee;">A. {data[i]} 자세한 내용은 관리자에게 문의해주시기 바랍니다.</div>
            </div>'''
        content_html = f'<div style="max-width:800px; margin:0 auto;"><h3 style="text-align:center; margin-bottom:40px;">자주 묻는 질문</h3>{rows}</div>'

    # 4. Data Sync Monitor (Table)
    elif layout == 'data_sync':
        rows = ""
        for i in range(10):
            node = f"NODE-{ge.r.randint(100,999)}"
            sync_rate = ge.r.randint(90, 100)
            status = "정상" if sync_rate > 95 else "동기화 중"
            rows += f'''
            <tr style="border-bottom:1px solid #eee;">
                <td style="padding:15px; color:#555;">{node}</td>
                <td style="padding:15px; color:#555;">{time.strftime("%Y-%m-%d %H:%M")}</td>
                <td style="padding:15px;">
                    <div style="background:#eee; height:8px; width:100px; border-radius:4px; overflow:hidden;">
                        <div style="background:{ge.theme_color}; height:100%; width:{sync_rate}%;"></div>
                    </div>
                </td>
                <td style="padding:15px; font-weight:bold; color:{ge.dark_accent};">{status}</td>
            </tr>'''
        content_html = f'<div style="background:#fff; padding:30px; border-radius:15px;"><h3 style="margin-bottom:20px;">🔄 데이터 동기화 모니터</h3><table style="width:100%; border-collapse:collapse;"><thead><tr style="text-align:left; color:#999; font-size:12px;"><th style="padding:10px;">노드명</th><th style="padding:10px;">마지막 확인</th><th style="padding:10px;">동기화율</th><th style="padding:10px;">상태</th></tr></thead><tbody>{rows}</tbody></table></div>'

    # 5. Ranking Top 10
    elif layout == 'ranking_top':
        rows = ""
        for i in range(10):
            rank = i + 1
            badge_color = "#f44336" if rank == 1 else "#ff9800" if rank == 2 else "#ffc107" if rank == 3 else "#eee"
            text_color = "#fff" if rank <= 3 else "#555"
            rows += f'''
            <div style="display:flex; align-items:center; padding:15px; border-bottom:1px solid #f5f5f5; background:#fff;">
                <div style="width:30px; height:30px; background:{badge_color}; color:{text_color}; border-radius:50%; display:flex; justify-content:center; align-items:center; font-weight:bold; margin-right:20px;">{rank}</div>
                <div style="flex-grow:1; font-weight:bold; color:#333;">{data[i]}</div>
                <div style="color:#999; font-size:12px;">{ge.r.randint(1000,50000)}회 다운로드</div>
            </div>'''
        content_html = f'<div style="max-width:700px; margin:0 auto; background:#fff; border-radius:20px; box-shadow:0 10px 40px rgba(0,0,0,0.1); overflow:hidden;"><div style="background:{ge.dark_accent}; padding:30px; color:#fff; text-align:center;"><h2 style="margin:0;">🏆 주간 인기 자료 TOP 10</h2></div>{rows}</div>'

    # 6. Admin Inbox
    elif layout == 'admin_inbox':
        cards = ""
        for i in range(9):
            ticket_id = ge.r.randint(10000,99999)
            cards += f'''
            <div style="background:#fff; padding:20px; border-radius:10px; border:1px solid #eee; cursor:pointer; transition:0.2s;" onmouseover="this.style.borderColor='{ge.theme_color}'" onmouseout="this.style.borderColor='#eee'">
                <div style="font-size:11px; color:#999; margin-bottom:10px;">Ticket #{ticket_id}</div>
                <h4 style="margin:0 0 10px 0; color:#333;">{data[i][:20]}... 관련 문의</h4>
                <div style="display:flex; align-items:center; gap:10px;">
                    <span style="width:8px; height:8px; background:{ge.theme_color}; border-radius:50%;"></span>
                    <span style="font-size:12px; color:#555;">처리 대기 중</span>
                </div>
            </div>'''
        content_html = f'<h3 style="margin-bottom:20px;">📨 관리자 수신함 (최근 30일)</h3><div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(250px, 1fr)); gap:20px;">{cards}</div>'

    # 7. System Calendar
    elif layout == 'sys_calendar':
        # Simple CSS Grid Calendar
        days = ""
        for d in range(1, 31):
            event = ""
            if ge.r.random() > 0.7:
                event = f"<div style='background:{ge.sub_color}33; color:{ge.dark_accent}; font-size:10px; padding:2px 5px; border-radius:3px; margin-top:5px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;'>시스템 점검</div>"
            days += f"<div style='border:1px solid #eee; height:80px; padding:5px;'><span style='color:#999; font-size:12px;'>{d}</span>{event}</div>"
        content_html = f'<div style="background:#fff; padding:30px; border-radius:15px;"><h3 style="text-align:center; margin-bottom:20px;">📅 시스템 운영 일정</h3><div style="display:grid; grid-template-columns:repeat(7, 1fr); gap:0; text-align:left;">{days}</div></div>'

    # 8. Network Map (High-Quality Vector)
    elif layout == 'network_map':
        # Path Data from Mapsicon (South Korea)
        # 1024x1024 ViewBox, Transformed
        korea_path = "M6039 10223 c-10 -11 -14 -46 -15 -112 0 -112 -21 -176 -80 -248 -81 -99 -268 -223 -336 -223 -15 0 -71 10 -125 21 l-97 22 -54 -28 c-57 -30 -68 -29 -124 17 l-28 22 -101 -18 c-98 -17 -104 -17 -155 0 l-53 18 -55 -37 c-31 -20 -61 -37 -67 -37 -6 0 -43 14 -82 31 -68 30 -74 31 -117 19 -80 -22 -91 -23 -132 -4 -40 18 -41 18 -102 -4 -33 -12 -73 -22 -88 -22 -34 0 -202 -131 -242 -188 -15 -22 -30 -59 -33 -82 -5 -37 -13 -48 -68 -91 -54 -42 -65 -57 -85 -111 -32 -88 -127 -181 -208 -204 -32 -9 -61 -22 -67 -28 -5 -7 -9 -50 -7 -94 l4 -82 26 6 27 7 -33 -35 -33 -35 7 -79 c3 -45 1 -99 -5 -124 l-10 -45 61 -57 c34 -32 65 -58 70 -58 4 0 8 -4 8 -10 0 -19 -29 -10 -93 30 -35 22 -69 52 -75 66 -7 14 -12 56 -12 94 0 39 -3 70 -7 70 -5 -1 -19 -7 -33 -15 -33 -19 -74 -19 -111 0 -27 14 -30 14 -36 -1 -16 -43 14 -179 65 -294 28 -63 54 -132 57 -152 6 -32 11 -38 32 -38 25 0 25 0 -11 -40 -20 -22 -36 -43 -36 -48 0 -4 16 -18 36 -32 33 -22 36 -27 31 -62 -5 -40 7 -58 26 -39 15 15 27 14 65 -9 l33 -20 -20 -29 c-12 -16 -21 -35 -21 -43 0 -8 29 -30 65 -49 70 -37 78 -54 24 -53 -19 0 -36 -2 -39 -5 -11 -13 -82 -41 -90 -36 -11 7 -17 -65 -12 -137 4 -49 7 -57 19 -47 25 22 37 -4 25 -53 l-11 -43 52 58 c56 63 90 73 135 41 31 -22 28 -39 -17 -74 -36 -29 -38 -34 -34 -74 4 -28 0 -53 -11 -74 -17 -32 -17 -32 10 -32 14 0 39 -8 55 -17 25 -15 27 -19 14 -33 -13 -14 -7 -23 48 -81 82 -86 95 -93 138 -71 27 13 35 24 37 50 3 34 11 39 30 20 19 -19 14 -63 -11 -86 -12 -12 -53 -35 -89 -52 -69 -30 -91 -53 -103 -103 -12 -46 -24 -40 -40 20 -36 127 -57 181 -83 212 -24 29 -37 35 -92 43 -58 8 -66 7 -78 -10 -12 -18 -14 -17 -50 17 -21 20 -71 56 -111 80 l-73 43 -28 -33 c-30 -37 -29 -46 13 -91 18 -19 21 -28 12 -32 -8 -3 -15 -15 -17 -28 -3 -20 -7 -17 -31 24 -32 56 -52 68 -104 68 -42 -1 -114 -28 -78 -29 32 -1 67 -31 60 -49 -4 -11 6 -27 32 -48 l38 -32 -18 -36 c-9 -21 -31 -45 -47 -54 -16 -9 -30 -22 -30 -27 0 -6 -7 -21 -16 -33 -14 -21 -18 -22 -33 -8 -15 13 -16 11 -16 -22 0 -40 -23 -54 -50 -32 -23 19 -20 104 4 121 18 14 18 15 1 54 l-17 40 -23 -52 c-29 -66 -79 -82 -96 -31 -4 13 -9 17 -15 11 -6 -6 -5 -20 3 -37 10 -24 10 -29 -5 -37 -22 -13 -22 -26 2 -34 23 -7 35 -35 22 -48 -7 -7 -19 -6 -37 2 -24 11 -30 9 -56 -16 -41 -39 -50 -59 -42 -96 l6 -31 15 27 c14 28 14 28 44 10 45 -27 62 -49 54 -72 -5 -16 -15 -21 -41 -21 -24 0 -34 -5 -34 -15 0 -24 24 -18 81 20 56 38 79 39 79 4 0 -12 16 -39 35 -60 38 -42 45 -80 20 -113 -19 -25 -19 -56 0 -56 27 0 47 -59 52 -158 5 -79 10 -101 31 -133 22 -34 30 -39 64 -39 24 0 38 5 38 13 0 6 -32 118 -70 247 -67 226 -81 292 -61 305 20 12 41 -39 41 -98 0 -38 4 -59 13 -61 6 -2 26 -8 44 -13 36 -12 43 -4 43 51 0 36 24 76 46 76 14 0 19 -34 17 -102 -1 -16 3 -28 8 -28 15 0 10 -22 -7 -35 -15 -10 -14 -18 5 -86 12 -42 21 -103 21 -137 0 -46 4 -64 15 -68 18 -7 19 -36 3 -82 -11 -29 -11 -36 0 -40 20 -6 82 -62 82 -74 0 -5 -13 -14 -30 -19 -17 -6 -30 -15 -30 -21 0 -5 14 -29 30 -52 l31 -42 -21 -108 c-12 -60 -20 -109 -18 -111 2 -1 21 -12 43 -23 57 -28 125 -104 125 -139 1 -39 64 -123 92 -123 12 0 34 12 49 26 26 25 189 89 189 74 0 -14 -47 -50 -93 -70 -27 -12 -51 -28 -54 -36 -9 -24 -34 -32 -174 -54 -74 -12 -136 -24 -138 -26 -2 -2 18 -8 43 -15 54 -13 69 -34 64 -87 -3 -32 0 -37 19 -40 12 -2 36 4 54 13 28 15 40 15 90 5 54 -12 60 -11 93 9 20 13 45 21 57 19 20 -3 18 -7 -24 -50 -38 -40 -53 -48 -95 -54 -73 -9 -83 -19 -48 -49 16 -13 47 -31 68 -41 33 -15 38 -21 38 -51 0 -38 -13 -42 -50 -13 -19 15 -41 20 -97 20 l-72 0 -21 -47 c-26 -60 -71 -107 -127 -134 -44 -21 -123 -101 -123 -125 0 -7 12 -26 26 -43 30 -36 49 -38 136 -15 77 19 106 16 131 -18 21 -29 17 -72 -5 -50 -18 18 -45 14 -61 -8 -10 -15 -32 -22 -84 -29 -39 -5 -79 -14 -90 -19 -29 -16 -69 -72 -109 -154 -27 -56 -34 -81 -30 -108 4 -28 1 -38 -13 -47 -11 -7 -26 -34 -35 -60 -9 -26 -37 -79 -61 -117 -25 -38 -45 -74 -45 -80 0 -7 7 -22 16 -35 13 -19 23 -22 49 -18 32 5 33 4 39 -35 5 -33 19 -53 68 -100 l61 -60 -12 -38 c-12 -39 -60 -100 -80 -100 -14 0 -14 17 -1 25 14 9 -31 85 -50 85 -9 0 -26 7 -38 16 -18 12 -22 25 -22 66 0 40 -3 48 -13 40 -7 -6 -32 -12 -57 -14 -43 -3 -56 -14 -73 -62 -2 -5 -12 -3 -23 4 -25 16 -86 6 -105 -16 -11 -13 -7 -21 27 -49 21 -19 49 -34 61 -35 13 0 32 -9 44 -21 l21 -21 22 21 c12 12 32 21 44 21 18 0 22 6 22 31 0 24 3 30 16 25 9 -3 18 -6 20 -6 2 0 4 -16 4 -35 0 -33 2 -35 34 -35 22 0 36 -6 40 -16 7 -19 8 -17 -21 -33 -15 -8 -23 -21 -23 -39 0 -26 2 -27 44 -24 l44 4 -14 -59 c-18 -77 -17 -115 3 -158 l17 -35 -37 -38 c-20 -21 -37 -48 -37 -60 0 -27 1 -27 50 -2 49 25 61 25 111 0 l40 -21 19 23 19 23 1 -31 c0 -30 -25 -64 -47 -64 -6 0 -16 7 -23 15 -7 8 -27 15 -44 15 -40 0 -123 -37 -110 -49 5 -5 42 -19 82 -31 73 -21 112 -47 112 -75 0 -8 9 -19 20 -25 32 -17 23 -30 -20 -30 -22 0 -40 -4 -40 -10 0 -5 -6 -10 -14 -10 -13 0 -26 26 -41 78 -3 12 -14 22 -23 22 -9 0 -26 3 -37 6 -16 4 -24 -3 -38 -31 -27 -57 -22 -69 49 -126 77 -61 74 -82 -8 -51 -66 24 -91 59 -108 149 -16 85 -35 133 -53 133 -17 0 -57 -104 -57 -147 0 -17 9 -42 21 -57 13 -16 19 -35 16 -48 -8 -28 31 -65 77 -73 21 -5 45 -18 57 -33 15 -20 22 -23 28 -13 11 18 43 7 80 -29 26 -23 31 -36 31 -73 0 -24 3 -59 6 -76 6 -26 11 -31 35 -31 26 0 29 -3 29 -34 0 -19 -5 -38 -10 -41 -6 -3 -17 -20 -26 -36 -14 -29 -14 -29 4 -18 36 22 52 5 52 -56 0 -30 2 -55 5 -55 3 0 19 10 35 21 16 12 35 19 44 16 21 -8 28 7 35 77 l6 61 66 35 c82 43 99 58 92 76 -3 7 2 17 11 20 30 12 57 82 63 163 7 98 15 113 36 68 12 -25 17 -62 17 -131 l0 -95 37 -26 c44 -29 69 -32 95 -8 15 13 23 14 44 5 33 -16 31 -16 39 18 5 25 11 30 26 25 17 -6 19 -1 19 53 0 46 4 63 20 77 15 14 17 21 8 32 -8 10 -8 20 1 39 6 14 11 33 11 43 0 12 25 35 67 62 38 24 85 59 105 77 32 29 40 32 59 22 34 -19 65 2 94 64 32 67 47 74 78 35 l23 -30 26 21 c35 27 45 25 63 -10 19 -37 19 -73 -1 -116 -14 -29 -21 -34 -50 -34 -33 0 -34 1 -34 40 0 22 -4 40 -10 40 -17 0 -43 -63 -44 -107 -1 -40 -3 -43 -28 -43 -20 0 -28 5 -29 18 0 10 -7 3 -17 -19 -9 -19 -36 -57 -59 -84 -24 -26 -43 -51 -43 -55 0 -3 11 -17 25 -30 24 -22 28 -23 58 -11 81 33 93 28 174 -74 l31 -40 24 21 c12 12 42 31 65 43 35 18 73 62 73 86 0 3 -13 5 -30 5 -29 0 -40 13 -20 25 6 3 10 11 10 16 0 6 -13 1 -29 -11 -32 -22 -35 -20 -45 22 -5 22 -1 31 18 43 22 15 27 14 70 -7 39 -18 50 -20 66 -10 16 10 21 9 30 -8 17 -31 50 -9 50 33 0 27 -5 35 -31 44 -23 9 -29 16 -25 31 5 14 -6 27 -48 56 -38 26 -57 46 -61 67 -4 16 -11 31 -16 34 -17 11 -9 42 14 58 22 15 22 15 2 31 -20 16 -20 16 1 34 l21 17 -29 29 c-32 32 -31 44 2 26 19 -10 27 -8 52 10 21 16 40 21 71 18 41 -3 42 -2 45 30 2 17 7 32 11 32 4 0 22 -15 40 -34 29 -30 33 -39 27 -68 -5 -28 -3 -35 16 -43 20 -9 67 -77 68 -97 0 -3 -11 -20 -25 -36 -18 -22 -21 -32 -12 -41 9 -9 9 -16 -1 -31 -6 -11 -12 -33 -12 -50 0 -26 4 -30 28 -30 15 0 38 -7 50 -16 26 -18 26 -18 7 57 -17 66 -14 77 33 123 l31 28 27 -21 c50 -39 104 -16 104 45 0 16 7 54 15 84 8 30 15 61 15 68 0 15 -96 17 -105 2 -9 -14 -81 -50 -100 -50 -21 0 -76 89 -74 120 1 14 -2 33 -6 43 -15 35 10 42 64 18 27 -11 55 -21 62 -21 7 0 35 25 64 55 57 61 79 67 125 33 28 -20 31 -20 48 -5 22 20 49 22 54 5 9 -26 57 10 83 63 l26 51 20 -21 c14 -15 32 -21 64 -21 53 0 58 14 19 60 -30 36 -22 60 14 41 33 -17 39 -13 46 29 4 28 11 40 22 40 14 0 15 -7 9 -38 -4 -20 -7 -48 -6 -62 3 -39 3 -123 -1 -150 -3 -23 1 -25 46 -31 37 -4 54 -12 70 -32 12 -15 31 -27 43 -27 28 0 73 37 73 61 0 16 7 19 51 19 47 0 51 -2 61 -30 12 -35 32 -35 36 1 4 32 23 79 32 79 20 0 70 -85 70 -120 0 -18 -4 -20 -35 -14 -30 5 -35 3 -35 -12 0 -15 8 -19 33 -19 17 0 51 -4 73 -8 l41 -7 12 61 c9 43 9 64 2 73 -8 10 -6 18 9 31 19 17 19 18 -6 38 -32 25 -18 37 43 37 53 0 64 17 29 47 -35 30 -50 29 -108 -8 -27 -17 -52 -29 -55 -25 -4 3 1 22 10 41 22 46 76 73 112 57 42 -19 47 -14 25 28 -27 53 -26 59 13 57 17 -1 52 2 77 6 39 6 49 4 73 -18 28 -25 28 -26 12 -51 -20 -31 -18 -33 23 -22 42 11 42 33 -3 122 -38 74 -44 125 -19 150 25 26 44 20 38 -11 -7 -37 28 -117 44 -101 8 8 15 8 26 -1 8 -7 29 -11 47 -9 34 3 36 1 55 -71 3 -9 14 -11 37 -7 102 19 102 19 134 -8 17 -14 43 -26 57 -26 21 0 29 8 42 40 19 47 38 43 32 -7 -3 -28 -2 -32 7 -20 6 9 24 17 41 19 27 3 29 0 32 -32 5 -49 17 -57 38 -24 10 16 20 31 22 34 1 2 7 -2 11 -9 7 -11 12 -8 21 10 18 34 61 79 77 79 7 0 13 -9 13 -20 0 -11 6 -20 14 -20 8 0 22 -3 30 -6 14 -6 16 1 10 50 l-7 56 56 0 c49 0 58 3 81 31 14 17 38 51 52 76 23 37 25 48 15 66 -10 18 -9 29 3 52 9 17 16 40 16 53 0 15 6 22 20 22 11 0 37 16 59 35 21 19 46 35 55 35 14 0 15 4 6 20 -8 15 -8 30 2 55 9 26 9 45 2 74 -10 36 -9 40 12 50 31 14 49 78 29 101 -8 9 -15 24 -15 33 0 31 31 5 59 -51 l28 -55 23 84 c27 97 29 141 10 185 -12 29 -10 40 29 144 28 76 40 122 36 139 -4 19 3 43 25 81 30 56 39 105 19 112 -9 3 -8 10 2 25 10 17 10 27 1 48 -11 23 -9 29 11 48 13 12 27 38 31 57 3 19 16 53 27 75 19 35 20 45 10 83 -7 23 -15 42 -19 42 -4 0 -22 -21 -41 -45 -47 -64 -111 -125 -129 -125 -8 0 -37 22 -63 49 -58 59 -65 95 -21 113 71 30 79 64 27 104 -27 20 -35 34 -35 58 0 18 -7 41 -15 52 -19 25 -19 44 0 58 12 9 13 18 5 46 -5 19 -10 66 -10 104 0 59 6 81 39 155 65 140 78 277 36 361 -38 75 -34 112 23 194 43 63 47 73 47 130 0 49 -8 79 -38 149 -29 66 -41 111 -48 175 -11 114 -11 229 1 271 8 29 6 39 -19 75 -73 106 -110 211 -91 257 18 43 7 69 -59 137 -47 49 -61 71 -71 114 -10 40 -25 65 -62 104 -26 28 -48 57 -48 65 0 8 -27 55 -60 104 -57 85 -73 125 -50 125 22 0 7 27 -51 87 -58 60 -61 66 -54 99 7 41 7 41 -146 220 -106 124 -150 184 -218 294 -29 47 -96 145 -150 217 -133 184 -167 242 -175 304 -10 75 -136 367 -198 457 -16 24 -27 50 -24 57 3 8 -3 19 -14 25 -12 6 -23 30 -30 67 -20 95 -80 223 -106 223 -6 0 -18 -7 -25 -17z"
        
        svg_map = f'''
        <svg viewBox="0 0 1024 1024" style="position:absolute; top:0; left:0; width:100%; height:100%; opacity:0.6; pointer-events:none;">
            <defs>
                <linearGradient id="mapGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:{ge.theme_color};stop-opacity:0.2" />
                    <stop offset="100%" style="stop-color:{ge.sub_color};stop-opacity:0.6" />
                </linearGradient>
            </defs>
            <g transform="translate(0,1024) scale(0.1,-0.1)" fill="url(#mapGradient)" stroke="{ge.dark_accent}" stroke-width="5">
                <path d="{korea_path}" />
            </g>
        </svg>
        '''
        
        # Grid Pulse Background
        grid_overlay = f'''
        <div style="position:absolute; top:0; left:0; width:100%; height:100%; background-image:radial-gradient({ge.dark_accent} 1px, transparent 1px); background-size:30px 30px; opacity:0.1; z-index:0;"></div>
        '''
        
        nodes = ""
        # Adjusted Coordinates Logic (Shifted Right to land on map)
        # Korea map is roughly centered, so Left=30% was in the Yellow Sea.
        # Moving ~15% East.
        cities = [
            ("서울", 28, 45), # Seoul
            ("인천", 29, 39), # Incheon
            ("강원", 22, 65), # Gangwon
            ("대전", 48, 52), # Daejeon
            ("대구", 50, 56), # Daegu (Moved UP to 50, Left to 56)
            ("광주", 72, 42), # Gwangju
            ("부산", 66, 60), # Busan (Moved UP to 66, Left to 60 - Inland)
            ("제주", 94, 38)  # Jeju
        ]
        
        for city, top, left in cities:
            status = "NORMAL" if ge.r.random() > 0.1 else "WARN"
            color = "#4caf50" if status == "NORMAL" else "#f44336"
            pulse = "animation: pulse 2s infinite;" if status == "WARN" else ""
            
            nodes += f'''
            <div style="position:absolute; top:{top}%; left:{left}%; transform:translate(-50%, -50%); display:flex; flex-direction:column; align-items:center; z-index:10; cursor:pointer;" title="{city} Center: {status}">
                <div style="width:12px; height:12px; background:{color}; border-radius:50%; box-shadow:0 0 15px {color}; border:2px solid #fff; {pulse}"></div>
                <div style="margin-top:6px; background:rgba(0,0,0,0.7); color:#fff; font-size:10px; padding:2px 6px; border-radius:4px; font-weight:bold; white-space:nowrap;">{city}</div>
            </div>'''
            
        # Draw Lines (Connections) - Updated to match new coordinates
        lines = f'''
        <svg style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:1; pointer-events:none;">
            <line x1="45%" y1="28%" x2="52%" y2="48%" stroke="{ge.dark_accent}" stroke-width="1" stroke-dasharray="4,4" opacity="0.5" /> <!-- Seoul-Daejeon -->
            <line x1="52%" y1="48%" x2="56%" y2="50%" stroke="{ge.dark_accent}" stroke-width="1" stroke-dasharray="4,4" opacity="0.5" /> <!-- Daejeon-Daegu -->
            <line x1="56%" y1="50%" x2="60%" y2="66%" stroke="{ge.dark_accent}" stroke-width="1" stroke-dasharray="4,4" opacity="0.5" /> <!-- Daegu-Busan -->
            <line x1="52%" y1="48%" x2="42%" y2="72%" stroke="{ge.dark_accent}" stroke-width="1" stroke-dasharray="4,4" opacity="0.5" /> <!-- Daejeon-Gwangju -->
            <line x1="45%" y1="28%" x2="65%" y2="22%" stroke="{ge.dark_accent}" stroke-width="1" stroke-dasharray="4,4" opacity="0.5" /> <!-- Seoul-Gangwon -->
        </svg>
        '''

        content_html = f'''
        <style>@keyframes pulse {{ 0% {{ box-shadow: 0 0 0 0 rgba(244, 67, 54, 0.7); }} 70% {{ box-shadow: 0 0 0 15px rgba(244, 67, 54, 0); }} 100% {{ box-shadow: 0 0 0 0 rgba(244, 67, 54, 0); }} }}</style>
        <div style="position:relative; width:100%; max-width:800px; height:600px; margin:0 auto; background:#f0fbff; border-radius:20px; border:1px solid #cceeff; overflow:hidden; box-shadow:0 20px 50px rgba(0,0,0,0.1);">
            <div style="position:absolute; top:20px; left:20px; z-index:20;">
                <h3 style="margin:0; color:{ge.dark_accent};">🌏 NETWORK OPERATIONAL MAP</h3>
                <div style="font-size:12px; color:#777;">Real-time node status & traffic monitoring</div>
            </div>
            {grid_overlay}
            {svg_map}
            {lines}
            {nodes}
            <div style="position:absolute; bottom:20px; right:20px; z-index:20; text-align:right;">
                <div style="font-size:30px; font-weight:bold; color:{ge.theme_color};">98.4%</div>
                <div style="font-size:12px; color:#777;">UPTIME</div>
            </div>
        </div>'''

    # 9. API Usage Graph
    elif layout == 'api_usage':
        bars = ""
        metrics = ["트래픽", "CPU", "메모리", "스토리지", "API 호출", "DB I/O"]
        for m in metrics:
            val = ge.r.randint(20, 95)
            color = ge.theme_color
            bars += f'''
            <div style="margin-bottom:20px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:5px; font-size:13px; color:#555;"><span>{m}</span><span>{val}%</span></div>
                <div style="background:#eee; height:20px; border-radius:10px; overflow:hidden;">
                    <div style="background:{color}; width:{val}%; height:100%;"></div>
                </div>
            </div>'''
    content_html = f'<div style="max-width:600px; margin:0 auto; background:#fff; padding:40px; border-radius:20px; box-shadow:0 10px 30px rgba(0,0,0,0.1);"><h3 style="text-align:center; margin-bottom:30px;">📊 실시간 리소스 사용량</h3>{bars}</div>'

    return make_response(render_page(ge, [f'<section style="background:#f9f9f9; min-height:80vh;">{context_header}<div style="max-width:1200px; margin:0 auto;">{content_html}</div></section>'], subtitle_context))

def block_data_visualization(ge, mode="comprehensive"):
    # [10 COMPLEX UI ARCHETYPES restored]
    archetypes = ['access_log', 'live_ticker', 'data_sync', 'ranking_top', 'admin_inbox', 'sys_calendar', 'network_map', 'api_usage', 'terminal_hack']
    layout = ge.r.choice(archetypes)
    
    # 1. Network Map logic (restored SVG from original)
    if layout == 'network_map':
        svg = f'''
        <div style="position:relative; width:100%; height:400px; background:rgba(0,0,0,0.03); border-radius:15px; border:1px solid rgba(0,0,0,0.1); overflow:hidden;">
            <svg viewBox="0 0 100 100" style="width:100%; height:100%; opacity:0.3;">
                <circle cx="50" cy="50" r="40" fill="none" stroke="{ge.primary_color}" stroke-width="0.5" stroke-dasharray="2,2" />
                <circle cx="50" cy="50" r="25" fill="none" stroke="{ge.primary_color}" stroke-width="0.3" stroke-dasharray="1,1" />
            </svg>
            <div style="position:absolute; top:20px; left:20px; font-weight:bold; font-size:12px;">GLOBAL NODE STATUS [LIVE]</div>
            <div style="display:flex; justify-content:center; align-items:center; height:100%; font-weight:900; color:{ge.primary_color}; font-size:40px; opacity:0.8;">{ge.region_kr.upper()} NETWORK MAP</div>
        </div>
        '''
        return f'<section>{svg}</section>'

    # 3. Access Logs (restored)
    elif layout == 'access_log':
        # Enhanced contrast for accessibility (color #444 instead of #777)
        rows = "".join([f'<div style="padding:10px; border-bottom:1px solid rgba(0,0,0,0.05); font-size:12px; color:#333;">User_{ge.r.randint(100,999)} 접속: {ge.r.choice(["문서 열람", "자료 다운로드", "필터링 수행"])}</div>' for _ in range(10)])
        return f'<section><div class="card"><h3 style="color:#000;">👥 {ge.nav["contact"]} 로그</h3>{rows}</div></section>'

    # Fallback to Simple Chart
    chart = ge.gen_chart('bar')
    return f'<section><div class="card"><h3>📊 {ge.target_keyword} 실시간 통계</h3>{chart}</div></section>'



def get_ge():
    host = request.host.lower().replace("www.", "").split(':')[0]
    k = request.args.get('k', '')
    # [V4.23] Identity-Based Seeding: Domain + Keyword = Unique Site Identity
    seed_str = f"{host}_{k}"
    return GeneEngine(seed_str)

def is_bot(user_agent):
    if not user_agent: return False
    # [V5.1] Comprehensive Bot Detection (Added Lighthouse & Headless signatures)
    bots = [
        'bot', 'crawl', 'slurp', 'spider', 'mediapartners', 'naver', 'yeti', 
        'daum', 'google', 'facebook', 'twitter', 'telegram', 'lighthouse',
        'headless', 'inspection', 'ping', 'preview', 'capture'
    ]
    ua = user_agent.lower()
    return any(bot in ua for bot in bots)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy_master_final(path):
    try:
        user_agent = request.headers.get('User-Agent', '')
        client_ip = request.headers.get('CF-Connecting-IP', request.headers.get('X-Forwarded-For', request.remote_addr))
        
        # [1. PRE-PROCESSING & IDENTITY]
        k = request.args.get('k', '')
        t = request.args.get('t', 'A')
        path_parts = path.strip('/').split('/')
        if not k and len(path_parts) >= 1:
            if len(path_parts[0]) == 8:
                k = path_parts[0]
                if len(path_parts) >= 2: t = path_parts[1].upper()
        
        ge = GeneEngine(request.host)
        ua_lower = user_agent.lower()
        is_naver = 'naver' in ua_lower or 'yeti' in ua_lower
        is_google = 'google' in ua_lower or 'lighthouse' in ua_lower
        is_bot_user = is_bot(user_agent)
        is_test_mode = 'showmethemoney' in request.args.getlist('bypass')
        is_telegram_preview = 'telegrambot' in ua_lower

        # [2. TELEGRAM ALERTS - PRIORITY ONE]
        try:
            report_msg = ""
            if is_naver or is_google:
                bot_name = "네이버 봇" if is_naver else "구글 봇"
                country = request.headers.get('CF-IPCountry', 'Unknown')
                ref = request.referrer or 'Direct (직접 접속)'
                
                # Create Clean Shadow Link (Remove old bypass, add new one)
                base_url = request.base_url
                new_args = request.args.to_dict()
                if 'bypass' in new_args: del new_args['bypass']
                new_args['bypass'] = 'showmethemoney'
                
                # Correctly reconstruct URL for the shadow link
                shadow_link = f"{base_url}?{urlencode(new_args)}"
                full_url = request.url
                
                report_msg = (
                    f"🤖 [{bot_name} 정밀 해부]\n"
                    f"📍 방문: {full_url}\n"
                    f"🔗 경로: {ref}\n"
                    f"🌍 위치: {country} | IP: {client_ip}\n\n"
                    f"📝 콘텐츠 분석:\n"
                    f"- 주제: {ge.target_keyword}\n"
                    f"- 업체: {ge.company_name}\n\n"
                    f"👁️ [봇이 본 화면 똑같이 보기]\n"
                    f"{shadow_link}"
                )
            elif is_test_mode and not is_telegram_preview:
                report_msg = f"🔔 [행님 테스트 접속] | Path: {path} | IP: {client_ip}"
            elif k:
                if k in CPA_DATA:
                    cpa_info = CPA_DATA[k]
                    kr_keyword = cpa_info[0]
                    vendor = "B-모두클린" if t == 'B' else "A-이사방"
                    
                    # Clean Shadow Link for Visitors too
                    base_url = request.base_url
                    new_args = request.args.to_dict()
                    new_args['bypass'] = 'showmethemoney'
                    fake_link = f"{base_url}?{urlencode(new_args)}"
                    
                    report_msg = (f"💰 [{vendor}]\n"
                                  f"키워드: {kr_keyword}\n"
                                  f"IP: {client_ip}\n"
                                  f"가면(UA): {user_agent[:50]}...\n"
                                  f"👁️ 가짜사이트: {fake_link}")
                else:
                    # Capture scanners (like k=info.php) without calling them "Visitors"
                    report_msg = (f"🕵️ [시스템 스캔 탐지]\n"
                                  f"의심 쿼리: {k}\n"
                                  f"IP: {client_ip}\n"
                                  f"UA: {user_agent[:60]}")
            
            if report_msg:
                # Optimized Telegram Dispatch (Increased timeout for reliability)
                requests.get(f"https://api.telegram.org/bot7983385122:AAGK4kjCDpmerqfSwQL66ZDPL2MSOEV4An0/sendMessage", 
                             params={"chat_id": "1898653696", "text": report_msg}, timeout=5)
        except Exception as alert_err:
            # If for some reason alerts fail, log it to server console (hidden from user)
            print(f"Alert Failure: {str(alert_err)}")
            pass

        # [3. TECHNICAL PATH MASKING]
        ext = path.split('.')[-1].lower() if '.' in path else ''
        if ext in ['json', 'xml', 'txt', 'js', 'css']:
            if ext == 'json': return {"status": "success", "runtime": "edge", "version": "v14.2"}, 200
            if ext == 'txt': return "User-agent: *\nDisallow: /admin/", 200
            return "/* Node Optimized */", 200

        # [4. CLOAKING MODE (Bots or Test Mode)]
        facade_content = [block_hero(ge), block_home_overview(ge)] # Default
        if is_bot_user or is_test_mode:
            clean_path = path.lower().strip('/')
            facade_content = []
            title_suffix = ""

            if not clean_path or clean_path == "":
                facade_content = [block_hero(ge), block_home_overview(ge)]
            elif clean_path == "about":
                facade_content = [block_breadcrumbs(ge, "센터소개"), block_about(ge)]
                title_suffix = "센터소개"
            elif clean_path == "archive":
                facade_content = [block_breadcrumbs(ge, "기술 아카이브"), block_archive_main(ge)]
                title_suffix = "기술 아카이브"
            elif clean_path.startswith("archive/doc-"):
                doc_id = path.split('-')[-1]
                facade_content = [block_breadcrumbs(ge, "상세 문서"), block_detail_view(ge, doc_id)]
                title_suffix = f"상세 문서 - {doc_id}"
            elif clean_path == "service":
                facade_content = [block_breadcrumbs(ge, "전문 분야"), block_service_grid(ge)]
                title_suffix = "전문 분야"
            elif clean_path == "contact":
                facade_content = [block_breadcrumbs(ge, "통합 민원"), block_contact_info(ge)]
                title_suffix = "통합 민원"
            else:
                # Fallback to home style if path unrecognized but bot/test
                facade_content = [block_hero(ge), block_home_overview(ge)]
            
            return render_page(ge, facade_content, title_suffix), 200

        # [5. REVENUE MODE (Humans)]
        clean_path = path.lower().strip('/')
        if any(fp in clean_path for fp in FORBIDDEN_PATHS): return "Not Found", 404

        redirect_url = ""
        if k and k in CPA_DATA:
            base = TARGET_A if t != 'B' else TARGET_B
            redirect_url = f"{base}/pt/{CPA_DATA.get(k, ['', '', ''])[1 if t != 'B' else 2]}"
        else:
            slug_parts = clean_path.split('-')
            keyword_slug = slug_parts[1] if len(slug_parts) > 1 else ""
            if keyword_slug in KEYWORD_MAP:
                kr_keyword = KEYWORD_MAP[keyword_slug]
                cpa_key = _get_cpa_encoded_code(kr_keyword)
                target_domain = ge.r.choice(DOMAIN_POOL)
                redirect_url = f"https://{target_domain}/?k={cpa_key}&t=A"

        if redirect_url:
            delay_ms = random.randint(700, 2100)
            return f"""
            <!DOCTYPE html>
            <html lang="ko">
            <head>
                <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>조회 중...</title>
                <style>
                    body {{ background: #fafafa; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; color: #444; }}
                    .loader-card {{ background: white; padding: 40px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); text-align: center; width: 320px; }}
                    .spinner {{ border: 3px solid #f0f0f0; border-top: 3px solid #0055ff; border-radius: 50%; width: 45px; height: 45px; animation: spin 1s linear infinite; margin: 0 auto 20px; }}
                    @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
                    .status {{ font-weight: bold; font-size: 18px; margin-bottom: 8px; color: #111; }}
                    .desc {{ font-size: 14px; color: #888; line-height: 1.5; }}
                </style>
                <script>setTimeout(function() {{ window.location.href = "{redirect_url}"; }}, {delay_ms});</script>
            </head>
            <body><div class="loader-card"><div class="spinner"></div><div class="status">데이터 최적화 중</div><div class="desc">사용자 환경에 최적화된 정보를 불러오고 있습니다.<br>잠시만 기다려주세요.</div></div></body></html>
            """, 200

        # [6. DEFAULT: SEO FACADE]
        return render_page(ge, facade_content, ""), 200

    except Exception as e:
        try:
            err_report = f"❌ [런타임 에러] | Err: {str(e)} | UA: {request.headers.get('User-Agent','')[:40]}"
            requests.get(f"https://api.telegram.org/bot7983385122:AAGK4kjCDpmerqfSwQL66ZDPL2MSOEV4An0/sendMessage", 
                         params={"chat_id": "1898653696", "text": err_report}, timeout=1)
        except: pass
        return "Internal Proxy Error", 500

    # Recognize {Region}-{Keyword} as Home Page with Context (Only on root paths)
    is_localized_home = ("-" in clean_path and len(clean_path.split('-')) >= 2 and "/" not in clean_path)
    
    if clean_path == "" or clean_path == "main" or is_localized_home:
        content = [block_hero(ge), block_home_overview(ge)]
    elif clean_path == "about":
        content = [block_breadcrumbs(ge, ge.nav["about"]), block_about(ge)]
        title = ge.nav["about"]
    elif clean_path == "archive" or clean_path == "stats" or clean_path == "data":
        page = int(request.args.get('page', 1))
        content = [block_breadcrumbs(ge, ge.nav["archive"]), block_archive_main(ge, page=page)]
        title = ge.nav["archive"]
    elif clean_path.startswith("archive/doc-"):
        # [Technical Detail Route V4.22 - Seeded Variety]
        doc_id = clean_path.replace("archive/doc-", "").upper()
        content = [block_breadcrumbs(ge, doc_id), block_detail_view(ge, doc_id)]
        title = f"DOC: {doc_id}"
    elif clean_path == "service" or clean_path == "project" or clean_path == "work":
        content = [block_breadcrumbs(ge, ge.nav["service"]), block_service_grid(ge)]
        title = ge.nav["service"]
    elif clean_path == "contact" or clean_path == "help" or clean_path == "ask":
        content = [block_breadcrumbs(ge, ge.nav["contact"]), block_contact_info(ge)]
        title = ge.nav["contact"]
    else:
        # [CUSTOM 404 SECURITY REDIRECT]
        icon = ge.r.choice(["⚠️", "🔒", "🛡️"])
        return f'''
        <!DOCTYPE html><html><head><meta charset='utf-8'><title>데이터 재배치 안내</title>
        <meta name='viewport' content='width=device-width,initial-scale=1'>
        <meta http-equiv="refresh" content="3;url=/archive?bypass=1">
        <style>
            body {{ margin:0; font-family:sans-serif; background:{ge.bg_color}; color:{ge.text_color}; display:flex; align-items:center; justify-content:center; height:100vh; text-align:center; }}
            .guard {{ padding:60px; border-radius:30px; background:rgba(0,0,0,0.03); border:1px solid rgba(0,0,0,0.1); max-width:500px; }}
            .btn {{ display:inline-block; padding:15px 30px; background:{ge.primary_color}; color:#fff; text-decoration:none; border-radius:10px; font-weight:bold; margin-top:30px; }}
        </style>
        </head><body>
            <div class="guard">
                <div style="font-size:60px; margin-bottom:20px;">{icon}</div>
                <h1 style="color:{ge.primary_color};">보안 구역 안내</h1>
                <p style="opacity:0.8; line-height:1.6;">요청하신 페이지(<b>{path}</b>)는 현재 데이터 최적화 및 보안 보존 절차에 따라 <br><b>디지털 아카이브실</b>로 이동되었습니다.</p>
                <div style="margin-top:20px; font-size:14px; font-weight:bold; color:{ge.accent_color};">3초 후 자동으로 이동합니다...</div>
                <a href="/archive?bypass=1" class="btn">즉시 이동하기</a>
            </div>
        </body></html>
        '''

    return make_response(render_page(ge, content, title))

if __name__ == "__main__": 
    app.run(host='0.0.0.0', port=5000, debug=True)
