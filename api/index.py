import requests, hashlib, random, base64, time # v35.10_FINAL_REPAIR
from flask import Flask, request, render_template_string, Response

app = Flask(__name__)

# [???] ???????? ????????
TELEGRAM_TOKEN = "7983385122:AAGK4kjCDpmerqfSwQL66ZDPL2MSOEV4An0"
CHAT_ID = "1898653696"
GA_ID = "G-1VH7D6BJTD"

# ????[v19.0] Iron Dome Defense Constants (???????? ????
WHITELIST_IPS = ['61.83.9.20'] # ??? ?????(???????????)

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
    # 1. User-Agent ????????(vercel-screenshot, headless ??
    if any(keyword in ua_lower for keyword in BOT_UA_KEYWORDS):
        return True, f"UA_BLACK({ua[:20]})"
    
    # 2. IP ??????? (??? ?????? ??
    if any(ip.startswith(prefix) for prefix in BLOCKED_IP_PREFIXES):
        return True, "IP_BLACK"
    
    # 3. ??? ??? (1??? 3????? ??? ??????????)
    now = time.time()
    if ip not in VISITOR_LOGS:
        VISITOR_LOGS[ip] = []
    
    # ??? 1????? ????????
    VISITOR_LOGS[ip] = [t for t in VISITOR_LOGS[ip] if now - t < 1.0]
    VISITOR_LOGS[ip].append(now)
    
    if len(VISITOR_LOGS[ip]) > 3:
        return True, "BEHAVIOR_SPEED"
        
    return False, None

# [v35.6] Site Configurations (Restored)
SITE_CONFIGS = {
    "logistics-dynamics.kr": {"name": "전략 물류 재단", "color": "#1e40af", "desc": "첨단 물류 시스템 연구 및 최적화 기관", "font": "Nanum+Gothic"},
    "polymer-cleaning.co.kr": {"name": "혁신 환경 연구소", "color": "#15803d", "desc": "친환경 세정 기술 및 공정 개발", "font": "Nanum+Myeongjo"},
    "infra-maintenance.kr": {"name": "차세대 기술 솔루션", "color": "#b91c1c", "desc": "도시 기반 시설 유지보수 전문 기업", "font": "Noto+Sans+KR"},
    "fluid-flow.xyz": {"name": "유체 역학 데이터센터", "color": "#0369a1", "desc": "배관 및 수자원 관리 시스템 분석", "font": "Nanum+Gothic+Coding"},
    "standard-eco.life": {"name": "표준 생활 환경", "color": "#0d9488", "desc": "주거 환경 개선을 위한 표준 지침 수립", "font": "Gowun+Batang"}
}
DEFAULT_CONFIG = {"name": "K-Tech 통합 기술원", "color": "#00c73c", "desc": "국가 기술 표준 가이드라인 제공", "font": "Nanum+Gothic"}

# 🦎 [v35.6] Chameleon Deception Engine: Restored Logic
def get_chameleon_data(host, keyword=""):
    # 호스트명에서 자동으로 '그럴듯한 이름' 생성
    subdomain = host.split('.')[0]
    h = int(hashlib.md5(host.encode()).hexdigest(), 16)
    random.seed(h)
    
    # 1. 기관명 생성
    p_names = ["한국", "전국", "미래", "청정", "우리", "바른", "착한", "제일", "나눔", "행복", "안심", "신뢰", "명품"]
    m_names = ["기술", "연구", "개발", "솔루션", "시스템", "환경", "산업", "공학", "데이터", "관리", "지원"]
    s_names = ["공사", "기업", "센터", "협회", "연구소", "개발원", "본부", "지사", "사업소", "연합"]
    
    # 키워드별 특화 (없으면 랜덤)
    if "청소" in keyword or "입주" in keyword:
        m_names = ["환경", "클린", "청소", "위생", "방역", "세정", "미화"]
    elif "이사" in keyword or "용달" in keyword:
        m_names = ["물류", "운송", "이사", "이삿짐", "용달", "화물"]
    elif "용접" in keyword:
        m_names = ["용접", "산업", "특수", "금속", "배관", "설비"]
    elif "배관" in keyword or "누수" in keyword or "막힘" in keyword:
        m_names = ["배관", "설비", "하수구", "보수", "누수", "수질"]
    elif "수전" in keyword or "변기" in keyword or "교체" in keyword:
        m_names = ["시설", "설비", "보수", "수리", "교체", "주거"]

    # 최종 기관명 조합
    site_name = f"{random.choice(p_names)} {random.choice(m_names)} {random.choice(s_names)}"
    
    # 2. 테마 색상 (랜덤이지만 고정)
    themes = [
        {"color": "#1e40af", "bg": "#f0f7ff"}, # 블루
        {"color": "#15803d", "bg": "#f0fdf4"}, # 그린
        {"color": "#b91c1c", "bg": "#fef2f2"}, # 레드
        {"color": "#0369a1", "bg": "#f0f9ff"}, # 스카이
        {"color": "#0d9488", "bg": "#f0fdfa"}, # 틸
        {"color": "#7c3aed", "bg": "#f5f3ff"}, # 퍼플
        {"color": "#475569", "bg": "#f8fafc"}  # 슬레이트
    ]
    theme = random.choice(themes)
    
    # 3. 문서 고유 번호 생성
    doc_id = f"KTS-{random.randint(2024, 2026)}-{h % 10000:04d}"
    
    # 4. 담당자 정보 생성
    last_names = ["김", "이", "박", "최", "정", "강", "조", "윤", "장"]
    ceo = random.choice(last_names) + random.choice(last_names) + random.choice(last_names)
    addr_cities = ["서울시 강남구", "경기도 분당구", "인천시 송도", "부산시 해운대구", "대구시 수성구", "대전시 유성구"]
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
    # 단순 반환 (복잡한 변조 로직 제거하여 안정성 확보)
    return text

def send_trace(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        params = {"chat_id": CHAT_ID, "text": msg}
        requests.get(url, params=params, timeout=3)
    except:
        pass

# ????[v12.0] Tactical A/B DATA_MAP
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
        "keywords": ["막힘", "누수", "뚫음", "변기막힘", "하수구막힘", "배관", "싱크대막힘", "역류", "누수탐지", "누수전문", "배관 누수", "변기뚫는업체", "배수구 막힘", "하수구 역류", "변기 물 안 내려감", "하수구 뚫는 업체", "변기 뚫는 곳", "배관누수"],
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


# ?? [v15.0] HASH-BASED SECURE OBFUSCATOR: ??? ??? ??? ???
SECRET_SALT = "yejin_love_2026"

def get_auto_code(keyword):
    # ???????? ???????? ??????(Salt)????? ???????? ???
    full_str = keyword + SECRET_SALT
    # MD5 ??? ??? ????6????????
    return hashlib.md5(full_str.encode()).hexdigest()[:6]

# ?? [v23.0] Bulk Automated KEYWORD_MAP
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

# ?? [v18.0] REPORT_SNIPPETS: ??? ????? ??? ???
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

# ?? [v15.0] ????????????? ??? ??? ?????
REVERSE_HASH_MAP = {}
def build_hash_map():
    # 1. ??? ????????????? ???
    all_kws = set(KEYWORD_MAP.values())
    for data in DATA_MAP.values():
        all_kws.update(data['keywords'])
    
    # 2. ??? ??? -> ???????? ??? ???
    for kw in all_kws:
        h_code = get_auto_code(kw)
        REVERSE_HASH_MAP[h_code] = kw

build_hash_map()

# ?? [v16.0] DYNAMIC BASE64 DECODER: ??? ??? ????????
def decode_keyword(encoded_str):
    try:
        # 1. Base64 ???????? (URL ??? ???)
        padding = '=' * (4 - len(encoded_str) % 4)
        decoded_bytes = base64.urlsafe_b64decode(encoded_str + padding)
        decoded_str = decoded_bytes.decode('utf-8')
        
        # 2. ??? ????? ????? ?????? ???????????
        if "|" in decoded_str:
            keyword, key = decoded_str.split("|")
            if key == SECRET_SALT:
                return keyword # '??????' ??? ???!
        return None
    except:
        return None

def get_keyword(code):
    # 1. ??? Base64 ?????(v16.0) - ??? ??? ???!
    dynamic_kw = decode_keyword(code)
    if dynamic_kw:
        return dynamic_kw
    
    # 2. ??? ??? ??? (v15.0)
    if code in REVERSE_HASH_MAP:
        return REVERSE_HASH_MAP[code]
    
    # 3. ??? ??? ??? (v14.0)
    if code in KEYWORD_MAP:
        return KEYWORD_MAP[code]
    
    # 4. ??? ?????? ??? (100% ??? ???)
    return code

# ????[v11.0] SEO Deception Engine

# ?? 50?????????? ??? ????????? (2023 ~ 2026)
DOC_DATABASE = [
    # 2026
    {"id": "KTS-2026-06", "cat": "hvac", "title": "고효율 냉난방 공조 시스템의 에너지 절감 효과 분석", "date": "2026-01-26", "desc": "성능계수(COP) 극대화를 위한 열교환기 최적화 설계 연구"},
    {"id": "KTS-2026-05", "cat": "homecare", "title": "실내 공기질 개선을 위한 광촉매 필터 적용 사례", "date": "2026-01-25", "desc": "휘발성유기화합물(VOCs) 제거 성능 및 항균 지속성 평가"},
    {"id": "KTS-2026-04", "cat": "drain", "title": "배수 관로 내부 이물질 퇴적 메커니즘 분석", "date": "2026-01-24", "desc": "유체전산역학(CFD)을 이용한 임계 유속 도출 및 설계 반영"},
    {"id": "KTS-2026-03", "cat": "welding", "title": "특수 합금 용접부의 응력 부식 균열 방지 기술", "date": "2026-01-22", "desc": "TIG/MIG 용접 시 HAZ 구간의 미세조직 제어 및 열처리(PWHT) 최적화"},
    {"id": "KTS-2026-02", "cat": "cleaning", "title": "초미세 표면 세정을 위한 나노 기포 활용 연구", "date": "2026-01-20", "desc": "반도체 및 정밀 기기 세정을 위한 캐비테이션 효과 분석"},
    {"id": "KTS-2026-01", "cat": "moving", "title": "물류 운송 중 진동 저감을 위한 포장재 완충 특성", "date": "2026-01-15", "desc": "동적 충격 전달율 저감을 위한 다공성 폴리머 소재 적용성 평가"},
    # 2025
    {"id": "KTS-2025-18", "cat": "structural", "title": "건축 구조물의 내진 성능 향상을 위한 댐퍼 설계", "date": "2025-12-15", "desc": "비선형 시간 이력 해석을 통한 감쇠 장치 성능 검증"},
    {"id": "KTS-2025-17", "cat": "material", "title": "친환경 건축 자재의 LCC(생애주기비용) 분석", "date": "2025-11-20", "desc": "재활용 골재 사용 시 구조적 안정성 및 경제성 평가"},
    {"id": "KTS-2025-16", "cat": "robotics", "title": "산업용 로봇의 정밀 제어를 위한 적응형 PID 튜닝", "date": "2025-10-25", "desc": "다축 로봇 팔의 궤적 추적 오차 최소화 알고리즘 구현"},
    {"id": "KTS-2025-15", "cat": "automation", "title": "스마트 팩토리 구축을 위한 엣지 컴퓨팅 활용", "date": "2025-10-12", "desc": "제조 데이터의 실시간 처리를 위한 분산 처리 아키텍처 설계"},
    {"id": "KTS-2025-14", "cat": "energy", "title": "차세대 ESS 시스템의 열폭주 방지 냉각 기술", "date": "2025-09-28", "desc": "상변화물질(PCM)을 이용한 배터리 모듈 온도 균일화 해석"},
    {"id": "KTS-2025-13", "cat": "fluid", "title": "난류 유동장 내에서의 입자 거동 시물레이션", "date": "2025-09-10", "desc": "라그랑주 관점 입자 추적법을 이용한 집진 효율 예측"},
    {"id": "KTS-2025-12", "cat": "safety", "title": "건설 현장 안전 관리를 위한 IoT 센서 네트워크", "date": "2025-09-05", "desc": "BLE/LoRa 기반 작업자 위치 추적 및 위험 구역 경보 시스템"},
    {"id": "KTS-2025-11", "cat": "coating", "title": "내식성 향상을 위한 세라믹 코팅층의 밀착력 평가", "date": "2025-08-14", "desc": "스크래치 테스트 및 염수 분무 시험을 통한 수명 예측"},
    {"id": "KTS-2025-10", "cat": "thermal", "title": "전자부품 방열 성능 개선을 위한 히트싱크 최적화", "date": "2025-07-22", "desc": "핀 형상 및 배열에 따른 자연대류 열전달 계수 측정"},
    # 2024
    {"id": "KTS-2024-12", "cat": "acoustic", "title": "층간 소음 저감을 위한 바닥 구조재의 차음 성능", "date": "2024-12-10", "desc": "중량 충격음 및 경량 충격음 저감재의 동탄성 계수 분석"},
    {"id": "KTS-2024-11", "cat": "plasma", "title": "대기압 플라즈마를 이용한 표면 친수성 개질 연구", "date": "2024-11-15", "desc": "접촉각 측정을 통한 표면 에너지 변화 및 접착력 향상 검증"},
    {"id": "KTS-2024-10", "cat": "optics", "title": "고해상도 디스플레이용 광학 필름의 투과율 개선", "date": "2024-10-20", "desc": "나노 임프린트 공정을 이용한 반사 방지 패턴 제작"},
    {"id": "KTS-2024-09", "cat": "vibration", "title": "회전 기계의 불평형 진동 진단 및 밸런싱 기법", "date": "2024-09-12", "desc": "주파수 스펙트럼 분석을 통한 결함 주파수 식별 및 교정"},
    {"id": "KTS-2024-08", "cat": "polymer", "title": "생분해성 고분자의 기계적 물성 및 분해 거동", "date": "2024-08-05", "desc": "토양 매립 시 미생물 분해 속도 및 인장 강도 변화 측정"},
    {"id": "KTS-2024-07", "cat": "concrete", "title": "고강도 콘크리트의 내화 성능 향상을 위한 방안", "date": "2024-07-15", "desc": "PP섬유 혼입률에 따른 폭열 방지 효과 실험적 검증"},
    {"id": "KTS-2024-06", "cat": "lubrication", "title": "극압 환경 하에서의 윤활유 마모 방지 성능 평가", "date": "2024-06-22", "desc": "4-Ball 마모 시험을 통한 마찰 계수 및 마모흔 직경 분석"},
    {"id": "KTS-2024-05", "cat": "turbine", "title": "가스 터빈 블레이드의 냉각 효율 향상 연구", "date": "2024-05-18", "desc": "막 냉각 홀 형상 최적화를 통한 단열 효율 증대 해석"},
    {"id": "KTS-2024-04", "cat": "additive", "title": "금속 3D 프린팅 부품의 미세조직 및 강도 특성", "date": "2024-04-10", "desc": "SLM 공정 변수에 따른 기공률 및 인장 특성 상관관계"},
    {"id": "KTS-2024-03", "cat": "semicon", "title": "반도체 공정용 초순수 공급 시스템의 오염 제어", "date": "2024-03-05", "desc": "TOC 및 파티클 저감을 위한 이온 교환 수지 재생 주기 최적화"},
    {"id": "KTS-2024-02", "cat": "wind", "title": "해상 풍력 발전기의 지지 구조물 피로 해석", "date": "2024-02-14", "desc": "조류 및 파력 하중을 고려한 자켓 구조물의 S-N 선도 분석"},
    {"id": "KTS-2024-01", "cat": "hydrogen", "title": "수소 저장 탱크의 라이너 재질별 수소 투과 특성", "date": "2024-01-20", "desc": "고압 수소 환경 하에서의 폴리머 라이너 기체 차단성 평가"}
]

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
        "resources": ["기술자료", "기술지원", "엔지니어링 자료", "표준 문서", "연구 성과"],
        "about": ["연구소 소개", "보유 기술", "조직도", "인사말", "비전 및 철학"],
        "portal": ["기술 표준 포털", "통합 정보 시스템", "연구 데이터베이스", "전문가 네트워크"],
        "report": ["기술 보고서", "분석 리포트", "공정 데이터", "검증 자료", "시험 성적서"]
    }
    return random.choice(matrix.get(key, ["자료"]))

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
            <a href="/careers">??????</a>
            <a href="/contact">??????</a>
        </div>
    </div>
    <div class="{{ cls_content }}">{{ body_content | safe }}</div>
    <div class="{{ cls_footer }}">
        (??{{ site_name }} | {{ identity.addr }} | ?????: {{ identity.ceo }} | T. {{ identity.phone }}<br>
        Copyright ? 2026 {{ site_name }}. All rights reserved.
    </div>
</body>
</html>
"""

def get_config():
    host = request.host.split(':')[0].replace('www.', '')
    conf = SITE_CONFIGS.get(host, DEFAULT_CONFIG).copy()
    
    # ????[v11.0/v13.0] ??? ??DOM ?????????????
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

# ????[v18.0] Deep Deception: ??? ??? ???????
def get_unique_report_content(host, category):
    h = int(hashlib.md5(host.encode()).hexdigest(), 16)
    random.seed(h)
    snippets = REPORT_SNIPPETS.get(category, REPORT_SNIPPETS["cleaning"])
    random.shuffle(snippets)
    def modulate(text):
        if h % 3 == 0: return text.replace("?????", "??").replace("??????.", "???.")
        elif h % 3 == 1: return text.replace("?????", "??? ??????????????.").replace("??????.", "??? ?????????????")
        return text
    modulated_snippets = [modulate(s) for s in snippets]
    report_text = ""
    for i, s in enumerate(modulated_snippets):
        report_text += f"<p style='line-height:1.8; margin-bottom:15px; text-align:justify;'>{s}</p>"
        if i == 1:
            report_text += f"<div style='background:#f1f5f9; padding:15px; border-radius:5px; font-size:12px; margin:20px 0; color:#475569; border-left:4px solid #94a3b8;'><strong>[??? ?????ID: {h % 99999:05d}]</strong><br>????????????? ??? ??? ???????? v{random.randint(2,4)}.0????? ???????????.</div>"
    return report_text

# ????[v22.0] Honeypot (?????: ????? ?????????? ?????
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
        <p style="margin-top:20px; font-size:12px; color:#ef4444; text-align:center;">????? IP ???????? ????????????????<br>?????????? ??? ?????????? ????????</p>
    </div>
    """
    return render_template_string(BASE_HTML, title="Intranet Gateway", body_content=body, site_name=cham['name'], theme_color="#94a3b8", ga_id=GA_ID, font_family=cham['font'], identity=cham, terms={"about": "Login", "resources": "System"}, cls_nav="n_lock", cls_footer="f_lock", cls_content="c_lock")

# ????[v22.0] Deep Deception: ??????????????? (??? ??? ??? ????
def get_professional_report(host, category, show_cta=False, target_url="#"):
    cham = get_chameleon_data(host, category)
    report_text = get_unique_report_content(host, category)
    
    cta_html = ""
    if show_cta:
        # ????[v22.0] Ultimate Stealth "The Ghost": ????????? ??????????
        # ??? ????? ?????? ?????????????????????????????????.
        b64_url = base64.b64encode(target_url.encode()).decode()
        cta_html = f"""
        <div id="cta-immediate-zone" style="margin-top:40px;"></div>
        <script>
            (function() {
                const u = atob('{b64_url}');
                const zone = document.getElementById('cta-immediate-zone');
                zone.innerHTML = `
                    <div style="padding:40px; background:#f8fafc; border:2px solid {cham['theme']['color']}; border-radius:12px; text-align:center; box-shadow: 0 10px 25px rgba(0,0,0,0.05);">
                        <h3 style="margin-bottom:12px; color:#1e293b; font-size:20px;">{category.upper()} ??? ??? ??? ???????</h3>
                        <p style="font-size:15px; color:#64748b; margin-bottom:25px;">????? ??? ??????????? ??? ????? ??? ?????????? ????????</p>
                        <a href="${{u}}" target="_blank" style="display:inline-block; padding:18px 60px; background:{cham['theme']['color']}; color:white; text-decoration:none; font-weight:bold; border-radius:8px; font-size:18px; box-shadow:0 8px 15px rgba(0,0,0,0.1); width: 80%; max-width: 400px;">??? ??? ????? ???????</a>
                    </div>
                `;
            })();
        </script>
        <style>@keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}</style>
        """

    content = f"""
    <div class="section">
        <div style="float:right; border:4px solid #e74c3c; color:#e74c3c; padding:10px 20px; font-weight:bold; transform:rotate(12deg); font-size:24px; border-radius:5px;">CONFIDENTIAL</div>
        <p style="color:{cham['theme']['color']}; font-weight:bold; font-size:14px;">[??????????????: {cham['doc_id']}]</p>
        <h1 style="color:#1e293b; margin-top:15px; font-size:32px; letter-spacing:-1px;">{category.upper()} 고등 기술 공정 분석 리포트 <span style="font-size:10px; color:#eee;">v34.0_SYNC</span></h1>
        <hr style="border:0; border-top:3px solid {cham['theme']['color']}22; margin:30px 0;">
        
        <div style="font-size:16px; color:#334155;">{report_text}</div>
        
        {cta_html}
        
                <p style="font-size:12px; color:#94a3b8; margin-top:50px; border-top:1px solid #eee; padding-top:20px; line-height:1.6;">
            본 문서는 {cham['name']}의 엄격한 보안 지침에 따라 관리되는 내부 성과물입니다. 비인가자에 의한 무단 복제 및 전재를 엄격히 금하며, 위반 시 법적 책임이 따를 수 있습니다. (Hash: {hashlib.md5(host.encode()).hexdigest()[:16].upper()})
        </p>
    </div>
    """
    return render_template_string(BASE_HTML, title=f"{category.upper()} 고등 기술 공정 분석 리포트", body_content=content, site_name=cham['name'], theme_color=cham['theme']['color'], ga_id=GA_ID, font_family=cham['font'], identity=cham, terms={"about": "연구소 소개", "resources": "기술자료"}, cls_nav="n_doc", cls_footer="f_doc", cls_content="c_doc")

# 🕸️ [v35.9] Honeypot (봇 전용 함정 페이지)
def get_honeypot_response(cham):
    body = f"""
    <div class="section" style="text-align:center; padding: 100px 20px;">
        <h1 style="color:#e74c3c; font-size:40px;">⛔ Access Denied</h1>
        <p style="margin-top:20px; color:#334155; font-size:18px;">비정상적인 접근이 감지되어 접속이 일시 차단되었습니다.</p>
        <div style="margin:40px auto; max-width:500px; padding:30px; background:#fef2f2; border:1px solid #fee2e2; border-radius:12px;">
            <p style="font-size:15px; color:#b91c1c;"><strong>보안 정책 위반 (Code: {random.randint(10000, 99999)})</strong><br>자동화된 수집 도구 또는 비정상적인 트래픽 패턴이 식별되었습니다.</p>
        </div>
        <p style="font-size:13px; color:#94a3b8;">차단이 실수라고 판단되시면 관리자에게 문의바라며, 24시간 모니터링 중입니다.</p>
        <div style="margin-top:40px;" id="spinner">
            <div style="border:5px solid #f3f3f3; border-top:5px solid #e74c3c; border-radius:50%; width:40px; height:40px; animation: spin 1s linear infinite; margin:0 auto;"></div>
        </div>
    </div>
    <style>@keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}</style>
    """
    return render_template_string(BASE_HTML, title="Security Alert", body_content=body, site_name=cham['name'], theme_color="#e74c3c", ga_id=GA_ID, font_family=cham['font'], identity=cham, terms={"about": "차단안내", "resources": "보안정책"}, cls_nav="n_err", cls_footer="f_err", cls_content="c_err")


@app.route('/')
def index():
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    ua = request.headers.get('User-Agent', '').lower()
    host = request.host.split(':')[0].replace('www.', '')
    
    # ????[v19.0] Iron Dome ?????????? (UA + IP + Behavioral)
    keyword_raw = request.args.get('k', '')
    keyword = get_keyword(keyword_raw) or ""
    
    is_bot, bot_reason = is_bot_detected(user_ip, ua)
    
    cham = get_chameleon_data(host, keyword)
    
    # ?? [CASE 0] ??? ?????? ??? ?????????????
    if is_bot:
        report = f"????[???] {bot_reason} ???!\n?? ???: {request.host}\n?? IP: {user_ip}\n????UA: {ua[:40]}..."
        send_trace(report)
        return get_honeypot_response(cham)
    type_code = request.args.get('t', 'A')

    # ?? [CASE 1] ?????? ???????? ??? ??? -> "??? ????????"
    if is_bot or not keyword:
        report = f"?? [{cham['name']}] ???????? (??????? {is_bot})\n?? ???: {request.host}\n?? IP: {user_ip}\n????UA: {ua[:40]}..."
        send_trace(report)
        
        # ???????????? ?? (6????3~5????? ???)
        all_cards = [
            f'<a href="/a/moving" class="card" style="text-decoration:none;"><h3>??? ??? ??? ?????/h3><p style="color:#666; font-size:13px;">{cham["doc_id"]} ??? ??? ???</p></a>',
            f'<a href="/a/cleaning" class="card" style="text-decoration:none;"><h3>??? ??? ??? ????/h3><p style="color:#666; font-size:13px;">ISO-9001 ??? ??? ?????/p></a>',
            f'<a href="/a/welding" class="card" style="text-decoration:none;"><h3>??? ??????????</h3><p style="color:#666; font-size:13px;">??? ??? ????????????/p></a>',
            f'<a href="/a/plumbing" class="card" style="text-decoration:none;"><h3>??????? ??? ?????/h3><p style="color:#666; font-size:13px;">??????????????? ???</p></a>',
            f'<a href="/a/fixture" class="card" style="text-decoration:none;"><h3>??? ??? ??? ????/h3><p style="color:#666; font-size:13px;">???????? ????? ???</p></a>'
        ]
        random.seed(int(hashlib.md5(host.encode()).hexdigest()[:8], 16))
        count = random.randint(3, 5) # ?????? 3??5???????????????
        selected_cards = random.sample(all_cards, count)
        random.shuffle(selected_cards)

        body = f"""
        <div class="section" style="text-align:center; background:{cham['theme']['bg']}">
            <h1 style="color:{cham['theme']['color']}; border-bottom:3px solid {cham['theme']['color']}; display:inline-block;">{cham['name']}</h1>
            <p style="margin-top:10px; font-weight:bold;">{cham['doc_id']} ??? ??? ??? ??????</p>
            <div style="margin-top:15px; font-size:12px; color:#94a3b8;">??? ??????: 2026-01-27 | ??????: ???????/div>
        </div>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:20px;">
            {"".join(selected_cards)}
        </div>
        """
        resp = Response(render_template_string(BASE_HTML, title=cham['name'], body_content=body, site_name=cham['name'], theme_color=cham['theme']['color'], site_desc=cham['doc_id'], ga_id=GA_ID, font_family=cham['font'], identity=cham, terms={"about": "????????", "resources": "??????"}, cls_nav="n_main", cls_footer="f_main", cls_content="c_main"))
        resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        return resp

    # ?? [CASE 2] ??? ??? -> [???] ??? ??? ???????????. ??????????????? ????? ???.
    selected_data = None
    category_key = "cleaning"
    for cat, data in DATA_MAP.items():
        if any(k in keyword for k in data['keywords']):
            selected_data = data
            category_key = cat
            break
    if not selected_data:
        selected_data = DATA_MAP["cleaning"]
    
    final_url = selected_data['link_A'] # ??? A??? ?????
    if type_code == 'B': final_url = selected_data['link_B']
    
    send_trace(f"[V35_3_STABLE_ASCII] Code: {keyword_raw} | Key: {keyword} ({category_key}) | IP: {user_ip} | UA: {ua[:50]}... | Link: {final_url}")
    
    # ?? [v20.0] ??????????????? ??? ????????????? (??? ??? ???)
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
    content = f'<div class="section"><h1>연구소 소개</h1><p style="line-height:2;">{cham["name"]}은(는) {request.host} 네트워크를 통해 설립된 고등 기술 분석 기관입니다. 우리는 산업 전반의 표준화와 효율성을 연구합니다.</p></div>'
    return render_template_string(BASE_HTML, title="연구소 소개", body_content=content, site_name=cham['name'], theme_color=cham['theme']['color'], ga_id=GA_ID, font_family=cham['font'], identity=cham, terms={"about": "연구소 소개", "resources": "기술자료"}, cls_nav="n_ab", cls_footer="f_ab", cls_content="c_ab")

@app.route('/careers')
def careers():
    host = request.host.split(':')[0].replace('www.', '')
    cham = get_chameleon_data(host)
    content = f'<div class="section"><h1>인재 채용</h1><p>{cham["name"]}와 함께 미래를 선도할 연구원을 모집합니다. 관련 전공 석/박사 학위 소지자를 우대합니다.</p></div>'
    return render_template_string(BASE_HTML, title="인재 채용", body_content=content, site_name=cham['name'], theme_color=cham['theme']['color'], ga_id=GA_ID, font_family=cham['font'], identity=cham, terms={"about": "연구소 소개", "resources": "기술자료"}, cls_nav="n_car", cls_footer="f_car", cls_content="c_car")

@app.route('/contact')
def contact():
    host = request.host.split(':')[0].replace('www.', '')
    cham = get_chameleon_data(host)
    content = f'<div class="section"><h1>연락처</h1><p>관리자 문의: admin@{host} | T. {cham["phone"]}</p></div>'
    return render_template_string(BASE_HTML, title="연락처", body_content=content, site_name=cham['name'], theme_color=cham['theme']['color'], ga_id=GA_ID, font_family=cham['font'], identity=cham, terms={"about": "연구소 소개", "resources": "기술자료"}, cls_nav="n_con", cls_footer="f_con", cls_content="c_con")


@app.route('/<company>/<category>')
@app.route('/a/<category>')
def check_visitor(category, company=None):
    host = request.host.split(':')[0].replace('www.', '')
    cham = get_chameleon_data(host)
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    ua = request.headers.get('User-Agent', '').lower()
    
    # ????[v19.0] ??? ????????????? ????
    is_bot, bot_reason = is_bot_detected(user_ip, ua)
    if is_bot:
        return get_honeypot_response(cham)
    
    # ?????? ??? (??? ??? ???????? ???)
    target_data = DATA_MAP.get(category.lower())
    real_url = target_data['link_A'] if target_data else "#"
    
    # ?? [v20.0] ?????? CPA ????? ??? ??? ??????, ??????????? ??? ?????? ?????
    # ?? /a/ ?????????????????'???????? ?????????? ??? ??? ???????? ???????? ??????.
    # ?????? ?? ???????? '??? ??? ???' ?????????????????????
    show_button = not is_bot 
    
    resp = Response(get_professional_report(host, category.lower(), show_cta=show_button, target_url=real_url))
    resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return resp

# --- ????[???] ??????(Sitemap) ??? ??? ??? ---
@app.route('/sitemap.xml')
def sitemap():
    conf = get_config()
    host = request.host.split(':')[0]
    # ??? ???????? ????? ??? ???
    pages = [
        {'loc': '/', 'freq': 'daily', 'pri': '1.0'},
        {'loc': '/about', 'freq': 'monthly', 'pri': '0.5'},
        {'loc': '/resources', 'freq': 'daily', 'pri': '0.8'},
        {'loc': '/careers', 'freq': 'monthly', 'pri': '0.5'},
        {'loc': '/contact', 'freq': 'monthly', 'pri': '0.5'}
    ]
    
    # DB????? ??? ??????????? ??? ?????????? ???
    categories = list(set(d['cat'] for d in DOC_DATABASE))
    for cat in categories:
        pages.append({'loc': f'/a/{cat}', 'freq': 'weekly', 'pri': '0.7'})

    # XML ?????? ?????????
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
