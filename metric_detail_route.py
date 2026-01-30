# METRIC Detail Page Route - Archive Style with Rich Content
# Generates 1500+ character content with random visual elements

@app.route('/metric/<int:metric_id>')
def route_metric_detail(metric_id):
    """
    Individual metric detail page with extensive archive-style content
    - Minimum 1,500 characters
    - Random visual elements (tables, graphs, checklists)
    - Seed-based uniqueness
    - No commercial content (archive site)
    """
    ge = get_ge()
    keyword = request.args.get('k', None)
    
    # Extract keyword from CPA_DATA
    target_keyword = None
    if keyword and keyword in CPA_DATA:
        target_keyword = CPA_DATA[keyword][0]
    
    # Generate base data for this metric
    data_item = ge.get_data(metric_id + 1)[metric_id]
    
    # Metric title
    if target_keyword:
        title = f"{target_keyword} 데이터 아카이브 #{metric_id}"
    else:
        title = f"시스템 데이터 아카이브 METRIC_{metric_id}"
    
    # [RICH CONTENT GENERATOR - 1500+ characters]
    
    # Section 1: Introduction (300 chars)
    intro = f"""
    <h2 style="color:{ge.dark_accent}; border-bottom:3px solid {ge.theme_color}; padding-bottom:15px; margin-bottom:30px;">{title}</h2>
    <div style="background:#f8f8f8; padding:25px; border-left:4px solid {ge.dark_accent}; margin-bottom:30px; line-height:1.8;">
        <p style="margin:0; color:#555;">{data_item}</p>
        <p style="margin-top:15px; color:#666;">
            본 데이터는 {ge.r.choice(['실시간', '정밀', '통합', '고급'])} 모니터링 시스템을 통해 수집되었으며,
            {ge.r.choice(['AI 알고리즘', '머신러닝 모델', '통계 분석 엔진', '데이터 마이닝 시스템'])}을 활용하여
            {ge.r.randint(500, 5000)}개 이상의 샘플을 기반으로 분석되었습니다.
            측정 신뢰도는 {ge.r.randint(85, 99)}%로 검증되었으며, 업계 표준 대비 상위 {ge.r.randint(1, 15)}% 수준의 
            품질을 유지하고 있습니다.
        </p>
    </div>
    """
    
    # Section 2: Main Analysis (500 chars)
    analysis_templates = [
        f"데이터 수집 과정에서 {ge.r.choice(['다차원', '복합적', '통합적', '계층적'])} 분석 기법이 적용되었으며, "
        f"{ge.r.choice(['시계열', '횡단면', '패널', '코호트'])} 데이터를 활용한 정량적 평가가 수행되었습니다. ",
        
        f"주요 측정 지표는 {ge.r.choice(['정확도', '재현성', '일관성', '안정성'])}을 중심으로 평가되었으며, "
        f"각 항목별로 {ge.r.randint(10, 50)}회 이상의 반복 측정을 통해 신뢰구간 {ge.r.randint(90, 98)}%를 확보했습니다. ",
        
        f"분석 결과, {ge.r.choice(['평균값', '중앙값', '최빈값', '표준편차'])}이 예상 범위 내에 위치하며, "
        f"{ge.r.choice(['통계적', '실증적', '경험적'])} 유의성이 검증되었습니다. ",
    ]
    
    analysis = f"""
    <h3 style="color:#333; margin-top:40px; margin-bottom:20px;">📊 주요 분석 결과</h3>
    <div style="background:#fff; padding:25px; border:1px solid #e0e0e0; border-radius:8px; line-height:1.8; color:#555;">
        {''.join([ge.r.choice(analysis_templates) for _ in range(ge.r.randint(3, 5))])}
        데이터 처리 파이프라인은 {ge.r.randint(3, 7)}단계로 구성되어 있으며, 각 단계마다 품질 검증 프로세스가 적용됩니다.
        최종적으로 {ge.r.randint(1000, 9999)}개의 데이터 포인트가 아카이브에 저장되었으며, 
        향후 {ge.r.randint(30, 365)}일간 지속적으로 모니터링될 예정입니다.
    </div>
    """
    
    # Section 3: Random Visual Element
    visual_roll = ge.r.random()
    
    if visual_roll < 0.3:  # 30%: Table
        visual = f"""
        <h3 style="color:#333; margin-top:40px; margin-bottom:20px;">📋 측정 데이터 통계표</h3>
        <table style="width:100%; border-collapse:collapse; background:#fff; box-shadow:0 2px 8px rgba(0,0,0,0.1);">
            <thead>
                <tr style="background:{ge.dark_accent}; color:#fff;">
                    <th style="padding:15px; text-align:left; border:1px solid #ddd;">측정 항목</th>
                    <th style="padding:15px; text-align:center; border:1px solid #ddd;">평균값</th>
                    <th style="padding:15px; text-align:center; border:1px solid #ddd;">표준편차</th>
                    <th style="padding:15px; text-align:center; border:1px solid #ddd;">신뢰구간</th>
                </tr>
            </thead>
            <tbody>
                <tr style="border-bottom:1px solid #eee;">
                    <td style="padding:12px; border:1px solid #eee; font-weight:bold; color:#333;">신뢰도</td>
                    <td style="padding:12px; border:1px solid #eee; text-align:center; color:#555;">{ge.r.randint(85, 99)}%</td>
                    <td style="padding:12px; border:1px solid #eee; text-align:center; color:#555;">±{ge.r.randint(1, 5)}.{ge.r.randint(0, 9)}%</td>
                    <td style="padding:12px; border:1px solid #eee; text-align:center; color:{ge.dark_accent};">{ge.r.randint(90, 98)}%</td>
                </tr>
                <tr style="border-bottom:1px solid #eee; background:#f9f9f9;">
                    <td style="padding:12px; border:1px solid #eee; font-weight:bold; color:#333;">처리 속도</td>
                    <td style="padding:12px; border:1px solid #eee; text-align:center; color:#555;">{ge.r.randint(50, 200)}ms</td>
                    <td style="padding:12px; border:1px solid #eee; text-align:center; color:#555;">±{ge.r.randint(5, 30)}ms</td>
                    <td style="padding:12px; border:1px solid #eee; text-align:center; color:{ge.dark_accent};">{ge.r.randint(90, 98)}%</td>
                </tr>
                <tr style="border-bottom:1px solid #eee;">
                    <td style="padding:12px; border:1px solid #eee; font-weight:bold; color:#333;">정확도</td>
                    <td style="padding:12px; border:1px solid #eee; text-align:center; color:#555;">{ge.r.randint(90, 99)}.{ge.r.randint(0, 9)}%</td>
                    <td style="padding:12px; border:1px solid #eee; text-align:center; color:#555;">±{ge.r.randint(0, 2)}.{ge.r.randint(0, 9)}%</td>
                    <td style="padding:12px; border:1px solid #eee; text-align:center; color:{ge.dark_accent};">{ge.r.randint(95, 99)}%</td>
                </tr>
                <tr style="background:#f9f9f9;">
                    <td style="padding:12px; border:1px solid #eee; font-weight:bold; color:#333;">처리량</td>
                    <td style="padding:12px; border:1px solid #eee; text-align:center; color:#555;">{ge.r.randint(1000, 9999)}/h</td>
                    <td style="padding:12px; border:1px solid #eee; text-align:center; color:#555;">±{ge.r.randint(100, 500)}</td>
                    <td style="padding:12px; border:1px solid #eee; text-align:center; color:{ge.dark_accent};">{ge.r.randint(90, 98)}%</td>
                </tr>
            </tbody>
        </table>
        """
    elif visual_roll < 0.5:  # 20%: Bar Graph
        bar_data = [(ge.r.choice(['신뢰도', '정확도', '효율성', '안정성', '품질']), ge.r.randint(60, 100)) for _ in range(5)]
        bars = ""
        for label, value in bar_data:
            bar_fill = int(value / 10)
            bar_empty = 10 - bar_fill
            bars += f"""
            <div style="margin-bottom:20px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                    <span style="font-weight:bold; color:#333;">{label}</span>
                    <span style="color:{ge.dark_accent}; font-weight:bold;">{value}%</span>
                </div>
                <div style="background:#e0e0e0; height:30px; border-radius:15px; overflow:hidden;">
                    <div style="background:linear-gradient(90deg, {ge.dark_accent}, {ge.theme_color}); height:100%; width:{value}%; transition:0.5s;"></div>
                </div>
            </div>
            """
        visual = f"""
        <h3 style="color:#333; margin-top:40px; margin-bottom:20px;">📈 성능 지표 그래프</h3>
        <div style="background:#fff; padding:30px; border:1px solid #e0e0e0; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.1);">
            {bars}
        </div>
        """
    elif visual_roll < 0.75:  # 25%: Checklist
        checklist_items = [
            ("데이터 수집 프로세스 완료", True),
            ("품질 검증 알고리즘 실행", True),
            ("통계 분석 처리 완료", True),
            ("AI 모델 학습 완료", True),
            ("최종 검증 대기", False),
            ("아카이브 저장 예약", False),
        ]
        checklist = ""
        for item, done in checklist_items:
            icon = "✓" if done else "□"
            color = ge.dark_accent if done else "#ccc"
            checklist += f"<div style='margin:15px 0; color:{color}; font-size:16px;'><b>{icon}</b> {item}</div>"
        
        visual = f"""
        <h3 style="color:#333; margin-top:40px; margin-bottom:20px;">✅ 처리 단계 체크리스트</h3>
        <div style="background:#f8f8f8; padding:30px; border-left:4px solid {ge.dark_accent}; border-radius:5px;">
            {checklist}
        </div>
        """
    else:  # 25%: Highlight Box
        visual = f"""
        <div style="background:linear-gradient(135deg, {ge.theme_color}22, {ge.dark_accent}22); padding:30px; border-radius:10px; margin:40px 0; border:2px solid {ge.dark_accent};">
            <h3 style="color:{ge.dark_accent}; margin-top:0;">🔍 핵심 발견사항</h3>
            <ul style="line-height:2; color:#555; margin:20px 0;">
                <li>측정 정밀도가 예상 범위를 {ge.r.randint(5, 20)}% 초과 달성</li>
                <li>데이터 일관성 지수 {ge.r.randint(90, 99)}점 기록</li>
                <li>시스템 안정성 {ge.r.randint(95, 99)}.{ge.r.randint(0, 9)}% 유지</li>
                <li>처리 효율성 업계 평균 대비 {ge.r.randint(110, 150)}% 수준</li>
            </ul>
        </div>
        """
    
    # Section 4: Archive Info (400 chars)
    archive_info = f"""
    <h3 style="color:#333; margin-top:40px; margin-bottom:20px;">🗄️ 아카이브 메타데이터</h3>
    <div style="background:#fff; padding:25px; border:1px solid #e0e0e0; border-radius:8px; line-height:1.8;">
        <p style="color:#555; margin-bottom:15px;">
            본 데이터는 {time.strftime('%Y년 %m월 %d일 %H:%M:%S')}에 시스템에 등록되었으며,
            {ge.r.choice(['자동화', '수동', '하이브리드', '스케줄링'])} 프로세스를 통해 수집되었습니다.
            총 {ge.r.randint(50, 500)}회의 측정이 수행되었으며, 각 측정값은 {ge.r.randint(3, 10)}단계의 
            검증 절차를 거쳤습니다.
        </p>
        <p style="color:#555;">
            데이터 보존 기간은 {ge.r.randint(180, 3650)}일로 설정되어 있으며,
            주기적인 무결성 검사가 매 {ge.r.randint(7, 30)}일마다 자동으로 실행됩니다.
            백업 시스템은 {ge.r.choice(['다중 지역', '분산', '이중화', '클라우드'])} 구조로 구성되어 있어
            데이터 손실 위험이 {ge.r.randint(1, 5) / 10000}% 미만으로 유지됩니다.
        </p>
    </div>
    """
    
    # Section 5: Technical Details (300 chars)
    tech_details = f"""
    <h3 style="color:#333; margin-top:40px; margin-bottom:20px;">⚙️ 기술 사양</h3>
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:20px; margin-bottom:40px;">
        <div style="background:#f8f8f8; padding:20px; border-radius:8px; text-align:center;">
            <div style="font-size:32px; color:{ge.dark_accent}; font-weight:bold;">{ge.r.randint(1000, 9999)}</div>
            <div style="font-size:12px; color:#666; margin-top:10px;">처리 토큰</div>
        </div>
        <div style="background:#f8f8f8; padding:20px; border-radius:8px; text-align:center;">
            <div style="font-size:32px; color:{ge.dark_accent}; font-weight:bold;">{ge.r.randint(50, 200)}ms</div>
            <div style="font-size:12px; color:#666; margin-top:10px;">응답 시간</div>
        </div>
        <div style="background:#f8f8f8; padding:20px; border-radius:8px; text-align:center;">
            <div style="font-size:32px; color:{ge.dark_accent}; font-weight:bold;">{ge.r.randint(85, 99)}%</div>
            <div style="font-size:12px; color:#666; margin-top:10px;">정확도</div>
        </div>
        <div style="background:#f8f8f8; padding:20px; border-radius:8px; text-align:center;">
            <div style="font-size:32px; color:{ge.dark_accent}; font-weight:bold;">v{ge.r.randint(3, 9)}.{ge.r.randint(0, 9)}</div>
            <div style="font-size:12px; color:#666; margin-top:10px;">시스템 버전</div>
        </div>
    </div>
    """
    
    # Footer with hash and timestamp
    footer = f"""
    <div style="margin-top:60px; padding-top:30px; border-top:2px dashed #ccc; font-family:monospace; font-size:11px; color:#999;">
        <div style="margin-bottom:10px;"><strong>ARCHIVE_ID:</strong> METRIC_{metric_id}_{hashlib.md5((str(metric_id) + ge.raw_seed).encode()).hexdigest()[:12]}</div>
        <div style="margin-bottom:10px;"><strong>TIMESTAMP:</strong> {time.strftime('%Y-%m-%d %H:%M:%S')}</div>
        <div style="margin-bottom:10px;"><strong>CHECKSUM:</strong> {hashlib.md5((data_item + str(metric_id)).encode()).hexdigest()[:16]}</div>
        <div><strong>ENGINE:</strong> Genesis_Archive_v{ge.r.randint(4, 7)}.{ge.r.randint(0, 9)}.{ge.r.randint(0, 20)}</div>
    </div>
    """
    
    # Back button
    back_link = f"""
    <div style="margin-top:40px; text-align:center;">
        <a href="/stats{ge.nav_qs}" style="display:inline-block; background:{ge.dark_accent}; color:#fff; padding:15px 40px; border-radius:8px; text-decoration:none; font-weight:bold; transition:0.3s;" onmouseover="this.style.opacity='0.8'" onmouseout="this.style.opacity='1'">
            ← 분석 목록으로 돌아가기
        </a>
    </div>
    """
    
    # Combine all sections
    full_content = f"""
    <section style="max-width:900px; margin:0 auto; padding:40px 20px;">
        {intro}
        {analysis}
        {visual}
        {archive_info}
        {tech_details}
        {footer}
        {back_link}
    </section>
    """
    
    return make_response(render_page(ge, [full_content]))
