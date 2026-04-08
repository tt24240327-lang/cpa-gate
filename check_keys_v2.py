import sys
import os
import re
import hashlib

sys.stdout.reconfigure(encoding='utf-8')

def check_keys():
    path = r"H:\checkpoint-system\api\index.py"
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all b64_key = r"..."
    matches = re.finditer(r'b64_key\s*=\s*r"(.*?)"', content)
    
    keys = []
    for m in matches:
        keys.append((m.start(), m.group(1)))

    if not keys:
        print("No keys found.")
        return

    print(f"Found {len(keys)} keys.")
    
    first_key = keys[0][1]
    first_hash = hashlib.md5(first_key.encode()).hexdigest()
    
    print(f"Key 1 (start: {keys[0][0]}): MD5={first_hash}")
    
    diff_found = False
    for i in range(1, len(keys)):
        k_val = keys[i][1]
        k_hash = hashlib.md5(k_val.encode()).hexdigest()
        if k_hash != first_hash:
            diff_found = True
            print(f"Key {i+1} (start: {keys[i][0]}): MD5={k_hash} - !!! DISCREPANCY !!!")
            # Find the first difference
            for j in range(min(len(first_key), len(k_val))):
                if first_key[j] != k_val[j]:
                    print(f"  First diff at char {j}: '{first_key[j]}' vs '{k_val[j]}'")
                    context_start = max(0, j - 20)
                    context_end = min(len(first_key), j + 20)
                    print(f"  Context 1: ...{first_key[context_start:context_end]}...")
                    print(f"  Context {i+1}: ...{k_val[context_start:context_end]}...")
                    break
            if len(first_key) != len(k_val):
                print(f"  Length diff: {len(first_key)} vs {len(k_val)}")
        else:
            print(f"Key {i+1} (start: {keys[i][0]}): MD5={k_hash} - Match")

check_keys()
