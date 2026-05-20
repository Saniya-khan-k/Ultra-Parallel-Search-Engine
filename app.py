import streamlit as st
import os
import time
import re
import csv
from io import StringIO
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Core Search Function
def search_inside_file(file_path, search_query):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            matches = []
            for line_num, line in enumerate(f, 1):
                if search_query.lower() in line.lower():
                    matches.append({"line_no": line_num, "text": line.strip()})
            if matches:
                return {"file_path": file_path, "matches": matches}
    except:
        pass
    return None

def serial_content_search(all_files, search_query):
    start_time = time.time()
    results = [search_inside_file(f, search_query) for f in all_files]
    return [r for r in results if r], time.time() - start_time

def parallel_content_search(all_files, search_query, workers, mode):
    start_time = time.time()
    PoolExecutor = ThreadPoolExecutor if mode == "⚡ Fast Mode (Multi-threading)" else ProcessPoolExecutor
    with PoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(lambda f: search_inside_file(f, search_query), all_files))
    return [r for r in results if r], time.time() - start_time

def convert_results_to_csv(results):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["File Path", "File Name", "Line Number", "Matched Text Snippet"])
    for item in results:
        f_name = os.path.basename(item['file_path'])
        for m in item['matches']:
            writer.writerow([item['file_path'], f_name, m['line_no'], m['text']])
    return output.getvalue()

# Main UI Setup
st.set_page_config(page_title="Enterprise Parallel Searcher", page_icon="⚙️", layout="wide")

st.title("⚙️ Enterprise High-Performance Parallel Search Engine")
st.markdown("An enterprise-grade file parsing benchmark utility leveraging high-concurrency architecture loops.")
st.divider()

# Sidebar Configuration
st.sidebar.header("🕹️ Search Dashboard Controls")
st.sidebar.markdown("### 📂 1. Select Folder Location:")

# Automated System Paths Setup
home_dir = os.path.expanduser("~")
downloads_path = os.path.join(home_dir, "Downloads")
desktop_path = os.path.join(home_dir, "Desktop")
documents_path = os.path.join(home_dir, "Documents")
project_path = os.getcwd() 

# Stable Dropdown Options
folder_options = {
    "📥 Downloads Folder": downloads_path,
    "💻 Desktop Folder": desktop_path,
    "📄 Documents Folder": documents_path,
    "📁 This Project Active Folder": project_path,
    "✏️ Custom Folder Path (Type Below)": "CUSTOM"
}

selected_label = st.sidebar.selectbox("🎯 Quick Location Select:", options=list(folder_options.keys()))

if folder_options[selected_label] == "CUSTOM":
    target_folder = st.sidebar.text_input("✍️ Type or Paste Folder Absolute Path:", value=downloads_path)
else:
    target_folder = folder_options[selected_label]

st.sidebar.info(f"📍 Active Folder Node:\n`{target_folder}`")
st.sidebar.divider()

st.sidebar.markdown("### 🔍 2. Search Parameters:")
keyword = st.sidebar.text_input("Word to find inside files:", "engine")

# USER FRIENDLY FIX: Emojis aur aasan text wala Dropdown Menu
file_filter = st.sidebar.selectbox(
    "Target File Type:",
    options=[
        "📂 All Formats (Search Everything)", 
        "🐍 Python Code Files", 
        "📄 Plain Text / Documents", 
        "🌐 Web Files (HTML, CSS, JS)"
    ]
)

parallel_mode = st.sidebar.radio(
    "Compute Speed Processing Mode:",
    options=["⚡ Fast Mode (Multi-threading)", "🚀 Turbo Mode (Multi-processing)"]
)

worker_count = st.sidebar.slider("Parallel CPU Workers:", min_value=2, max_value=32, value=16, step=2)

# Start Analysis Button
run_search = st.sidebar.button("🚀 Run Search Engine Pipeline", type="primary", use_container_width=True)

if run_search:
    if not target_folder or not os.path.exists(target_folder):
        st.error("❌ Folder path configuration error. Target directory node does not exist.")
    elif not keyword:
        st.warning("⚠️ Please provide a keyword string.")
    else:
        with st.spinner("Analyzing target directory items..."):
            # Clean Extension Mapping matching the new user-friendly texts
            ext_map = {
                "📂 All Formats (Search Everything)": ('.txt', '.py', '.html', '.css', '.js', '.json', '.md', '.csv'),
                "🐍 Python Code Files": ('.py',),
                "📄 Plain Text / Documents": ('.txt', '.md', '.csv'),
                "🌐 Web Files (HTML, CSS, JS)": ('.html', '.css', '.js')
            }
            
            selected_extensions = ext_map[file_filter]
            all_files = []
            for root, _, files in os.walk(target_folder):
                for file in files:
                    if file.lower().endswith(selected_extensions):
                        all_files.append(os.path.join(root, file))
            
        total_files = len(all_files)
        
        if total_files == 0:
            st.warning("0 readable files found matching your selected parameters.")
        else:
            with st.spinner("Calculating Baseline Speeds..."):
                s_res, s_time = serial_content_search(all_files, keyword)
                
            with st.spinner(f"Accelerating with Parallel Core Engines..."):
                p_res, p_time = parallel_content_search(all_files, keyword, worker_count, parallel_mode)
                
            # Analytics Section
            st.subheader("📊 Performance Statistics")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric(label="Total Files Scanned", value=f"{total_files}")
            m2.metric(label="Files Containing Word", value=f"{len(p_res)}")
            m3.metric(label="Standard Engine Time", value=f"{s_time:.4f}s")
            m4.metric(label="Parallel Engine Time", value=f"{p_time:.4f}s", delta=f"{s_time/p_time:.1f}x Faster")
            
            st.divider()
            
            g_col, a_col = st.columns(2)
            
            with g_col:
                fig, ax = plt.subplots(figsize=(5, 1.8))
                modes = ['Standard Search', f'Parallel Engine ({worker_count} Workers)']
                times = [s_time, p_time]
                ax.barh(modes, times, color=['#e74c3c', '#2ecc71'], height=0.35)
                ax.set_xlabel('Execution Speed Time (Seconds)')
                st.pyplot(fig)
                
            with a_col:
                speedup = s_time / p_time
                if speedup > 1:
                    st.success(f"### 🚀 Super Speed Achieved!\n\nYour parallel engine completed processing files **{speedup:.1f}x times faster** than standard system loops.")
                else:
                    st.warning("### 💡 Process Overhead Notice\n\nThe dataset is too small to display multi-core optimization efficiency metrics.")
            
            # Data Export Report
            if len(p_res) > 0:
                st.divider()
                st.subheader("💾 Export Search Report")
                csv_data = convert_results_to_csv(p_res)
                st.download_button(
                    label="📥 Download Search Results as Excel/CSV File",
                    data=csv_data,
                    file_name="search_results_report.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            st.divider()
            
            # Matched results explorer
            if len(p_res) > 0:
                st.subheader("🔍 Found Matches Explorer (Visual View)")
                for item in p_res:
                    file_name = os.path.basename(item['file_path'])
                    with st.expander(f"📄 {file_name} ── 🔴 {len(item['matches'])} Matches Found"):
                        for match in item['matches']:
                            raw_text = match['text']
                            compiled_regex = re.compile(re.escape(keyword), re.IGNORECASE)
                            highlighted_text = compiled_regex.sub(f'<mark style="background-color: #f7dc6f; padding: 2px 4px; border-radius: 3px; color: black; font-weight: bold;">\g<0></mark>', raw_text)
                            
                            st.markdown(
                                f"""
                                <div style="display: flex; align-items: center; border-left: 4px solid #2ecc71; padding-left: 10px; margin-bottom: 8px; background-color: #f8f9f9; padding-top: 5px; padding-bottom: 5px;">
                                    <span style="background-color: #34495e; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px; margin-right: 15px; font-weight: bold; min-width: 65px; text-align: center;">Line {match['line_no']}</span>
                                    <span style="font-family: monospace; font-size: 14px; color: #2c3e50; word-break: break-all;">{highlighted_text}</span>
                                </div>
                                """, 
                                unsafe_allow_html=True
                            )
