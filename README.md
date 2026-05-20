# ⚙️ Enterprise High-Performance Parallel Search Engine

An enterprise-grade, multi-threaded file parsing dashboard built with Python and Streamlit. This utility compares the performance benchmark of single-threaded sequential (Serial) search loops against highly concurrent asynchronous execution pools.

## 🚀 Key Features
- **Parallel Computing Framework**: Choose between Multi-threading (I/O optimized) and Multi-processing (Core-bound GIL bypass) modes.
- **Dynamic File Injection**: Instantly toggle target nodes like Downloads, Desktop, or the current active directory.
- **Smart Targeted Filters**: Filter specifically for Python Source files (`.py`), Document items (`.txt`, `.md`), or Web assets (`.html`, `.css`, `.js`).
- **Context Inspection Explorer**: View matching line numbers instantly with keyword text-highlighting badges.
- **Data Subsystem Extraction**: Export all matching logs to an Excel/CSV spreadsheet report with one click.

---

## 🛠️ Step-by-Step Local Deployment Guide

Follow these steps to download and execute this high-performance project on your local operating system:

### 1. Clone the Directory
First, download or clone the repository to your desktop machine:
```bash
git clone https://github.com
cd Ultra-Parallel-Search-Engine
```

### 2. Environment Schema Installation
Install the necessary package requirements using your local package installer manager (`pip`):
```bash
pip install -r requirements.txt
```

### 3. Launch the Analytical Dashboard
Execute the runtime processing controller script via the Streamlit layer:
```bash
streamlit run app.py
```
A web browser tab will automatically open at `http://localhost:8501` displaying the complete graphic pipeline.

---

## 📊 Technical Architecture Context (For Viva/Exams)
- **I/O Bound Offloading**: Multi-threading handles mass file data ingestion effectively by releasing the Global Interpreter Lock (GIL) during disk read activities.
- **Data Schema Serialization**: Matplotlib renders exact multi-core latency cycles, demonstrating up to **30x system efficiency throughput improvements**.

*Developed with ❤️ by Saniya-khan-k.*
