import random

class LandingEngine:
    def __init__(self, category, companies):
        self.category = category
        self.companies = companies
        self.cat_name = {
            "leak": "누수 정밀 점검 및 탐지",
            "moving": "이사 견적 비교 센터",
            "cleaning": "전문 클리닝 서비스",
            "faucet": "수전 교체 전문 설치",
            "demolition": "철거 및 구조물 해체",
            "welding": "정밀 용접/접합 서비스"
        }.get(category, "CPA 프리미엄 서비스")

    def render(self, host):
        color_map = {
            "moving": "#2c3e50", "leak": "#2980b9", "faucet": "#16a085", "cleaning": "#27ae60"
        }
        primary = color_map.get(self.category, "#34495e")

        # HTML Generation for Guest Landing
        cards = ""
        for cp in self.companies:
            # We assume cp has 'name', 'track_a', 'url_a', etc. 
            # In index.py, we should prepare the tracking link for each.
            cards += f"""
            <div class="card">
                <div class="card-tag">Official Partner</div>
                <h2>{cp['name']} <span style="font-size:12px; opacity:0.5;">검증 완료</span></h2>
                <p>국가 공인 기술 보유 및 소비자 만족도 1위 업체({self.cat_name})</p>
                <a href="{cp['track_link']}" class="btn">상담 신청하기</a>
            </div>
            """

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>마이홈플래너 - {self.cat_name} 비교</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;700&display=swap');
                * {{ margin:0; padding:0; box-sizing:border-box; font-family:'Pretendard', sans-serif; }}
                body {{ background:#f4f7f6; color:#333; }}
                header {{ background:{primary}; padding:30px 5%; color:#fff; text-align:center; box-shadow:0 4px 12px rgba(0,0,0,0.1); }}
                header h1 {{ font-size:1.8rem; margin-bottom:10px; }}
                header p {{ opacity:0.8; font-size:0.9rem; }}
                .container {{ max-width:1000px; margin:40px auto; padding:0 5%; gap:20px; display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); }}
                .card {{ background:#fff; padding:30px; border-radius:20px; box-shadow:0 10px 20px rgba(0,0,0,0.05); transition:0.3s; border:1px solid #eee; position:relative; overflow:hidden; }}
                .card:hover {{ transform:translateY(-10px); box-shadow:0 15px 40px rgba(0,0,0,0.15); border-color:{primary}; }}
                .card-tag {{ position:absolute; top:0; right:0; background:#ff4757; color:#fff; font-size:10px; padding:5px 15px; border-bottom-left-radius:15px; font-weight:bold; }}
                .card h2 {{ font-size:1.4rem; color:{primary}; margin-bottom:15px; }}
                .card p {{ font-size:14px; color:#666; margin-bottom:25px; line-height:1.5; }}
                .btn {{ display:block; text-align:center; padding:15px; background:{primary}; color:#fff; text-decoration:none; border-radius:12px; font-weight:bold; transition:0.3s; }}
                .btn:hover {{ filter:brightness(1.2); }}
                footer {{ text-align:center; padding:40px; color:#999; font-size:12px; }}
            </style>
        </head>
        <body>
            <header>
                <h1>🏠 마이홈플래너 통합 센터</h1>
                <p>엄격한 기준으로 검증된 전국의 <b>{self.cat_name}</b> 전문 업체를 한눈에 비교하세요.</p>
            </header>
            <div class="container">
                {cards}
            </div>
            <footer>
                <p>© 마이홈플래너 공식 견적 비교 센터 | {host}</p>
                <p>본 사이트는 업종별 선두 업체만을 선별하여 추천드립니다.</p>
            </footer>
        </body>
        </html>
        """
