$file = 'api/index.py'
$content = Get-Content $file -Encoding UTF8
$content[0] = 'import requests, hashlib, random, base64, time # v35.1_IP_FIX_FINAL'
$content[611] = '    send_trace(f"🛡️ [V35_1_IP_FIX] 코드: {keyword_raw}\n🎯 결정 키워드: {keyword} ({category_key})\n📍 IP: {user_ip}\n🕵️ UA: {ua}\n🔗 실제 CPA링크: {final_url}")'
$content | Set-Content $file -Encoding UTF8
Write-Host "File updated successfully."
