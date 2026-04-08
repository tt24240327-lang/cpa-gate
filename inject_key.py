import re

def inject_key():
    with open('verified_b64.txt', 'r') as f:
        b64_key = f.read().strip()
    
    with open('api/index.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace both occurrences
    # b64_key = "..." or b64_key = r"..."
    pattern = r'b64_key = r?\"(.*?)\"'
    new_content = re.sub(pattern, f'b64_key = r"{b64_key}"', content)
    
    with open('api/index.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully injected verified B64 key into api/index.py")

if __name__ == "__main__":
    inject_key()
