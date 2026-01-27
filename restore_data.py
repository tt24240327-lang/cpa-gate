import os

file_path = 'api/index.py'

# The correct, full Korean data maps
DATA_MAP_STR = '''DATA_MAP = {
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
}'''

KEYWORD_MAP_STR = '''KEYWORD_MAP = {
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
}'''

try:
    # Read the file with permissive encoding (ascii/utf-8/latin-1 fallback)
    # Since it might be mixed, we try to read carefully.
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # Identify the start and end of DATA_MAP
    # We look for "DATA_MAP = {" and the closing "}" before "SECRET_SALT"
    # This is a heuristic based on file structure.
    start_dm = content.find("DATA_MAP = {")
    end_dm = content.find("SECRET_SALT =", start_dm)
    # Backtrack to find the closing brace of DATA_MAP
    end_dm = content.rfind("}", start_dm, end_dm) + 1
    
    if start_dm != -1 and end_dm != -1:
        content = content[:start_dm] + DATA_MAP_STR + content[end_dm:]
        print("Restored DATA_MAP")
    else:
        print("Could not find DATA_MAP block")

    # Identify KEYWORD_MAP
    start_km = content.find("KEYWORD_MAP = {")
    end_km = content.find("REPORT_SNIPPETS =", start_km)
    end_km = content.rfind("}", start_km, end_km) + 1
    
    if start_km != -1 and end_km != -1:
        content = content[:start_km] + KEYWORD_MAP_STR + content[end_km:]
        print("Restored KEYWORD_MAP")
    else:
        print("Could not find KEYWORD_MAP block")
        
    # Update version header
    content = content.replace("v35.3_STABLE_ASCII", "v35.4_KOREAN_RESTORED")
    # Also update the top line manually if needed, but replace is safer
    if "# v35.3" in content:
        content = content.replace("# v35.3", "# v35.4")
        
    # Write back as proper UTF-8
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("File updated successfully.")
    
except Exception as e:
    print(f"Error: {e}")
