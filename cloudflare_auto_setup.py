#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cloudflare 자동 보안 설정 스크립트
- 모든 도메인에 WAF 규칙 5개 자동 생성
- DNS 프록시 자동 활성화
- Bot Fight Mode 자동 활성화
"""

import requests
import time
from typing import List, Dict

# ==================== 설정 ====================
CLOUDFLARE_API_TOKEN = "osw7n7MdIl2naSXMKic5O20NeB1R2ALGDPcHsmwX"
CLOUDFLARE_EMAIL = "tt24240327@gmail.com"  # 클라우드플레어 계정 이메일

# WAF 차단 규칙 목록
WAF_RULES = [
    {
        "name": "Block WordPress Scanners",
        "path": "/wp-admin",
        "description": "WordPress 관리자 페이지 스캐너 차단"
    },
    {
        "name": "Block Config Scanners",
        "path": "/.env",
        "description": "환경 설정 파일 스캐너 차단"
    },
    {
        "name": "Block Setup Scanners",
        "path": "/setup-config",
        "description": "설정 파일 스캐너 차단"
    },
    {
        "name": "Block XMLRPC Scanners",
        "path": "/xmlrpc",
        "description": "XMLRPC 공격 차단"
    },
    {
        "name": "Block Install Scanners",
        "path": "/install.php",
        "description": "설치 파일 스캐너 차단"
    }
]

# ==================== API 헤더 ====================
HEADERS = {
    "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
    "Content-Type": "application/json"
}

# ==================== 함수 ====================

# ==================== 로깅 설정 ====================
LOG_FILE = "setup_log.txt"

def log(message: str):
    """로그 파일 및 화면에 출력"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    formatted_msg = f"[{timestamp}] {message}"
    
    # 파일에 쓰기 (UTF-8)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(formatted_msg + "\n")
    
    # 화면에는 간단히 출력 (에러 방지용)
    try:
        print(message)
    except:
        pass

def get_all_zones() -> List[Dict]:
    """모든 도메인(Zone) 목록 가져오기"""
    log("[INFO] 도메인 목록 가져오는 중...")
    
    zones = []
    page = 1
    
    while True:
        url = f"https://api.cloudflare.com/client/v4/zones?page={page}&per_page=50"
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code != 200:
            log(f"[ERROR] API 오류: {response.status_code}")
            log(response.text)
            break
        
        data = response.json()
        zones.extend(data['result'])
        
        if data['result_info']['page'] >= data['result_info']['total_pages']:
            break
        
        page += 1
    
    log(f"[OK] 총 {len(zones)}개 도메인 발견!")
    return zones


def enable_dns_proxy(zone_id: str, zone_name: str) -> bool:
    """DNS 레코드 프록시 활성화"""
    log(f"  [INFO] [{zone_name}] DNS 프록시 활성화 중...")
    
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        log(f"  [ERROR] DNS 레코드 조회 실패")
        return False
    
    records = response.json()['result']
    success_count = 0
    for record in records:
        if record['type'] in ['A', 'CNAME'] and not record['proxied']:
            update_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record['id']}"
            update_data = {
                "type": record['type'],
                "name": record['name'],
                "content": record['content'],
                "proxied": True
            }
            
            update_response = requests.patch(update_url, headers=HEADERS, json=update_data)
            if update_response.status_code == 200:
                success_count += 1
    
    log(f"  [OK] {success_count}개 레코드 프록시 활성화 완료")
    return True


def create_waf_rules(zone_id: str, zone_name: str) -> bool:
    """WAF 규칙 5개 생성 (Ruleset API 사용 - 무료 플랜 호환)"""
    log(f"  [INFO] [{zone_name}] WAF 규칙 생성 (Ruleset API)...")
    
    # 1. 해당 Zone의 'custom' ruleset ID 찾기
    rulesets_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets"
    response = requests.get(rulesets_url, headers=HEADERS)
    
    if response.status_code != 200:
        log(f"  [ERROR] Ruleset 조회 실패: {response.text}")
        return False
        
    ruleset_id = None
    datas = response.json().get('result', [])
    for rs in datas:
        if rs['phase'] == 'http_request_firewall_custom' and rs['kind'] == 'zone':
            ruleset_id = rs['id']
            break
            
    # Ruleset이 없으면 새로 생성해야 함 (보통은 있음)
    if not ruleset_id:
        log(f"  [INFO] Custom Ruleset이 없어서 새로 생성합니다...")
        create_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets"
        create_data = {
            "name": "default",
            "kind": "zone",
            "phase": "http_request_firewall_custom"
        }
        create_res = requests.post(create_url, headers=HEADERS, json=create_data)
        if create_res.status_code == 200:
            ruleset_id = create_res.json()['result']['id']
        else:
            log(f"  [ERROR] Ruleset 생성 실패: {create_res.text}")
            return False

    # 2. 규칙 추가하기
    update_url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/rulesets/{ruleset_id}/rules"
    
    success_count = 0
    for rule in WAF_RULES:
        rule_data = {
            "action": "block",
            "expression": f'(http.request.uri.path contains "{rule["path"]}")',
            "description": rule["name"],
            "enabled": True
        }
        
        res = requests.post(update_url, headers=HEADERS, json=rule_data)
        
        if res.status_code == 200:
            success_count += 1
            log(f"  [OK] {rule['name']} 생성 완료")
        else:
            # 이미 존재하거나 에러인 경우
            if "duplicate" in res.text.lower():
                 log(f"  [INFO] {rule['name']} 이미 존재함")
                 success_count += 1
            else:
                log(f"  [WARN] {rule['name']} 생성 실패: {res.text}")
        
        time.sleep(0.5)

    log(f"  [OK] {success_count}/{len(WAF_RULES)}개 규칙 처리 완료")
    return success_count > 0


def enable_bot_fight_mode(zone_id: str, zone_name: str) -> bool:
    """Bot Fight Mode 활성화"""
    log(f"  [INFO] [{zone_name}] Bot Fight Mode 활성화 중...")
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/bot_fight_mode"
    data = {"value": "on"}
    response = requests.patch(url, headers=HEADERS, json=data)
    
    if response.status_code == 200:
        log(f"  [OK] Bot Fight Mode 활성화 완료")
        return True
    else:
        log(f"  [WARN] Bot Fight Mode 활성화 실패")
        return False


def whitelist_master_ip(zone_id: str, zone_name: str, master_ip: str = "61.83.9.20") -> bool:
    """마스터 IP를 화이트리스트(IP Access Rule)에 추가"""
    log(f"  [INFO] [{zone_name}] 마스터 IP({master_ip}) 화이트리스트 등록 중...")
    
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/firewall/access_rules/rules"
    data = {
        "mode": "allow",
        "configuration": {
            "target": "ip",
            "value": master_ip
        },
        "notes": "Master Testing IP - Antigravity Auto Setup"
    }
    
    response = requests.post(url, headers=HEADERS, json=data)
    
    if response.status_code == 200:
        log(f"  [OK] 마스터 IP 등록 완료")
        return True
    elif "already exists" in response.text:
        log(f"  [INFO] 마스터 IP가 이미 존재함")
        return True
    else:
        log(f"  [WARN] 마스터 IP 등록 실패: {response.text}")
        return False


def setup_zone(zone: Dict) -> Dict:
    """개별 도메인 설정"""
    zone_id = zone['id']
    zone_name = zone['name']
    
    log(f"\n{'='*60}")
    log(f"[START] [{zone_name}] 설정 시작...")
    log(f"{'='*60}")
    
    results = {
        "zone_name": zone_name,
        "dns_proxy": False,
        "waf_rules": False,
        "bot_fight": False,
        "whitelist": False
    }
    
    results["dns_proxy"] = enable_dns_proxy(zone_id, zone_name)
    time.sleep(1)
    results["waf_rules"] = create_waf_rules(zone_id, zone_name)
    time.sleep(1)
    results["bot_fight"] = enable_bot_fight_mode(zone_id, zone_name)
    time.sleep(1)
    results["whitelist"] = whitelist_master_ip(zone_id, zone_name)
    
    return results


def main():
    """메인 실행 함수"""
    # 로그 파일 초기화
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("=== Cloudflare 자동 설정 로그 ===\n")

    log("="*60)
    log("[START] Cloudflare 자동 보안 설정 시작!")
    log("="*60)
    
    zones = get_all_zones()
    
    if not zones:
        log("[ERROR] 도메인을 찾을 수 없습니다.")
        return
    
    log(f"\n[INFO] 총 {len(zones)}개 도메인 설정 시작...\n")
    
    all_results = []
    
    for i, zone in enumerate(zones, 1):
        log(f"\n[{i}/{len(zones)}] 진행 중...")
        result = setup_zone(zone)
        all_results.append(result)
        if i < len(zones):
            time.sleep(2)
    
    log("\n" + "="*60)
    log("[RESULT] 최종 결과 요약")
    log("="*60)
    
    success_count = 0
    for result in all_results:
        status = "[OK]" if all([result["dns_proxy"], result["waf_rules"]]) else "[WARN]"
        log(f"{status} {result['zone_name']}")
        
        if result["dns_proxy"] and result["waf_rules"]:
            success_count += 1
    
    log("\n" + "="*60)
    log(f"[DONE] 완료! {success_count}/{len(zones)}개 도메인 설정 성공!")
    log("="*60)


if __name__ == "__main__":
    main()
