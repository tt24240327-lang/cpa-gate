
import os

def fix_api_index():
    file_path = 'api/index.py'
    try:
        with open('verified_b64.txt', 'r', encoding='utf-8') as f:
            correct_b64 = f.read().strip()
    except FileNotFoundError:
        print("Error: verified_b64.txt not found.")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return

    new_lines = []
    replaced_count = 0
    
    for line in lines:
        if 'b64_key = r"eyJ' in line:
            # Preserve indentation
            indent = line[:line.find('b64_key')]
            new_line = f'{indent}b64_key = r"{correct_b64}"\n'
            new_lines.append(new_line)
            replaced_count += 1
        else:
            new_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"Successfully replaced {replaced_count} occurrences of b64_key in {file_path}.")

if __name__ == "__main__":
    fix_api_index()
