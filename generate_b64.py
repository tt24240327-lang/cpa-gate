import base64, json
with open('gen-lang-client-0222061612-b7f9fc3ed86a.json', 'r', encoding='utf-8') as f:
    d = json.load(f)
b = base64.b64encode(json.dumps(d).encode('utf-8')).decode('utf-8')
print("--- NEW BASE64 KEY ---")
print(b)
print("--- END ---")
