import re

def check_file():
    with open('api/index.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for both r"..." and "..."
    keys = re.findall(r'b64_key = r?\"(.*?)\"', content)
    print(f"Found {len(keys)} keys")
    for i, k in enumerate(keys):
        print(f"Key {i}: len={len(k)}, start={k[:30]}, end={k[-30:]}")

if __name__ == "__main__":
    check_file()
