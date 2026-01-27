$file = 'api/index.py'
# Read as UTF8 (or try to recover)
$content = Get-Content $file
# Manually replace the corrupted line 612 (index 611) with a clean, simple string
$content[611] = '    send_trace(f"🛡️ [V35_2_HOTFIX] 코드: {keyword_raw}\n🎯 결정 키워드: {keyword} ({category_key})\n📍 IP: {user_ip}\n🕵️ UA: {ua[:50]}...\n🔗 실제 CPA링크: {final_url}")'
# Force write as BOM-less UTF8 to be safe for Linux/Vercel
[System.IO.File]::WriteAllLines($file, $content, (New-Object System.Text.UTF8Encoding $False))
Write-Host "Hotfix applied."
