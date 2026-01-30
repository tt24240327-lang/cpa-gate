#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cloudflare API 토큰 테스트
"""

import requests

CLOUDFLARE_API_TOKEN = "osw7n7MdIl2naSXMKic5O20NeB1R2ALGDPcHsmwX"

HEADERS = {
    "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
    "Content-Type": "application/json"
}

print("[TEST] Cloudflare API 토큰 테스트 시작...")
print(f"[INFO] 토큰: {CLOUDFLARE_API_TOKEN[:20]}...")

# API 호출 테스트
url = "https://api.cloudflare.com/client/v4/zones?page=1&per_page=1"

print(f"[INFO] API 호출 중: {url}")

try:
    response = requests.get(url, headers=HEADERS, timeout=10)
    
    print(f"[INFO] 응답 코드: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("[OK] API 토큰 정상 작동!")
        print(f"[INFO] 총 도메인 수: {data['result_info']['total_count']}")
        
        if data['result']:
            print(f"[INFO] 첫 번째 도메인: {data['result'][0]['name']}")
    else:
        print(f"[ERROR] API 오류!")
        print(f"[ERROR] 응답: {response.text}")
        
except requests.exceptions.Timeout:
    print("[ERROR] 타임아웃! 네트워크 연결을 확인하세요.")
except Exception as e:
    print(f"[ERROR] 예외 발생: {e}")

print("[DONE] 테스트 완료")
