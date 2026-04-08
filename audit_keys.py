import sys
import os
import re
import base64
import json

sys.stdout.reconfigure(encoding='utf-8')

def audit_keys():
    path = r"H:\checkpoint-system\api\index.py"
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    matches = list(re.finditer(r'b64_key\s*=\s*r"(.*?)"', content))
    
    for i, m in enumerate(matches):
        k_val = m.group(1)
        print(f"Key {i+1} (Line approx {content.count('\n', 0, m.start()) + 1}):")
        try:
            decoded = base64.b64decode(k_val).decode('utf-8')
            info = json.loads(decoded)
            print(f"  Valid JSON. Email: {info.get('client_email')}")
            # Check for suspicious differences in the key itself
            pkey = info.get('private_key', '')
            print(f"  Private Key Snippet: {pkey[:30]}...{pkey[-30:]}")
            print(f"  Private Key Len: {len(pkey)}")
        except Exception as e:
            print(f"  !!! FAILED TO DECODE/PARSE !!! Error: {e}")
            # Show where it might be broken
            print(f"  Length: {len(k_val)}")

audit_keys()
