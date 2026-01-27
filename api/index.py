import requests, hashlib, random, base64, time # v35.1_IP_FIX_FINAL
from flask import Flask, request, render_template_string, Response

app = Flask(__name__)

# [설정] 행님의 중앙 통제실 정보
TELEGRAM_TOKEN = "7983385122:AAGK4kjCDpmerqfSwQL66ZDPL2MSOEV4An0"
CHAT_ID = "1898653696"
GA_ID = "G-1VH7D6BJTD"

# 🛡️ [v19.0] Iron Dome Defense Constants (강력봇 차단 대역)
WHITELIST_IPS = ['61.83.9.20'] # 형님 아이피 (무조건 프리패스)

BOT_UA_KEYWORDS = [
    'bot', 'crawl', 'slurp', 'spider', 'naver', 'daum', 'google', 'phantom', 'headless',
    'vercel-screenshot', 'req/v3', 'python-requests', 'aiohttp', 'curl', 'wget',
    'selenium', 'playwright', 'cypress', 'go-http-client', 'okhttp', 'axios', 'guava'
]
BLOCKED_IP_PREFIXES = [
    '110.93.', '114.111.', '125.209.', '211.249.', '210.89.', '223.130.', 
    '216.73.', '34.', '35.', '52.', '54.', '13.107.', '20.', '192.30.', '140.82.', '185.199.'
]
VISITOR_LOGS = {} 

def is_bot_detected(ip, ua):
    if ip in WHITELIST_IPS:
        return False, None
    
    ua_lower = ua.lower()
    # 1. User-Agent 블랙리스트 (vercel-screenshot, headless 등)
    if any(keyword in ua_lower for keyword in BOT_UA_KEYWORDS):
        return True, f"UA_BLACK({ua[:20]})"
    
    # 2. IP 대역 차단 (해외 클라우드 등)
    if any(ip.startswith(prefix) for prefix in BLOCKED_IP_PREFIXES):
        return True, "IP_BLACK"
    
    # 3. 행동 분석 (1초에 3회 이상 클릭 시 봇으로 간주)
    now = time.time()
    if ip not in VISITOR_LOGS:
        VISITOR_LOGS[ip] = []
    
    # 최근 1초 이내 기록만 유지
    VISITOR_LOGS[ip] = [t for t in VISITOR_LOGS[ip] if now - t < 1.0]
    VISITOR_LOGS[ip].append(now)
    
    if len(VISITOR_LOGS[ip]) > 3:
        return True, "BEHAVIOR_SPEED"
        
    return False, None

# [멀티 도메인 설정] 주소에 따라 간판과 색상을 자동으로 바꿉니더
SITE_CONFIGS = {
    "logistics-dynamics.kr": {"name": "지능형물류수송공학연구원", "color": "#1e40af", "desc": "물류 하중 분산 및 수송 효율 최적화 표준 연구", "font": "Nanum+Gothic"},
    "polymer-cleaning.co.kr": {"name": "고분자화학세정기술표준센터", "color": "#15803d", "desc": "고정밀 화학 세정 공정 및 안전 관리 지침 수립", "font": "Nanum+Myeongjo"},
    "infra-maintenance.kr": {"name": "산업시설 유지관리 기술본부", "color": "#b91c1c", "desc": "국가 기반 시설물 유지보수 및 신뢰성 진단 표준", "font": "Noto+Sans+KR"},
    "fluid-flow.xyz": {"name": "고압정밀유체흐름진단소", "color": "#0369a1", "desc": "고압 유체 역학 기반의 정밀 진단 시스템 연구", "font": "Nanum+Gothic+Coding"},
    "standard-eco.life": {"name": "융복합환경위생표준연구소", "color": "#0d9488", "desc": "환경 위생 인프라 최적화 및 지속가능 공법 연구", "font": "Gowun+Batang"}
}
DEFAULT_CONFIG = {"name": "K-Tech 기술표준연구소", "color": "#00c73c", "desc": "산업 공정 및 기술 표준화 연구 전문", "font": "Nanum+Gothic"}

# 🛡️ [v17.0] Chameleon Deception Engine: 무한 생성 엔진
def get_chameleon_data(host, keyword=""):
    # 서브도메인을 시드로 사용하여 '주소별 고정 랜덤' 실현
    subdomain = host.split('.')[0]
    h = int(hashlib.md5(host.encode()).hexdigest(), 16)
    random.seed(h)
    
    # 1. 기관명 생성 사전
    p_names = ["예진", "한국", "미래", "현대", "통합", "전략", "글로벌", "스마트", "중앙", "차세대", "대한", "산업", "혁신", "정밀"]
    m_names = ["물류", "인프라", "환경", "기술", "시스템", "에너지", "안전", "유체", "공정", "기반", "생활"]
    s_names = ["연구소", "지원센터", "솔루션", "그룹", "개발원", "위원회", "본부", "재단", "연합", "기구"]
    
    # 카테고리별 특화 단어 (키워드가 있을 때 우선 적용)
    if "이사" in keyword or "물류" in keyword:
        m_names = ["물류수송", "화물운송", "적재공학", "수송체계", "이동로직"]
    elif "청소" in keyword or "세정" in keyword:
        m_names = ["고분자세정", "환경위생", "항균공학", "정밀세척", "분자정제"]
    elif "용접" in keyword:
        m_names = ["금속접합", "정밀용접", "접합신뢰성", "특수합금", "열변형제어"]
    elif "막힘" in keyword or "누수" in keyword or "배관" in keyword:
        m_names = ["유체흐름", "지하관로", "비굴착복구", "수압진단", "관로유지"]
    elif "교체" in keyword or "수전" in keyword or "변기" in keyword:
        m_names = ["시설교체", "기기보수", "노후설비", "부품표준", "유지보수"]

    # 도메인 기반 고정 이름 생성
    site_name = f"{random.choice(p_names)} {random.choice(m_names)} {random.choice(s_names)}"
    
    # 2. 디자인 테마 (주소별 다른 색상)
    themes = [
        {"color": "#1e40af", "bg": "#f0f7ff"}, # 블루
        {"color": "#15803d", "bg": "#f0fdf4"}, # 그린
        {"color": "#b91c1c", "bg": "#fef2f2"}, # 레드
        {"color": "#0369a1", "bg": "#f0f9ff"}, # 스카이
        {"color": "#0d9488", "bg": "#f0fdfa"}, # 틸
        {"color": "#7c3aed", "bg": "#f5f3ff"}, # 퍼플
        {"color": "#475569", "bg": "#f8fafc"}  # 그레이
    ]
    theme = random.choice(themes)
    
    # 3. 문서 번호 및 메타 데이터
    doc_id = f"KTS-{random.randint(2024, 2026)}-{h % 10000:04d}"
    
    # 4. 가짜 신원 정보
    last_names = ["김", "이", "박", "최", "정", "강", "조", "윤", "장", "임"]
    ceo = random.choice(last_names) + random.choice(last_names) + random.choice(last_names)
    addr_cities = ["서울시 중구", "경기도 성남시", "대전시 유성구", "인천시 연수구", "부산시 해운대구", "광주시 북구"]
    address = f"{random.choice(addr_cities)} {random.randint(10, 500)}번길 {random.randint(1, 100)} (v{random.randint(2, 5)}.0)"
    phone = f"070-{random.randint(3000, 8999)}-{random.randint(1000, 9999)}"

    return {
        "name": site_name,
        "theme": theme,
        "doc_id": doc_id,
        "ceo": ceo,
        "addr": address,
        "phone": phone,
        "font": random.choice(["Nanum+Gothic", "Nanum+Myeongjo", "Noto+Sans+KR", "Gowun+Batang"])
    }

def text_stylist(text, host):
    h = int(hashlib.md5(host.encode()).hexdigest(), 16) % 3
    # 도메인별 문체 변조 매트릭스
    if h == 1: # 격식 보고서체
        text = text.replace("합니다", "함").replace("입니더", "임").replace("입니다", "임")
    elif h == 2: # 부드러운 구어체
        text = text.replace("한다", "해요").replace("입니더", "예요").replace("입니다", "입니다")
    return text

def send_trace(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        params = {"chat_id": CHAT_ID, "text": msg}
        requests.get(url, params=params, timeout=3)
    except:
        pass

# 🛡️ [v12.0] Tactical A/B DATA_MAP
DATA_MAP = {
    "cleaning": {
        "keywords": ["입주청소", "이사청소", "거주청소", "청소업체", "청소", "입주 청소", "사무실청소", "집청소"],
        "image": "cleaning.jpg",
        "link_A": "https://www.replyalba.co.kr/pt/WwVCgW9E1R",
        "link_B": "https://albarich.com/pt/z2NytCt42i"
    },
    "moving": {
        "keywords": ["이사", "포장이사", "원룸이사", "용달이사", "이삿짐", "포장 이사", "이사업체", "사무실이사", "이사견적"],
        "image": "moving.jpg",
        "link_A": "https://www.replyalba.co.kr/pt/LlocSbdUSY",
        "link_B": "https://albarich.com/pt/zdIDBDSzof"
    },
    "welding": {
        "keywords": ["용접", "출장용접", "알곤용접", "배관용접", "용접업체", "용접수리", "알곤출장용접", "스텐 출장용접"],
        "image": "welding.jpg",
        "link_A": "https://www.replyalba.co.kr/pt/XpBx9dZ5aE",
        "link_B": "https://albarich.com/pt/SROHH97olh"
    },
    "plumbing": {
        "keywords": ["막힘", "누수", "뚫음", "변기막힘", "하수구막힘", "배관", "싱크대막힘", "역류", "누수탐지", "누수전문", "배관 누수", "변기뚫는업체", "배수구 막힘", "하수구 역류", "변기 물 안 내려감", "하수구 뚫는 업체", "변기 뚫는 곳"],
        "image": "plumbing.jpg",
        "link_A": "https://www.replyalba.co.kr/pt/GkVRvxfx1T",
        "link_B": "https://albarich.com/pt/QOaojnBV2v"
    },
    "fixture": {
        "keywords": ["수전교체", "변기교체", "세면대교체", "부속교체", "수전", "세면대", "도기교체", "수전수리", "변기수전", "화장실 변기 교체", "세면대 교체", "변기업체", "수전업체"],
        "image": "fixture.jpg",
        "link_A": "https://www.replyalba.co.kr/pt/FzYOdTzVNw",
        "link_B": "https://albarich.com/pt/vRUcqPts9r"
    },
    "demolition": {
        "keywords": ["철거", "원상복구", "상가철거", "인테리어철거", "가벽철거", "폐기물"],
        "image": "demolition.jpg",
        "link_A": "https://www.replyalba.co.kr/pt/10qHjZwUanF",
        "link_B": "https://albarich.com/pt/NS5WRB4yKa"
    }
}


# 🔑 [v15.0] HASH-BASED SECURE OBFUSCATOR: 솔트 입힌 해시 엔진
SECRET_SALT = "yejin_love_2026"

def get_auto_code(keyword):
    # 키워드 뒤에 우리만 아는 비밀번호(Salt)를 살짝 섞어서 보안 강화
    full_str = keyword + SECRET_SALT
    # MD5 해시 생성 후 앞 6자리만 사용
    return hashlib.md5(full_str.encode()).hexdigest()[:6]

# 🔑 [v23.0] Bulk Automated KEYWORD_MAP
KEYWORD_MAP = {
    # [청소]
    "8cf12edf": "이사청소", "ca4a68a6": "사무실청소", "c8a4cf5a": "입주청소", "d7ea613c": "집청소",
    "cb845113": "청소업체",
    # [이사]
    "faf45575": "이사", "ce8a5ce4": "포장이사", "c8b22f8a": "이사업체", "d108d7a5": "사무실이사",
    "f79702a3": "이사견적", "fa13bc33": "원룸이사", "eeaf8186": "용달이사",
    # [배관/막힘]
    "d0b65aba": "배관누수", "3e848ae6": "수전교체", "66cb8240": "누수탐지",
    "8e2996c7": "배관 누수", "81edc02c": "변기막힘", "8745563e": "하수구막힘", "617a0005": "누수탐지",
    "5d19986d": "변기뚫는업체", "a0ef0c00": "싱크대막힘", "e6d02452": "배수구 막힘", "35467a5c": "하수구 역류",
    "9ce613e1": "변기 물 안 내려감", "68943f44": "하수구 뚫는 업체", "c8abc514": "변기 뚫는 곳",
    # [용접]
    "dc19f4ea": "용접", "af5f2375": "출장용접", "c4c5ee7e": "용접업체", "4a2f6816": "배관용접",
    "87a3472b": "알곤용접", "63b2da0a": "용접수리", "20186798": "알곤출장용접", "ef310430": "스텐 출장용접",
    # [교체/수리]
    "ffbfdc28": "변기수전", "be4adb64": "수전교체", "a01f1db0": "변기교체", "b1585a85": "화장실 변기 교체",
    "c2bddbcc": "세면대 교체", "b6f6c35f": "변기업체", "3e750243": "수전업체",
    # [기존 호환성]
    "f2a3b4c5": "누수탐지", "d1e2f3g4": "입주청소", "h5i6j7k8": "포장이사"
}

# 🤖 [v18.0] REPORT_SNIPPETS: 문서 변조용 재료 창고
REPORT_SNIPPETS = {
    "cleaning": [
        "고분자 화학 성분을 활용한 정밀 세정 공정은 주거 환경의 위생 표준을 획기적으로 개선합니다.",
        "미세먼지 및 잔류 오염물질 제거를 위해 나노 단위의 계면활성제 반응 최적화가 필수적입니다.",
        "화학적 거동 분석을 통해 산성 및 알칼리성 세제의 중화 과정을 정밀하게 제어해야 합니다.",
        "주거 공간의 공기질 개선을 위한 항균 코팅 기술은 박테리아 증식을 효율적으로 제어하는 성과를 보였습니다.",
        "표면 장력 제어 공법을 통한 코팅막 형성은 오염 방지 및 유지관리 비용 절감의 핵심입니다."
    ],
    "moving": [
        "화물 적재 하중의 동역학적 분산 알고리즘은 운송 중 파손율을 실시간으로 저감하는 공학적 기초가 됩니다.",
        "이동 경로의 최적 최단 경로 탐색 알고리즘은 에너지 효율 증대와 운영 비용 최적화에 기여합니다.",
        "고충 부하 분배 시스템을 통한 중량물 상하차 공정은 작업자의 안전 보건 및 시설 보호를 보장합니다.",
        "물류 수송 체계의 표준화 작업은 체계적인 자산 보호 및 운송 신뢰성을 높이는 핵심 지표입니다.",
        "충격 흡수 프레임워크를 적용한 특수 적재 공법은 정밀 기기 및 가구 보호에 탁월한 효능을 보입니다."
    ],
    "welding": [
        "금속 접합부의 열변형 제어 알고리즘은 구조물의 장기적 신뢰성과 내구성을 보장하는 핵심 기술입니다.",
        "분자 조직 결합 메커니즘 분석을 통해 용접 HAZ 구간의 물리적 변형을 최소화하는 공정을 수립했습니다.",
        "비파괴 탐상 기술(UT/RT) 기반의 품질 검증 시스템은 미세 균열 전파를 사전 차단하는 역할을 수행합니다.",
        "특수 합금용 플럭스 최적 배합비는 산화 방지 및 접합 강도 극대화를 위한 필수 연구 결과입니다.",
        "고온 고압 환경 하에서의 금속 결합 안정성 테스트를 통해 안전 계수 2.5 이상의 표준을 달성했습니다."
    ],
    "plumbing": [
        "도시 지하 관로 유체 흐름 분석을 통해 배관 내부의 압력 강하와 역류 현상을 정밀하게 진단합니다.",
        "비굴착 복구 공학을 적용한 고압 제팅 공법은 기존 매설물의 손상 없이 내부 이물질을 완벽히 제거합니다.",
        "레이놀즈 수 기반의 유체 역학 시뮬레이션은 배관 설계의 최적 구배 및 유속 결정에 활용됩니다.",
        "초음파 누수 탐지 알고리즘은 미세한 음향 파형의 변이를 감지하여 0.01mm 급의 균열 위치를 특정합니다.",
        "배관 내벽 나노 코팅 기술은 이물질 흡착을 방지하고 유체 저항을 최소화하여 펌핑 효율을 높입니다."
    ],
    "fixture": [
        "노후 설비의 기기 보수 및 교체 표준 가이드라인은 안정적인 주거 수자원 관리를 위한 필수 지침입니다.",
        "수압 제어 밸브의 압력 평형 최적 설계는 급격한 온도 변화 및 유량 변동 요인을 사전 차단합니다.",
        "환경 친화적 절수 기술 표준은 ISO 인증 기준에 부합하는 수자원 보존 효율을 입증하였습니다.",
        "시설 교체 시 발생하는 소음 및 진동 차단 공법은 주거 쾌적성 향상을 위한 핵심 시공 표준입니다.",
        "부위별 부품 호환성 표준화(Standardization)는 유지보수 편의성과 장기 운영 안정성을 보장합니다."
    ]
}

# 🔐 [v15.0] 역방향 조회를 위한 자동 해시 맵 생성
REVERSE_HASH_MAP = {}
def build_hash_map():
    # 1. 모든 알려진 키워드 수량 확보
    all_kws = set(KEYWORD_MAP.values())
    for data in DATA_MAP.values():
        all_kws.update(data['keywords'])
    
    # 2. 해시 코드 -> 키워드 맵핑 자동 생성
    for kw in all_kws:
        h_code = get_auto_code(kw)
        REVERSE_HASH_MAP[h_code] = kw

build_hash_map()

# 🔄 [v16.0] DYNAMIC BASE64 DECODER: 무한 확장 실시간 엔진
def decode_keyword(encoded_str):
    try:
        # 1. Base64 암호를 푼다 (URL 안전 모드)
        padding = '=' * (4 - len(encoded_str) % 4)
        decoded_bytes = base64.urlsafe_b64decode(encoded_str + padding)
        decoded_str = decoded_bytes.decode('utf-8')
        
        # 2. 비밀 열쇠가 맞는지 확인하고 한글만 추출한다
        if "|" in decoded_str:
            keyword, key = decoded_str.split("|")
            if key == SECRET_SALT:
                return keyword # '입주청소' 추출 성공!
        return None
    except:
        return None

def get_keyword(code):
    # 1. 동적 Base64 디코딩 (v16.0) - 장부 필요 없음!
    dynamic_kw = decode_keyword(code)
    if dynamic_kw:
        return dynamic_kw
    
    # 2. 해시 코드 매칭 (v15.0)
    if code in REVERSE_HASH_MAP:
        return REVERSE_HASH_MAP[code]
    
    # 3. 수동 코드 매칭 (v14.0)
    if code in KEYWORD_MAP:
        return KEYWORD_MAP[code]
    
    # 4. 그냥 키워드인 경우 (100% 하위 호환)
    return code

# 🛡️ [v11.0] SEO Deception Engine

# 🤖 50개 이상의 기술 논문 데이터베이스 (2023 ~ 2026)
DOC_DATABASE = [
    # 2026
    {"id": "KTS-2026-06", "cat": "hvac", "title": "지능형 공조 시스템의 열역학적 에너지 효율 분석", "date": "2026-01-26", "desc": "냉난방 사이클 성적계수(COP) 극대화 및 스마트 제어 알고리즘"},
    {"id": "KTS-2026-05", "cat": "homecare", "title": "주거 환경 위생 최적화 및 항균 코팅 기술 표준", "date": "2026-01-25", "desc": "휘발성 유기화합물(VOCs) 저감 및 광촉매 지속성 데이터 보고서"},
    {"id": "KTS-2026-04", "cat": "drain", "title": "도시 지하 관로 유체 흐름 및 비굴착 복구 공학", "date": "2026-01-24", "desc": "레이놀즈 수 분석 및 고압 분사 공법 유지관리 매뉴얼"},
    {"id": "KTS-2026-03", "cat": "welding", "title": "금속 접합부의 열변형 제어 및 신뢰성 검증 표준", "date": "2026-01-22", "desc": "TIG/아크 용접 HAZ 조직 변화 제어 및 PWHT 공정 검증"},
    {"id": "KTS-2026-02", "cat": "cleaning", "title": "고분자 화학 세정 공법 및 분자 정제 매뉴얼", "date": "2026-01-20", "desc": "고효율 계면활성제 적용 나노 단위 세정 기술 표준 지침"},
    {"id": "KTS-2026-01", "cat": "moving", "title": "물류 수송 체계의 동역학적 하중 분산 연구", "date": "2026-01-15", "desc": "화물 운송 주선 사업의 적재 최적화 알고리즘 및 표준 공정 분석 자료"},
    # 2025
    {"id": "KTS-2025-18", "cat": "structural", "title": "산업용 대형 구조물의 응력 해석 및 균열 전파 억제 기술", "date": "2025-12-15", "desc": "FEM 기반 집중 하중 분산 메커니즘 및 미세 조직 보강 표준"},
    {"id": "KTS-2025-17", "cat": "material", "title": "신소재 복합 합금의 고온 산화 방지 및 산 부식 내성 검증", "date": "2025-11-20", "desc": "세라믹 코팅 및 전기화학적 부식 방지 시스템 유효성 보고서"},
    {"id": "KTS-2025-16", "cat": "robotics", "title": "자동화 라인의 협동 로봇 안전 토크 제어 알고리즘", "date": "2025-10-25", "desc": "인간-로봇 공존 환경에서의 충돌 조기 감지 및 충격 완화 프레임워크"},
    {"id": "KTS-2025-15", "cat": "automation", "title": "AI 기반 제조 공정 이상 징후 감지 및 예지 보전 시스템", "date": "2025-10-12", "desc": "딥러닝 시계열 분석 및 설비 고장 예측 기술 표준 로드맵"},
    {"id": "KTS-2025-14", "cat": "energy", "title": "차세대 전고체 배터리 팩의 열관리 시스템 최적화 설계", "date": "2025-09-28", "desc": "상변화 물질(PCM)을 이용한 고온 방전 시 셀 간 온도 편차 억제 기술"},
    {"id": "KTS-2025-13", "cat": "fluid", "title": "초임계 유체를 이용한 반도체 세정 공정의 오염 입자 제거 기작", "date": "2025-09-10", "desc": "표면 장력 제로화 기술을 활용한 미세 패턴 손상 방지 기술 표준"},
    {"id": "KTS-2025-12", "cat": "safety", "title": "산업 현장 중대 재해 방지를 위한 휴먼 에러 제어 공학", "date": "2025-09-05", "desc": "작업자 인지 심리 모델 기반 안전 인터락 설계 지침"},
    {"id": "KTS-2025-11", "cat": "coating", "title": "해양 구조물용 초발수 방오 코팅제의 내구성 평가", "date": "2025-08-14", "desc": "나노 구조 제어를 통한 표면 에너지 최적화 및 장기 방식 성능 검증"},
    {"id": "KTS-2025-10", "cat": "thermal", "title": "데이터 센터 액침 냉각 시스템의 열전달 성능 향상 연구", "date": "2025-07-22", "desc": "비전도성 유체 내 비등 열전달 계수 측정 및 냉각 효율 매뉴얼"},
    # 2024
    {"id": "KTS-2024-12", "cat": "acoustic", "title": "소음 저감을 위한 메타 물질 구조 설계 및 음향 임피던스 분석", "date": "2024-12-10", "desc": "특정 주파수 대역의 완전 흡음 실현을 위한 구조적 최적화 기술"},
    {"id": "KTS-2024-11", "cat": "plasma", "title": "대기압 플라즈마 표면 처리를 통한 고분자 접착력 향상 기술", "date": "2024-11-15", "desc": "표면 관능기 활성화를 이용한 이종 재료 간 계면 결합력 강화 공정"},
    {"id": "KTS-2024-10", "cat": "optics", "title": "정밀 측정을 위한 레이저 간섭계의 오차 보정 알고리즘", "date": "2024-10-20", "desc": "나노 미터 급 변위 측정을 위한 환경 변수 보상 및 신호 처리 표준"},
    {"id": "KTS-2024-09", "cat": "vibration", "title": "압전 소자를 이용한 능동형 진동 억제 시스템 구현", "date": "2024-09-12", "desc": "정밀 공작 기계의 실시간 진동 감쇄를 위한 폐루프 제어 전략"},
    {"id": "KTS-2024-08", "cat": "polymer", "title": "재활용 플라스틱의 물성 복원을 위한 첨가제 배합 기술", "date": "2024-08-05", "desc": "순환 경제 대응을 위한 재생 원료 품질 표준 및 가공 매뉴얼"},
    {"id": "KTS-2024-07", "cat": "concrete", "title": "초고강도 콘크리트의 열적 거동 및 폭렬 방지 공법", "date": "2024-07-15", "desc": "내화 성능 향상을 위한 폴리프로필렌 섬유 혼입량 최적화 자료"},
    {"id": "KTS-2024-06", "cat": "lubrication", "title": "극압 환경 하에서의 합성 윤활유 트라이볼로지 측정", "date": "2024-06-22", "desc": "고하중 기어 박스의 마찰 마모 저감을 위한 첨가제 반응 기작 분석"},
    {"id": "KTS-2024-05", "cat": "turbine", "title": "가스 터빈 블레이드의 냉각 구멍 형상에 따른 필름 냉각 효율", "date": "2024-05-18", "desc": "고온 가스 유입 방지를 위한 분사구 각도 및 형상 설계 표준"},
    {"id": "KTS-2024-04", "cat": "additive", "title": "금속 3D 프린팅 공정의 잔류 응력 분포 수치 해석", "date": "2024-04-10", "desc": "적층 제조 시 발생하는 레이저 열원 모델링 및 변형 방지 지침"},
    {"id": "KTS-2024-03", "cat": "semicon", "title": "EUV 노광 공정용 펠리클의 투과율 및 기계적 강도 검증", "date": "2024-03-05", "desc": "차세대 반도체 마스크 보호를 위한 나노 박막 적층 기술 표준"},
    {"id": "KTS-2024-02", "cat": "wind", "title": "해상 풍력 발전기 타워의 피로 수명 예측 모델링", "date": "2024-02-14", "desc": "파랑 하중 및 풍하중 복합 작용 시의 연결부 건전성 평가 자료"},
    {"id": "KTS-2024-01", "cat": "hydrogen", "title": "수소 충전소용 고압 저장 탱크의 취성 파괴 저항성", "date": "2024-01-20", "desc": "700bar 압력 조건 하에서의 소재 투과성 및 장기 내구도 시험 표준"},
    # 2023 
    {"id": "KTS-2023-12", "cat": "smart", "title": "스마트 팩토리용 산업용 사물인터넷(IIoT) 보안 표준", "date": "2023-12-15", "desc": "에지 컴퓨팅 환경에서의 종단간 암호화 및 비인가 접근 차단 규격"},
    {"id": "KTS-2023-11", "cat": "gear", "title": "정밀 감속기의 치형 기하학적 오차 분석 및 보정 기술", "date": "2023-11-28", "desc": "로봇 관절용 사이클로이드 치형의 전달 오차 최소화 설계 지침"},
    {"id": "KTS-2023-10", "cat": "vacuum", "title": "초고진공 펌프 블레이드의 기체 동역학적 성능 최적화", "date": "2023-10-12", "desc": "분자 유동 대역에서의 압축비 향상을 위한 날개 형상 수치 해석"},
    {"id": "KTS-2023-09", "cat": "foundry", "title": "주물 공정의 응고 결함 예측을 위한 열전달 계수 측정", "date": "2023-09-22", "desc": "수축공 및 다공성 결함 방지를 위한 금형 냉각 시스템 설계 가이드"},
    {"id": "KTS-2023-08", "cat": "filtration", "title": "대기 오염 방지용 대용량 백필터의 압력 손실 저감 기술", "date": "2023-08-14", "desc": "필터 표면 처리 및 분진 박리 효율 향상을 위한 펄스 제팅 최적화"},
    {"id": "KTS-2023-07", "cat": "pipeline", "title": "천연가스 배관망의 정적 및 동적 누출 감지 알고리즘", "date": "2023-07-05", "desc": "질량평형법 및 음파 감지법을 결합한 고신뢰성 배관 관리 표준"},
    {"id": "KTS-2023-06", "cat": "solar", "title": "페로브스카이트 태양전지의 봉지 공정 기술 및 투습도 검증", "date": "2023-06-18", "desc": "차세대 박막 태양광 셀의 장기 안정성 확보를 위한 캡슐화 기술"},
    {"id": "KTS-2023-05", "cat": "aerospace", "title": "위성용 가벼운 탄소 복합재 구조물의 모드 해석", "date": "2023-05-25", "desc": "발사 시 발생하는 극심한 가속도 및 진동 하에서의 고유 진동수 확인"},
    {"id": "KTS-2023-04", "cat": "hydraulics", "title": "건설 기계용 고압 유압 호스의 파열 압력 가속 시험", "date": "2023-04-12", "desc": "아레니우스 모델을 적용한 고무 소재 노화 예측 및 교체 주기 표준"},
    {"id": "KTS-2023-03", "cat": "biotech", "title": "세포 배양 배양기(Bioreactor) 내부의 산소 전달 계수 분석", "date": "2023-03-20", "desc": "대량 생산용 바이오 공정의 교반 날개 형상 및 임펠러 속도 최적화"},
    {"id": "KTS-2023-02", "cat": "ship", "title": "LNG 운반선 화물창의 극저온 멤브레인 용접 건전성", "date": "2023-02-15", "desc": "-163℃ 환경 하에서의 슬로싱 하중 대응 및 자동 용접 품질 표준"},
    {"id": "KTS-2023-01", "cat": "mining", "title": "광산 현장 건설 장비의 자율 주행용 장애물 회피 경로 계획", "date": "2023-01-10", "desc": "비정형 지형에서의 Lidar 데이터 융합 및 실시간 궤적 생성 알고리즘"}
]

# 🎨 [v13.0] 익스트림 위장 엔진: 요염한 데이터 생성기
def get_dynamic_chart(host):
    h = int(hashlib.md5(host.encode()).hexdigest(), 16)
    random.seed(h)
    points = [random.randint(20, 130) for _ in range(5)]
    color = random.choice(["#00c73c", "#1e40af", "#b91c1c", "#0d9488", "#0369a1"])
    path = f"M50,{points[0]} L150,{points[1]} L250,{points[2]} L350,{points[3]} L450,{points[4]}"
    circles = "".join([f'<circle cx="{i*100+50}" cy="{points[i]}" r="5" fill="#1e293b"/>' for i in range(5)])
    return f"""
    <svg viewBox="0 0 500 150" style="background:#fff; border:1px solid #eee; border-radius:8px; margin:20px 0;">
        <path d="{path}" fill="none" stroke="{color}" stroke-width="4"/>
        {circles}
    </svg>
    """

def get_term(host, key):
    h = int(hashlib.md5(host.encode()).hexdigest(), 16)
    random.seed(h)
    matrix = {
        "resources": ["기술표준자료", "데이터 아카이브", "표준 문서 보관소", "공정 매뉴얼 센터", "기술 백서"],
        "about": ["연구소 소개", "기관 안내", "연구원 개요", "센터 히스토리", "조직 가이드"],
        "portal": ["메인 포털", "종합 관제 센터", "허브 포털", "통합 정보실", "중앙 데이터 센터"],
        "report": ["기술 보고서", "표준 지침서", "연구 성과물", "공정 분석서", "기술 규격서"]
    }
    return random.choice(matrix.get(key, ["정보"]))

BASE_HTML = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <script async src="https://www.googletagmanager.com/gtag/js?id={{ ga_id }}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', '{{ ga_id }}');
    </script>
    <link href="https://fonts.googleapis.com/css2?family={{ font_family }}&display=swap" rel="stylesheet">
    <meta charset="UTF-8">
    <title>{{ title }} | {{ site_name }}</title>
    <style>
        body { font-family: '{{ font_family | replace("+", " ") }}', sans-serif; margin: 0; background: #f8fafc; color: #334155; letter-spacing: -0.5px; }
        .{{ cls_nav }} { background: white; padding: 20px 10%; display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid {{ theme_color }}; position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 5px rgba(0,0,0,0.02); }
        .{{ cls_nav }} a { text-decoration: none; color: #1e293b; font-weight: bold; margin-left: 30px; font-size: 14px; transition: 0.2s; }
        .{{ cls_nav }} a:hover { color: {{ theme_color }}; }
        .{{ cls_footer }} { background: #0f172a; color: #94a3b8; padding: 40px 10%; text-align: center; font-size: 11px; line-height: 2; border-top: 1px solid #1e293b; }
        .{{ cls_content }} { max-width: 1000px; margin: 40px auto; padding: 0 20px; min-height: 500px; }
        .section { background: white; padding: 35px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.04); margin-bottom: 25px; border: 1px solid #f1f5f9; }
        .card { display: block; background: white; padding: 25px; border: 1px solid #e2e8f0; border-radius: 8px; text-decoration: none; color: inherit; transition: 0.2s; position: relative; overflow: hidden; }
        .card:hover { border-color: {{ theme_color }}; transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.08); }
        .card h3 { margin: 0 0 10px 0; font-size: 18px; color: #1e293b; }
        .pagination { display: flex; justify-content: center; margin-top: 30px; gap: 10px; }
        .pagination a { padding: 8px 15px; border: 1px solid #ddd; background: white; color: #333; text-decoration: none; border-radius: 5px; }
        .pagination a.active { background: {{ theme_color }}; color: white; border-color: {{ theme_color }}; }
    </style>
</head>
<body>
    <div style="display:none;">DEPLOY_VER: v27.0</div>
    <div class="{{ cls_nav }}">
        <a href="/" style="font-size: 22px; font-weight: 900; color: {{ theme_color }}; margin: 0; letter-spacing: -1.5px;">{{ site_name }}</a>
        <div>
            <a href="/about">{{ terms.about }}</a>
            <a href="/resources">{{ terms.resources }}</a>
            <a href="/careers">인재채용</a>
            <a href="/contact">고객센터</a>
        </div>
    </div>
    <div class="{{ cls_content }}">{{ body_content | safe }}</div>
    <div class="{{ cls_footer }}">
        (주){{ site_name }} | {{ identity.addr }} | 대표자: {{ identity.ceo }} | T. {{ identity.phone }}<br>
        Copyright © 2026 {{ site_name }}. All rights reserved.
    </div>
</body>
</html>
"""

def get_config():
    host = request.host.split(':')[0].replace('www.', '')
    conf = SITE_CONFIGS.get(host, DEFAULT_CONFIG).copy()
    
    # 🛡️ [v11.0/v13.0] 신원 및 DOM 랜덤화 데이터 생성
    h = hashlib.md5(host.encode()).hexdigest()
    random.seed(int(h[:8], 16))
    conf['identity'] = identity_gen(host)
    conf['cls_nav'] = "n_" + h[:5]
    conf['cls_footer'] = "f_" + h[5:10]
    conf['cls_content'] = "c_" + h[10:15]
    conf['terms'] = {
        "resources": get_term(host, "resources"),
        "about": get_term(host, "about"),
        "portal": get_term(host, "portal"),
        "report": get_term(host, "report")
    }
    
    return conf

# 🛡️ [v18.0] Deep Deception: 무한 문서 변조 엔진
def get_unique_report_content(host, category):
    h = int(hashlib.md5(host.encode()).hexdigest(), 16)
    random.seed(h)
    snippets = REPORT_SNIPPETS.get(category, REPORT_SNIPPETS["cleaning"])
    random.shuffle(snippets)
    def modulate(text):
        if h % 3 == 0: return text.replace("합니다.", "함.").replace("있습니다.", "있음.")
        elif h % 3 == 1: return text.replace("합니다.", "하는 것으로 나타났습니다.").replace("있습니다.", "있는 것으로 판단됩니다.")
        return text
    modulated_snippets = [modulate(s) for s in snippets]
    report_text = ""
    for i, s in enumerate(modulated_snippets):
        report_text += f"<p style='line-height:1.8; margin-bottom:15px; text-align:justify;'>{s}</p>"
        if i == 1:
            report_text += f"<div style='background:#f1f5f9; padding:15px; border-radius:5px; font-size:12px; margin:20px 0; color:#475569; border-left:4px solid #94a3b8;'><strong>[분석 데이터 ID: {h % 99999:05d}]</strong><br>본 섹션의 데이터는 국가 표준 가이드라인 v{random.randint(2,4)}.0에 따라 검증되었습니다.</div>"
    return report_text

# 🛡️ [v22.0] Honeypot (허니팟): 봇 전용 고퀄리티 위장 페이지
def get_honeypot_response(cham):
    body = f"""
    <div class="section" style="max-width:400px; margin: 100px auto; padding:40px; border-top: 5px solid {cham['theme']['color']};">
        <h2 style="text-align:center; color:#1e293b; margin-bottom:30px;">K-Tech Intranet Login</h2>
        <div style="margin-bottom:20px;">
            <label style="display:block; font-size:13px; color:#64748b; margin-bottom:5px;">Employee ID</label>
            <input type="text" style="width:100%; padding:10px; border:1px solid #e2e8f0; border-radius:5px; background:#f8fafc;" disabled value="Guest_Member">
        </div>
        <div style="margin-bottom:30px;">
            <label style="display:block; font-size:13px; color:#64748b; margin-bottom:5px;">Security Password</label>
            <input type="password" style="width:100%; padding:10px; border:1px solid #e2e8f0; border-radius:5px; background:#f8fafc;" disabled value="********">
        </div>
        <button style="width:100%; padding:12px; background:#94a3b8; color:white; border:none; border-radius:5px; font-weight:bold; cursor:not-allowed;">Access Restricted</button>
        <p style="margin-top:20px; font-size:12px; color:#ef4444; text-align:center;">비인가 IP 대역에서의 접근이 감지되었습니다.<br>보안팀에 의해 해당 세션의 로그가 기록됩니다.</p>
    </div>
    """
    return render_template_string(BASE_HTML, title="Intranet Gateway", body_content=body, site_name=cham['name'], theme_color="#94a3b8", ga_id=GA_ID, font_family=cham['font'], identity=cham, terms={"about": "Login", "resources": "System"}, cls_nav="n_lock", cls_footer="f_lock", cls_content="c_lock")

# 🛡️ [v22.0] Deep Deception: 고퀄리티 리포트 빌더 (버튼 유무 선택 가능)
def get_professional_report(host, category, show_cta=False, target_url="#"):
    cham = get_chameleon_data(host, category)
    report_text = get_unique_report_content(host, category)
    
    cta_html = ""
    if show_cta:
        # 🛡️ [v22.0] Ultimate Stealth "The Ghost": 스크롤해야만 버튼이 생성됨
        # 정적 크롤러, 헤드리스 브라우저는 절대로 이 버튼을 구경할 수 없습니더.
        b64_url = base64.b64encode(target_url.encode()).decode()
        cta_html = f"""
        <div id="cta-immediate-zone" style="margin-top:40px;"></div>
        <script>
            (function() {
                const u = atob('{b64_url}');
                const zone = document.getElementById('cta-immediate-zone');
                zone.innerHTML = `
                    <div style="padding:40px; background:#f8fafc; border:2px solid {cham['theme']['color']}; border-radius:12px; text-align:center; box-shadow: 0 10px 25px rgba(0,0,0,0.05);">
                        <h3 style="margin-bottom:12px; color:#1e293b; font-size:20px;">{category.upper()} 분야 공식 기술 지원 센터</h3>
                        <p style="font-size:15px; color:#64748b; margin-bottom:25px;">검증된 공정 표준에 기반하여 해당 지역의 즉시 대응 서비스를 제공합니다.</p>
                        <a href="${{u}}" target="_blank" style="display:inline-block; padding:18px 60px; background:{cham['theme']['color']}; color:white; text-decoration:none; font-weight:bold; border-radius:8px; font-size:18px; box-shadow:0 8px 15px rgba(0,0,0,0.1); width: 80%; max-width: 400px;">전문 상담 및 현장 지원 신청</a>
                    </div>
                `;
            })();
        </script>
        <style>@keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}</style>
        """

    content = f"""
    <div class="section">
        <div style="float:right; border:4px solid #e74c3c; color:#e74c3c; padding:10px 20px; font-weight:bold; transform:rotate(12deg); font-size:24px; border-radius:5px;">CONFIDENTIAL</div>
        <p style="color:{cham['theme']['color']}; font-weight:bold; font-size:14px;">[기술인프라 보존번호: {cham['doc_id']}]</p>
        <h1 style="color:#1e293b; margin-top:15px; font-size:32px; letter-spacing:-1px;">{category.upper()} 고등 기술 공정 분석 리포트 <span style="font-size:10px; color:#eee;">v34.0_SYNC</span></h1>
        <hr style="border:0; border-top:3px solid {cham['theme']['color']}22; margin:30px 0;">
        
        <div style="font-size:16px; color:#334155;">{report_text}</div>
        
        {cta_html}
        
        <p style="font-size:12px; color:#94a3b8; margin-top:50px; border-top:1px solid #eee; padding-top:20px; line-height:1.6;">
            ※ 본 문서는 {cham['name']}의 엄격한 보안 지침에 따라 관리되는 내부 성과물입니다. 비인가자에 의한 무단 복제 및 전재를 엄격히 금하며, 위반 시 법적 책임이 따를 수 있습니다. (Hash: {hashlib.md5(host.encode()).hexdigest()[:16].upper()})
        </p>
    </div>
    """
    return render_template_string(BASE_HTML, title=f"{category.upper()} 기술 보고서", body_content=content, site_name=cham['name'], theme_color=cham['theme']['color'], ga_id=GA_ID, font_family=cham['font'], identity=cham, terms={"about": "연구소 소개", "resources": "기술자료"}, cls_nav="n_doc", cls_footer="f_doc", cls_content="c_doc")

# 🛡️ [v19.0] Honeypot (허니팟): 봇 전용 가짜 페이지
def get_honeypot_response(cham):
    body = f"""
    <div class="section" style="text-align:center; padding: 100px 20px;">
        <h1 style="color:#e74c3c; font-size:40px;">⚠️ Access Denied</h1>
        <p style="margin-top:20px; color:#334155; font-size:18px;">비정상적인 접속 활동이 감지되어 시스템 접근이 차단되었습니다.</p>
        <div style="margin:40px auto; max-width:500px; padding:30px; background:#fef2f2; border:1px solid #fee2e2; border-radius:12px;">
            <p style="font-size:15px; color:#b91c1c;"><strong>보안 정책 위반 (Code: {random.randint(10000, 99999)})</strong><br>자동화된 크롤링 또는 비정상적인 속도의 요청이 감지되었습니다.</p>
        </div>
        <p style="font-size:13px; color:#94a3b8;">본 조치는 시스템 안정성을 위해 자동으로 실행되었으며, 24시간 후 해제됩니다.</p>
        <div style="margin-top:40px;" id="spinner">
            <div style="border:5px solid #f3f3f3; border-top:5px solid #e74c3c; border-radius:50%; width:40px; height:40px; animation: spin 1s linear infinite; margin:0 auto;"></div>
        </div>
    </div>
    <style>@keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}</style>
    """
    return render_template_string(BASE_HTML, title="Security Alert", body_content=body, site_name=cham['name'], theme_color="#e74c3c", ga_id=GA_ID, font_family=cham['font'], identity=cham, terms={"about": "안내", "resources": "보안"}, cls_nav="n_err", cls_footer="f_err", cls_content="c_err")

@app.route('/')
def index():
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    ua = request.headers.get('User-Agent', '').lower()
    host = request.host.split(':')[0].replace('www.', '')
    
    # 🕵️ [v19.0] Iron Dome 전방위 봇 탐지 (UA + IP + Behavioral)
    keyword_raw = request.args.get('k', '')
    keyword = get_keyword(keyword_raw) or ""
    
    is_bot, bot_reason = is_bot_detected(user_ip, ua)
    
    cham = get_chameleon_data(host, keyword)
    
    # 🚩 [CASE 0] 봇이 확실하면 즉시 허니팟으로 던지기
    if is_bot:
        report = f"🛡️ [차단] {bot_reason} 탐지!\n🌐 주소: {request.host}\n📍 IP: {user_ip}\n🕵️ UA: {ua[:40]}..."
        send_trace(report)
        return get_honeypot_response(cham)
    type_code = request.args.get('t', 'A')

    # 🚩 [CASE 1] 봇이거나 키워드 없는 직접 접속 -> "전문 연구소 메인"
    if is_bot or not keyword:
        report = f"🚩 [{cham['name']}] 위장홈 접속 (탐지된 봇: {is_bot})\n🌐 주소: {request.host}\n📍 IP: {user_ip}\n🕵️ UA: {ua[:40]}..."
        send_trace(report)
        
        # 가짜 연구물 카드 풀 (6개 중 3~5개 랜덤 선택)
        all_cards = [
            f'<a href="/a/moving" class="card" style="text-decoration:none;"><h3>물류 수송 체계 보고서</h3><p style="color:#666; font-size:13px;">{cham["doc_id"]} 공계 분석 자료</p></a>',
            f'<a href="/a/cleaning" class="card" style="text-decoration:none;"><h3>환경 세정 기술 지침</h3><p style="color:#666; font-size:13px;">ISO-9001 인증 표준 매뉴얼</p></a>',
            f'<a href="/a/welding" class="card" style="text-decoration:none;"><h3>접합 신뢰성 검증서</h3><p style="color:#666; font-size:13px;">안전 진단 및 비파괴 테스트</p></a>',
            f'<a href="/a/plumbing" class="card" style="text-decoration:none;"><h3>관로 유체 역학 데이터</h3><p style="color:#666; font-size:13px;">지하 시설물 유지보수 공학</p></a>',
            f'<a href="/a/fixture" class="card" style="text-decoration:none;"><h3>주거 보건 위생 지표</h3><p style="color:#666; font-size:13px;">친환경 자재 및 시공 표준</p></a>'
        ]
        random.seed(int(hashlib.md5(host.encode()).hexdigest()[:8], 16))
        count = random.randint(3, 5) # 주소마다 3개~5개 사이로 다르게 나옴
        selected_cards = random.sample(all_cards, count)
        random.shuffle(selected_cards)

        body = f"""
        <div class="section" style="text-align:center; background:{cham['theme']['bg']}">
            <h1 style="color:{cham['theme']['color']}; border-bottom:3px solid {cham['theme']['color']}; display:inline-block;">{cham['name']}</h1>
            <p style="margin-top:10px; font-weight:bold;">{cham['doc_id']} 기술 표준 통합 아카이브</p>
            <div style="margin-top:15px; font-size:12px; color:#94a3b8;">최종 업데이트: 2026-01-27 | 보안등급: 대외주의</div>
        </div>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:20px;">
            {"".join(selected_cards)}
        </div>
        """
        resp = Response(render_template_string(BASE_HTML, title=cham['name'], body_content=body, site_name=cham['name'], theme_color=cham['theme']['color'], site_desc=cham['doc_id'], ga_id=GA_ID, font_family=cham['font'], identity=cham, terms={"about": "연구소 소개", "resources": "기술자료"}, cls_nav="n_main", cls_footer="f_main", cls_content="c_main"))
        resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        return resp

    # 🎯 [CASE 2] 진짜 손님 -> [중요] 절대 자동 리다이렉트 안함. 리포트 페이지로 이동 후 버튼 노출.
    selected_data = None
    category_key = "cleaning"
    for cat, data in DATA_MAP.items():
        if any(k in keyword for k in data['keywords']):
            selected_data = data
            category_key = cat
            break
    if not selected_data:
        selected_data = DATA_MAP["cleaning"]
    
    final_url = selected_data['link_A'] # 기본 A업체 접수처
    if type_code == 'B': final_url = selected_data['link_B']
    
    send_trace(f"?썳截?[V35_1_IP_FIX] 肄붾뱶: {keyword_raw}\n?렞 寃곗젙 ?ㅼ썙?? {keyword} ({category_key})\n?뱧 IP: {user_ip}\n?빑截?UA: {ua}\n?뵕 ?ㅼ젣 CPA留곹겕: {final_url}")
    
    # 🚩 [v20.0] 리포트 페이지에 상담 신청 버튼을 넣어서 반환 (자동 이동 금지)
    resp = Response(get_professional_report(host, category_key, show_cta=True, target_url=final_url))
    resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return resp

@app.route('/resources')
def resources():
    host = request.host.split(':')[0].replace('www.', '')
    cham = get_chameleon_data(host)
    page = request.args.get('page', 1, type=int)
    per_page = 10
    total_docs = len(DOC_DATABASE)
    total_pages = (total_docs + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    docs = DOC_DATABASE[start:end]

    list_html = ""
    for d in docs:
        list_html += f"""
        <div style="padding:22px; border-bottom:1px solid #eee;">
            <a href="/a/{d['cat']}" style="text-decoration:none; color:{cham['theme']['color']}; font-weight:bold;">[{d['id']}] {d['title']}</a>
            <p style="font-size:13px; color:#666; margin-top:8px;">{d['desc']}</p>
        </div>
        """
    
    pagination_html = '<div class="pagination">'
    for p in range(1, total_pages + 1):
        active_class = 'active' if p == page else ''
        pagination_html += f'<a href="/resources?page={p}" class="{active_class}">{p}</a>'
    pagination_html += '</div>'

    content = f"""
    <div class="section">
        <h1 style="color:{cham['theme']['color']}; border-bottom:3px solid {cham['theme']['color']}; display:inline-block;">기술 자료실</h1>
        <div style="margin-top:20px;">{list_html}</div>
        {pagination_html}
    </div>
    """
    return render_template_string(BASE_HTML, title="기술 자료실", body_content=content, site_name=cham['name'], theme_color=cham['theme']['color'], ga_id=GA_ID, font_family=cham['font'], identity=cham, terms={"about": "연구소 소개", "resources": "기술자료"}, cls_nav="n_res", cls_footer="f_res", cls_content="c_res")

@app.route('/about')
def about():
    host = request.host.split(':')[0].replace('www.', '')
    cham = get_chameleon_data(host)
    content = f'<div class="section"><h1>연구소 소개</h1><p style="line-height:2;">{cham["name"]}는 {request.host} 네트워크를 통한 산업 전반의 기술 표준화 및 신뢰성 진단을 선도합니다.</p></div>'
    return render_template_string(BASE_HTML, title="연구소 소개", body_content=content, site_name=cham['name'], theme_color=cham['theme']['color'], ga_id=GA_ID, font_family=cham['font'], identity=cham, terms={"about": "연구소 소개", "resources": "기술자료"}, cls_nav="n_ab", cls_footer="f_ab", cls_content="c_ab")

@app.route('/careers')
def careers():
    host = request.host.split(':')[0].replace('www.', '')
    cham = get_chameleon_data(host)
    content = f'<div class="section"><h1>인재채용</h1><p>{cham["name"]}와 함께할 차세대 기술 분석가 및 시스템 운영 효율화 전문가를 모십니다.</p></div>'
    return render_template_string(BASE_HTML, title="인재채용", body_content=content, site_name=cham['name'], theme_color=cham['theme']['color'], ga_id=GA_ID, font_family=cham['font'], identity=cham, terms={"about": "연구소 소개", "resources": "기술자료"}, cls_nav="n_car", cls_footer="f_car", cls_content="c_car")

@app.route('/contact')
def contact():
    host = request.host.split(':')[0].replace('www.', '')
    cham = get_chameleon_data(host)
    content = f'<div class="section"><h1>고객센터</h1><p>관리자 문의: admin@{host} | T. {cham["phone"]}</p></div>'
    return render_template_string(BASE_HTML, title="고객센터", body_content=content, site_name=cham['name'], theme_color=cham['theme']['color'], ga_id=GA_ID, font_family=cham['font'], identity=cham, terms={"about": "연구소 소개", "resources": "기술자료"}, cls_nav="n_con", cls_footer="f_con", cls_content="c_con")

@app.route('/<company>/<category>')
@app.route('/a/<category>')
def check_visitor(category, company=None):
    host = request.host.split(':')[0].replace('www.', '')
    cham = get_chameleon_data(host)
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    ua = request.headers.get('User-Agent', '').lower()
    
    # 🛡️ [v19.0] 내부 링크에서도 봇 감지 가동
    is_bot, bot_reason = is_bot_detected(user_ip, ua)
    if is_bot:
        return get_honeypot_response(cham)
    
    # 카테고리 매칭 (상담 신청 버튼용 링크 추출)
    target_data = DATA_MAP.get(category.lower())
    real_url = target_data['link_A'] if target_data else "#"
    
    # 🚩 [v20.0] 봇에게는 CPA 링크가 전혀 없는 리포트를, 사람에게는 버튼 있는 리포트를 줍니다.
    # 단, /a/ 경로는 봇 검수용이므로 '기본적으로' 버튼을 숨기되, 봇이 아닌 게 확실하면 보여줄 수도 있습니다.
    # 여기서는 좀 더 안전하게 '봇이 아닐 때만' 버튼을 노출하도록 처리합니다.
    show_button = not is_bot 
    
    resp = Response(get_professional_report(host, category.lower(), show_cta=show_button, target_url=real_url))
    resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return resp

# --- 🗺️ [신규] 사이트맵(Sitemap) 자동 생성 엔진 ---
@app.route('/sitemap.xml')
def sitemap():
    conf = get_config()
    host = request.host.split(':')[0]
    # 봇이 긁어갈 전체 페이지 목록 작성
    pages = [
        {'loc': '/', 'freq': 'daily', 'pri': '1.0'},
        {'loc': '/about', 'freq': 'monthly', 'pri': '0.5'},
        {'loc': '/resources', 'freq': 'daily', 'pri': '0.8'},
        {'loc': '/careers', 'freq': 'monthly', 'pri': '0.5'},
        {'loc': '/contact', 'freq': 'monthly', 'pri': '0.5'}
    ]
    
    # DB에 있는 모든 카테고리별 기술 문서 경로를 지도에 추가
    categories = list(set(d['cat'] for d in DOC_DATABASE))
    for cat in categories:
        pages.append({'loc': f'/a/{cat}', 'freq': 'weekly', 'pri': '0.7'})

    # XML 형식으로 지도 그리기
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for p in pages:
        xml += f'  <url>\n    <loc>https://{host}{p["loc"]}</loc>\n'
        xml += f'    <changefreq>{p["freq"]}</changefreq>\n'
        xml += f'    <priority>{p["pri"]}</priority>\n  </url>\n'
    xml += '</urlset>'
    
    return Response(xml, mimetype='application/xml')

if __name__ == "__main__":
    app.run()
