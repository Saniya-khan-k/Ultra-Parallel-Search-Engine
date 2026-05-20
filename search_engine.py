import os
import time
from concurrent.futures import ThreadPoolExecutor

# 1. FILE CONTENT SEARCH FUNCTION (File open kar ke andar text dhoondna)
def search_inside_file(file_path, search_query):
    try:
        # Sirf text/code files ko check karne ke liye (Tathak reading errors na aayen)
        if file_path.endswith(('.txt', '.py', '.html', '.css', '.js', '.json', '.md', '.csv')):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if search_query.lower() in content.lower():
                    return file_path
    except Exception:
        pass
    return None

# 2. SERIAL CONTENT SEARCH
def serial_content_search(all_files, search_query):
    start_time = time.time()
    results = []
    for file_path in all_files:
        res = search_inside_file(file_path, search_query)
        if res:
            results.append(res)
    return results, time.time() - start_time

# 3. PARALLEL CONTENT SEARCH (Using Multi-threading for Heavy Disk Reading)
def parallel_content_search(all_files, search_query):
    start_time = time.time()
    results = []
    
    # 16 threads aik sath files open kar ke read karenge
    with ThreadPoolExecutor(max_workers=16) as executor:
        search_results = executor.map(lambda f: search_inside_file(f, search_query), all_files)
        for res in search_results:
            if res:
                results.append(res)
                
    return results, time.time() - start_time

if __name__ == "__main__":
    # Apni marzi ka folder path dein jahan kafi files hon (Jaise aapka high-performance project folder)
    target_folder = r"C:\Users\light tech\Downloads\High-Performance-Parallel-Search-Engine-main"
    keyword = "engine"  # Wo lafz jo files ke ANDAR dhoondna hai
    
    print(f"📖 Scanning file CONTENTS for the word '{keyword}'...\n")
    
    # Pehle saari files ki list bana lete hain
    all_files = []
    for root, dirs, files in os.walk(target_folder):
        for file in files:
            all_files.append(os.path.join(root, file))
            
    print(f"Total files to scan: {len(all_files)}\n")
    
    # Run Serial
    print("⏳ Running Serial Content Search...")
    s_res, s_time = serial_content_search(all_files, keyword)
    print(f"✅ Found in {len(s_res)} files | Time: {s_time:.4f} seconds.\n")
    
    # Run Parallel
    print("⚡ Running Parallel Content Search...")
    p_res, p_time = parallel_content_search(all_files, keyword)
    print(f"✅ Found in {len(p_res)} files | Time: {p_time:.4f} seconds.\n")
    
    # Speed difference
    if p_time < s_time:
        print(f"🚀 Parallel is {s_time/p_time:.2f}x FASTER because of multi-threaded disk reading!")
    else:
        print("💡 Tip: Try pointing to a larger folder with more text files to see the speed boost.")
