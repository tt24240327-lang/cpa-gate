$file = 'api/index.py'
$content = Get-Content $file
# Replaces line 612 (index 611) with SAFE ASCII ONLY content
$content[611] = '    send_trace(f"[V35_3_STABLE_ASCII] Code: {keyword_raw} | Key: {keyword} ({category_key}) | IP: {user_ip} | UA: {ua[:50]}... | Link: {final_url}")'
# Force write as ASCII to guarantee no hidden bytes
[System.IO.File]::WriteAllLines($file, $content, [System.Text.Encoding]::ASCII)
Write-Host "ASCII Hotfix applied."
