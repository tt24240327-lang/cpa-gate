import json
import base64

def normalize_and_b64():
    with open('service_key.json', 'r') as f:
        data = json.load(f)
    
    # Normalize private_key
    pk = data['private_key']
    header = "-----BEGIN PRIVATE KEY-----"
    footer = "-----END PRIVATE KEY-----"
    
    # Strip headers/footers to get the body
    body = pk.replace(header, "").replace(footer, "").strip()
    # Remove all whitespace from body
    body = "".join(body.split())
    
    # Reconstruct with clean newlines
    new_pk = f"{header}\n{body}\n{footer}\n"
    data['private_key'] = new_pk
    
    # Convert to JSON string (compact)
    json_str = json.dumps(data)
    
    # Encode to B64
    b64_key = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
    
    with open('verified_b64.txt', 'w') as f:
        f.write(b64_key)
    
    print(f"Normalized B64 Key Length: {len(b64_key)}")
    print(f"B64 Key End: {b64_key[-20:]}")

if __name__ == "__main__":
    normalize_and_b64()
