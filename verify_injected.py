import re

def verify_injected():
    with open('api/index.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    keys = re.findall(r'b64_key = r\"(.*?)\"', content)
    print(f"Number of keys found: {len(keys)}")
    for i, k in enumerate(keys):
        print(f"Key {i} length: {len(k)}")
        # Check start and end
        print(f"Key {i} start: {k[:20]}... end: {k[-20:]}")

if __name__ == "__main__":
    verify_injected()
