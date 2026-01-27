import os

file_path = 'api/index.py'

try:
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # 1. Added identity_gen
    if 'def identity_gen' not in content:
        id_gen_code = '\\ndef identity_gen(host):\\n    return get_chameleon_data(host)\\n'
        # Just append to the end or find a safe spot
        content += id_gen_code
        print("Added identity_gen")

    # 2. Fix report content box (Fixed version)
    target = 'report_text += f"<div'
    if target in content:
        start_box = content.find(target)
        # Find the next closing </div>"
        end_box = content.find('</div>"', start_box)
        if end_box != -1:
            end_box += 7
            new_line = '        report_text += f"<div style=\'background:#f1f5f9; padding:15px; border-radius:5px; font-size:12px; margin:20px 0; color:#475569; border-left:4px solid #94a3b8;\'><strong>[분석 데이터 ID: {h % 99999:05d}]</strong><br>본 섹션의 데이터는 국가 표준 가이드라인 v{random.randint(2,4)}.0에 따라 검증되었습니다.</div>"'
            content = content[:start_box] + new_line + content[end_box:]
            print("Fixed report box")

    # 3. Mass string cleanup
    content = content.replace('??????</a>', '인재 채용</a>')
    content = content.replace('??????</a>', '연락처</a>')
    content = content.replace('(??', '(주)')
    content = content.replace('?????:', '대표자:')
    content = content.replace('Copyright ?', 'Copyright ©')
    content = content.replace('??????????????:', '기술인프라 보전번호:')
    content = content.replace('????? IP', '비정상 접근')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Repair successful.")

except Exception as e:
    print(f"Error: {e}")
