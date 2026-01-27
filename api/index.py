import requests, hashlib, random, base64 # v1.1.1 Deployment Force
from flask import Flask, request, render_template_string, Response

app = Flask(__name__)

# [설정] 행님의 중앙 통제실 정보
TELEGRAM_TOKEN = "7983385122:AAGK4kjCDpmerqfSwQL66ZDPL2MSOEV4An0"
CHAT_ID = "1898653696"
GA_ID = "G-1VH7D6BJTD"

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
        "keywords": ["입주청소", "이사청소", "거주청소", "청소업체", "청소", "입주 청소"],
        "image": "cleaning.jpg",
        "link_A": "https://www.replyalba.co.kr/pt/WwVCgW9E1R",
        "link_B": "https://albarich.com/pt/z2NytCt42i"
    },
    "moving": {
        "keywords": ["이사", "포장이사", "원룸이사", "용달이사", "이삿짐", "포장 이사"],
        "image": "moving.jpg",
        "link_A": "https://www.replyalba.co.kr/pt/LlocSbdUSY",
        "link_B": "https://albarich.com/pt/zdIDBDSzof"
    },
    "welding": {
        "keywords": ["용접", "출장용접", "알곤용접", "배관용접", "용접업체"],
        "image": "welding.jpg",
        "link_A": "https://www.replyalba.co.kr/pt/XpBx9dZ5aE",
        "link_B": "https://albarich.com/pt/SROHH97olh"
    },
    "plumbing": {
        "keywords": ["막힘", "누수", "뚫음", "변기막힘", "하수구막힘", "배관", "싱크대막힘", "역류"],
        "image": "plumbing.jpg",
        "link_A": "https://www.replyalba.co.kr/pt/GkVRvxfx1T",
        "link_B": "https://albarich.com/pt/QOaojnBV2v"
    },
    "fixture": {
        "keywords": ["수전교체", "변기교체", "세면대교체", "부속교체", "수전", "세면대", "도기교체"],
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

# 🔑 [v14.0] SMART KEYWORD DECODER: 무한 확장형 키워드 엔진
KEYWORD_MAP = {
    # [청소]
    "cln-01": "입주청소", "cln-02": "이사청소", "cln-03": "거주청소", "cln-04": "청소업체",
    # [이사]
    "mov-01": "포장이사", "mov-02": "원룸이사", "mov-03": "용달이사", "mov-04": "이삿짐",
    # [용접]
    "wld-01": "용접", "wld-02": "출장용접", "wld-03": "알곤용접",
    # [설비/막힘]
    "pip-01": "하수구막힘", "pip-02": "변기막힘", "pip-03": "싱크대막힘",
    # [교체/수리]
    "fix-01": "수전교체", "fix-02": "변기교체", "fix-03": "세면대교체",
    # [철거]
    "dem-01": "철거", "dem-02": "원상복구", "dem-03": "상가철거"
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

@app.route('/')
def index():
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    ua = request.headers.get('User-Agent', '').lower()
    host = request.host.split(':')[0].replace('www.', '')
    
    # 🕵️ [v17.0] 실시간 키워드 추출 및 봇 탐지 (네이버 Yeti/G-bot/IP 차단)
    keyword_raw = request.args.get('k', '')
    keyword = get_keyword(keyword_raw) or ""
    is_bot = any(bot in ua for bot in ['bot', 'crawl', 'slurp', 'spider', 'naver', 'daum', 'google', 'phantom', 'headless'])
    
    # 카멜레온 데이터 생성 (주소 + 키워드 기반 고정 랜덤)
    cham = get_chameleon_data(host, keyword)
    type_code = request.args.get('t', 'A')

    # 🚩 [CASE 1] 봇이거나 키워드 없는 직접 접속 -> "전문 연구소"로 위장
    if is_bot or not keyword:
        report = f"🚩 [{cham['name']}] 위장홈 접속 (탐지된 봇: {is_bot})\n🌐 주소: {request.host}\n📍 IP: {user_ip}\n🕵️ UA: {ua[:40]}..."
        send_trace(report)
        
        # 가짜 연구물 카드 (주소별 셔플링)
        cards = [
            f'<a href="/a/moving" class="card" style="text-decoration:none;"><h3>{keyword or "핵심"} 기술 보고서</h3><p style="color:#666; font-size:13px;">{cham["doc_id"]} 공정 분석 자료</p></a>',
            f'<a href="/a/cleaning" class="card" style="text-decoration:none;"><h3>주요 인프라 최적화</h3><p style="color:#666; font-size:13px;">에너지 효율 및 시스템 진단</p></a>',
            f'<a href="/a/welding" class="card" style="text-decoration:none;"><h3>글로벌 기술 표준</h3><p style="color:#666; font-size:13px;">ISO 인증 및 국가 표준 준수</p></a>'
        ]
        random.seed(int(hashlib.md5(host.encode()).hexdigest()[:8], 16))
        random.shuffle(cards)

        body = f"""
        <div class="section" style="text-align:center; background:{cham['theme']['bg']}">
            <h1 style="color:{cham['theme']['color']}; border-bottom:3px solid {cham['theme']['color']}; display:inline-block;">{cham['name']}</h1>
            <p style="margin-top:15px; font-weight:bold;">{keyword or "차세대"} {cham['doc_id']} 운영 표준 가이드라인</p>
            <div style="margin-top:20px; font-size:12px; color:#94a3b8;">문서 보안등급: 2급 | 검토완료: 2026-01-27</div>
        </div>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:20px;">
            {"".join(cards)}
        </div>
        """
        return render_template_string(BASE_HTML, title=cham['name'], body_content=body, site_name=cham['name'], theme_color=cham['theme']['color'], site_desc=cham['doc_id'], ga_id=GA_ID, font_family=cham['font'], identity=cham, terms={"about": "연구소 소개", "resources": "기술자료"}, cls_nav="n_main", cls_footer="f_main", cls_content="c_main")

    # 🎯 [CASE 2] 진짜 손님 -> CPA 랜딩에 카멜레온 위장막 입히기
    selected_data = None
    for category, data in DATA_MAP.items():
        if any(k in keyword for k in data['keywords']):
            selected_data = data
            break
    if not selected_data:
        selected_data = DATA_MAP["moving"]
    
    final_link = selected_data['link_B'] if type_code == 'B' else selected_data['link_A']
    send_trace(f"💰 [{selected_data['image'].split('.')[0]}] 진입 - {keyword} ({request.host})")

    return render_template_string(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{keyword} {cham['name']}</title>
        <style>
            body {{ margin: 0; padding: 0; background: {cham['theme']['bg']}; overflow-x: auto; }}
            .header {{ background: white; padding: 15px 5%; border-bottom: 2px solid {cham['theme']['color']}; display: flex; justify-content: space-between; align-items: center; }}
            .container {{ width: 100%; min-width: 1000px; margin: 0 auto; }}
            @media (max-width: 768px) {{ .container {{ min-width: 100%; }} }}
            .cpa-frame {{ width: 100%; height: 6000px; border: none; display: block; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div style="font-weight:900; color:{cham['theme']['color']};">{cham['name']}</div>
            <div style="font-size:12px; color:#666;">ID: {cham['doc_id']}</div>
        </div>
        <div class="container">
            <iframe class="cpa-frame" src="{final_link}"></iframe>
        </div>
    </body>
    </html>
    """)

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
def check_visitor(company, category):
    host = request.host.split(':')[0].replace('www.', '')
    cham = get_chameleon_data(host)
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    ua = request.headers.get('User-Agent', '').lower()
    is_bot = any(prefix in user_ip for prefix in ['110.93.', '114.111.', '125.209.', '211.249.', '210.89.']) or any(bot in ua for bot in ['naver', 'yeti', 'bot', 'crawl', 'google'])
    host = request.host.split(':')[0].replace('www.', '')

    # 🕵️ [v12.0] 기존 CPA_DATA 대신 DATA_MAP에서 카테고리 매칭 (하위 호환성)
    target_data = DATA_MAP.get(category.lower())
    real_url = None
    if target_data:
        real_url = target_data['link_A'] # 기본 A 업체로 연동
    
    # 텔레그램 추적
    report = f"🚩 [{conf['identity']['name']}] 내부링크 방문!\n📍 경로: /{company}/{category}\n🌐 주소: {request.host}\n📍 IP: {user_ip}\n🕵️ 신분: {ua[:50]}..."
    send_trace(report)

    # 봇이거나 링크가 없는 정보성 페이지일 때 -> '기술 보고서' 노출
    if not real_url or is_bot:
        doc = next((d for d in DOC_DATABASE if d['cat'] == category), None)
        title = doc['title'] if doc else category.upper() + " 기술 표준"
        text = text_stylist(doc['desc'] if doc else "국가 표준(KS) 및 국제 규격(ISO)에 따른 전문 기술 지침입니다.", request.host)
        chart = get_dynamic_chart(host)
        doc_content = f"""
        <div class="section">
            <div style="float:right; border:2px solid #e74c3c; color:#e74c3c; padding:4px 10px; font-weight:bold; transform:rotate(12deg);">APPROVED</div>
            <p style="color:{conf['color']}; font-weight:bold;">[{conf['terms']['report']}]</p>
            <h1 style="color:#1e293b; margin-top:10px;">{title}</h1>{chart}
            <p style="text-align:justify; line-height:2; color:#334155;">{text}</p>
            <p style="font-size:12px; color:#888; margin-top:30px; border-top:1px solid #f1f5f9; padding-top:15px;">※ 본 문서는 인가된 시스템에 의해 생성된 기술 보안 문서입니다. (ID: {hashlib.md5(host.encode()).hexdigest()[:8].upper()})</p>
        </div>
        """
        return render_template_string(BASE_HTML, title=conf['terms']['report'], body_content=doc_content, site_name=conf['name'], theme_color=conf['color'], site_desc=conf['desc'], ga_id=GA_ID, font_family=conf['font'], identity=conf['identity'], cls_nav=conf['cls_nav'], cls_footer=conf['cls_footer'], cls_content=conf['cls_content'], terms=conf['terms'])
    
    return render_template_string(f'<html><head><meta http-equiv="refresh" content="0.5;url={{{{ real_url }}}}"></head><body style="text-align:center; padding-top:150px; font-family:sans-serif;"><h3>데이터 보안 검사 중...</h3></body></html>', real_url=real_url)

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