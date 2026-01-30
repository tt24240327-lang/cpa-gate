"""
Extract AI-generated data from rank_vault.db
"""
import sqlite3
import json

DB_PATH = r"h:\SERVER\rank_vault.db"

def extract_all_ai_data():
    """Extract all AI-generated prompts and content"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get all master prompts
    cursor.execute("""
        SELECT target_keyword, master_prompt, url, title, description 
        FROM blog_details 
        WHERE master_prompt IS NOT NULL 
        LIMIT 100
    """)
    
    results = []
    for row in cursor.fetchall():
        results.append({
            'keyword': row['target_keyword'],
            'prompt': row['master_prompt'][:500] if row['master_prompt'] else None,  # Preview
            'url': row['url'],
            'title': row['title'],
            'desc': row['description'][:200] if row['description'] else None
        })
    
    conn.close()
    return results

if __name__ == "__main__":
    # First, list all tables
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"📊 Available tables: {tables}\n")
    conn.close()
    
    # Now try to extract data
    try:
        data = extract_all_ai_data()
        print(f"Total AI data found: {len(data)}")
        
        if data:
            print("\n=== Sample Data ===")
            for i, item in enumerate(data[:3]):
                print(f"\n[{i+1}] Keyword: {item['keyword']}")
                print(f"    Title: {item['title']}")
                print(f"    Prompt: {item['prompt'][:100]}...")
        
        # Save to JSON
        with open(r'h:\checkpoint-system\ai_data_export.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Exported to ai_data_export.json")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTrying to check available columns...")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        if 'blog_analysis_groups' in tables:
            cursor.execute("PRAGMA table_info(blog_analysis_groups)")
            cols = cursor.fetchall()
            print(f"blog_analysis_groups columns: {[c[1] for c in cols]}")
        conn.close()
