import random, time, hashlib
from urllib.parse import quote

class GeneEngine:
    def __init__(self, host, seed_str, db_cat='leak', company_name='일반', cpa_link=None, k='', t='A'):
        self.host = host
        self.raw_seed = seed_str
        self.r = random.Random(seed_str)
        self.db_cat = db_cat
        self.assigned_company = company_name
        self.cpa_link = cpa_link
        self.k = k
        self.t = t
        
        # Obfuscation Suffix for preservation
        self.q_suffix = f"&bypass=showmethemoney&k={k}&t={t}"
        
        # 1. Theme & Color Matrix
        self.main_types = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        self.major_type = self.r.choice(self.main_types)
        self.theme_h = self.r.randint(0, 360)
        self.is_dark = (self.r.random() > 0.8)
        self.primary_color = f"hsl({self.theme_h}, 70%, {'30%' if self.is_dark else '45%'})"
        
        # 2. Keyword Mapping (Logic Sync)
        self.niche_map = {
            'leak': ['정밀 누수 탐지', '배관 비파괴 분석', '수압 계측 기술'],
            'moving': ['거주 이전 공학', '물류 시스템 최적화', '이전 공정 표준'],
            'cleaning': ['환경 위생 관리', '첨단 클리닝 공법', '공간 방역 지표'],
            'welding': ['고정밀 용접 기술', '금속 접합 시방서', '특수 용접 표준'],
            'demolition': ['구조물 해체 공법', '철거 안전 가이드', '폐기물 처리 공정'],
            'faucet': ['수전 설비 표준', '위생 기구 설치 기술', '급배수 시스템']
        }
        self.target_keyword = self.r.choice(self.niche_map.get(db_cat, ['기술 표준 아카이브']))
        self.company_name = f"{self.r.choice(['미래', '글로벌', '대한', '한국', '통합', '차세대'])} {self.target_keyword.split()[0]} {self.r.choice(['연구소', '데이터센터', '아카이브', '협회'])}"
        
        # 3. Ghost Classes (Obfuscation)
        self.c = {
            'nav': f"n_{self.r.randint(100,999)}",
            'card': f"c_{self.r.randint(100,999)}",
            'btn': f"b_{self.r.randint(100,999)}",
            'hero': f"h_{self.r.randint(100,999)}",
            'footer': f"f_{self.r.randint(100,999)}"
        }

    def _get_styles(self):
        txt_color = '#eee' if self.is_dark else '#222'
        bg_color = '#111' if self.is_dark else '#fff'
        card_bg = 'rgba(255,255,255,0.05)' if self.is_dark else '#fff'
        
        return f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;700&display=swap');
            * {{ margin:0; padding:0; box-sizing:border-box; font-family:'Pretendard', sans-serif; }}
            body {{ background:{bg_color}; color:{txt_color}; line-height:1.6; transition:0.3s; }}
            header {{ padding:20px 5%; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(0,0,0,0.1); background:{bg_color}; position:sticky; top:0; z-index:100; }}
            nav a {{ text-decoration:none; color:inherit; margin-left:30px; font-weight:700; font-size:14px; transition:0.2s; border-bottom:2px solid transparent; padding-bottom:5px; }}
            nav a:hover {{ color:{self.primary_color}; border-bottom-color:{self.primary_color}; }}
            .{self.c['hero']} {{ padding:100px 5%; background:linear-gradient(135deg, {self.primary_color}, {self.theme_h + 30}deg, 60%, 40%); color:#fff; text-align:center; }}
            .{self.c['hero']} h1 {{ font-size:3rem; margin-bottom:20px; word-break:keep-all; }}
            .container {{ max-width:1200px; margin:0 auto; padding:60px 5%; }}
            .{self.c['card']} {{ background:{card_bg}; padding:30px; border-radius:15px; box-shadow:0 10px 30px rgba(0,0,0,0.05); margin-bottom:20px; transition:0.3s; border:1px solid rgba(0,0,0,0.05); overflow:hidden; }}
            .{self.c['card']}:hover {{ transform:translateY(-5px); box-shadow:0 15px 40px rgba(0,0,0,0.1); border-color:{self.primary_color}; }}
            .{self.c['btn']} {{ display:inline-block; padding:15px 35px; background:{self.primary_color}; color:#fff !important; text-decoration:none; border-radius:50px; font-weight:bold; transition:0.3s; border:none; cursor:pointer; }}
            .{self.c['btn']}:hover {{ transform:scale(1.05); filter:brightness(1.1); box-shadow:0 10px 20px rgba(0,0,0,0.2); }}
            .{self.c['footer']} {{ padding:60px 5%; background:rgba(0,0,0,0.03); font-size:13px; color:rgba(0,0,0,0.5); border-top:1px solid rgba(0,0,0,0.05); }}
            .grid {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:30px; }}
            .meta-box {{ display:flex; gap:15px; font-size:11px; opacity:0.6; margin-bottom:10px; font-weight:bold; }}
            table td {{ padding: 12px 15px; border-bottom: 1px solid #ddd; color: #222 !important; }}
            table th {{ background-color: {self.primary_color}; color: white; text-align: left; padding: 12px 15px; }}
        </style>
        """

    def _gen_lego_text(self, count=5):
        fragments = [
            f"ISO-2026 표준 규격에 따른 실시간 무결성 검증을 완료한 {self.target_keyword} 연구 리포트입니다.",
            f"산업보건안전법 제24조 및 기술보호법 시행령 제18조에 의거한 공정 지침을 준수합니다.",
            f"데이터 분석 결과 시스템 가용성이 {self.r.randint(990,999)/10}% 이상으로 확인되었습니다.",
            f"첨단 센서 및 시계열 트래픽 분석을 통해 도출된 {self.target_keyword} 최적화 지표를 포함합니다.",
            f"현장 실측 데이터 {self.r.randint(1000,5000)}건의 샘플을 기반으로 한 통계 리포트입니다.",
            f"공정 자동화 시스템의 하중 밸런싱 결과와 물리적 가동 효율 사이의 상관관계 분석 결과입니다.",
            f"기존의 {self.r.randint(1,5)}세대 분석 방식에서 탈피하여 동적 모니터링 엔진이 탑재되었습니다.",
            f"심층 신경망 분석(DNN)을 통한 향후 {self.r.randint(6,12)}개월간의 수요 예측 모델입니다.",
            f"본 기술 표준서는 {self.company_name} 산하 기술전략실의 전수 조사 결과를 토대로 작성되었습니다."
        ]
        paras = []
        for _ in range(count):
            paras.append(" ".join(self.r.sample(fragments, self.r.randint(3, 5))))
        return "<br><br>".join(paras)

    def _block_header(self):
        return f"""
        <header>
            <a href="/?{self.q_suffix}" style="text-decoration:none; color:inherit; font-size:20px;"><b>{self.company_name}</b></a>
            <nav>
                <a href="/?path=/about{self.q_suffix}">정보센터</a>
                <a href="/?path=/archive{self.q_suffix}">기술자료실</a>
                <a href="/?path=/manual{self.q_suffix}">운영지침</a>
            </nav>
        </header>
        """

    def _block_footer(self):
        return f"""
        <footer class="{self.c['footer']}">
            <div style="max-width:1200px; margin:0 auto; display:flex; justify-content:space-between; flex-wrap:wrap; gap:30px;">
                <div>
                    <b>{self.company_name}</b><br><br>
                    주소: {self.r.choice(['서울시','경기도'])} 디지털단지로 | Tel: 02-{self.r.randint(100,999)}-{self.r.randint(1000,9999)}<br><br>
                    Copyright © {self.company_name}. ALL RIGHTS RESERVED.
                </div>
                <div style="display:flex; gap:20px;">
                    <a href="/?path=/privacy{self.q_suffix}">개인정보처리방침</a>
                    <a href="/?path=/terms{self.q_suffix}">이용약관</a>
                </div>
            </div>
        </footer>
        """

    def _block_detail(self, doc_id):
        cpa_button = ""
        if self.cpa_link:
            cpa_button = f"""
            <div style="margin:30px 0; padding:30px; background:{self.primary_color}1a; border:2px dashed {self.primary_color}; border-radius:15px; text-align:center;">
                <h4 style="color:{self.primary_color}; margin-bottom:10px;">🔍 {self.assigned_company} 전문 솔루션 연동</h4>
                <p style="font-size:14px; color:#555; margin-bottom:20px;">본 리포트 사양을 적용한 공식 인증 업체({self.assigned_company}) 무료 상담 서비스입니다.</p>
                <a href="{self.cpa_link}" class="{self.c['btn']}">
                    {self.assigned_company} 무료 기술 상담 신청 &rarr;
                </a>
            </div>
            """

        return f"""
        <div class="container">
            <div class="{self.c['card']}" style="padding:40px; border-top:10px solid {self.primary_color};">
                <h1 style="font-size:2.5rem; margin-bottom:30px;">{self.target_keyword} 통합 정밀 리포트</h1>
                <div style="display:grid; grid-template-columns: 2fr 1fr; gap:40px;">
                    <div>
                        <h3>[1] 분석 결과 요약</h3>
                        <p style="font-size:16px; line-height:1.8;">{self._gen_lego_text(3)}</p>
                        {cpa_button}
                    </div>
                    <div style="background:#f9f9f9; padding:20px; border-radius:10px; color:#222 !important;">
                        <h4 style="margin-bottom:10px;">[2] 계측 데이터 실측치</h4>
                        <table style="width:100%; font-size:12px;">
                            <thead><tr><th>항목</th><th>수치</th></tr></thead>
                            <tbody>
                                <tr><td>가용성</td><td>{self.r.randint(98,99)}%</td></tr>
                                <tr><td>응답속도</td><td>{self.r.randint(10,50)}ms</td></tr>
                                <tr><td>정밀검증</td><td>PASS</td></tr>
                            </tbody>
                        </table>
                        <br>
                        {cpa_button}
                    </div>
                </div>
            </div>
            <center style="margin-top:30px;">
                <a href="/?path=/archive{self.q_suffix}" style="opacity:0.5;">&larr; 기술 자료실로 돌아가기</a>
            </center>
        </div>
        """

    def render(self, path='/'):
        content = ""
        if 'about' in path: content = f"<div class='container'><h1>정보센터</h1><p>{self._gen_lego_text(5)}</p></div>"
        elif 'archive' in path: content = f"<div class='container'><h1>기술 자료실</h1><div class='grid'>{self._gen_cards(12)}</div></div>"
        elif 'doc-' in path: content = self._block_detail(path.split('doc-')[-1])
        else:
            content = f"""
            <section class="{self.c['hero']}"><h1>{self.target_keyword} 전문 기술 포털</h1></section>
            <div class="container"><div class="grid">{self._gen_cards(6)}</div></div>
            """
        
        return f"<!DOCTYPE html><html><head><title>{self.company_name}</title><meta charset='utf-8'>{self._get_styles()}</head><body>{self._block_header()}{content}{self._block_footer()}</body></html>"

    def _gen_cards(self, count):
        html = ""
        for i in range(count):
            doc_id = self.r.randint(1000, 9999)
            html += f"""
            <div class="{self.c['card']}">
                <h3>{self.target_keyword} 리포트 {doc_id}</h3>
                <p style="font-size:14px; opacity:0.7; margin:15px 0;">{self._gen_lego_text(1)}</p>
                <a href="/?path=/doc-{doc_id}{self.q_suffix}" style="color:{self.primary_color}; font-weight:bold;">상세 보기 &rarr;</a>
            </div>
            """
        return html
