# 📡 6G-NetPulse Agent

> An AI-powered, self-healing 6G network monitoring dashboard built with Python, Google Gemini, and Streamlit.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.5+-red?style=flat&logo=streamlit)
![Gemini AI](https://img.shields.io/badge/Google_Gemini-AI-orange?style=flat&logo=google)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

---

## 📊 Project Stats & Metrics

| Metric | Value |
|---|---|
| 🐍 Total Lines of Code | ~400 lines (across 5 Python files) |
| 📁 Source Files | 5 Python modules + 1 Streamlit entry point |
| 🧠 AI Model | Google Gemini 2.5 Flash |
| ⚙️ Autonomous Actions | 4 (`allocate_bandwidth`, `block_ip`, `reboot_tower`, `no_action`) |
| 📡 Simulated Network Metrics | 4 (Latency, Packet Loss, Throughput, Active Devices) |
| 📈 Live Charts | 3 independent real-time charts |
| 🗂 Rolling Log Window | 50 entries (in-memory, session-scoped) |
| 🔁 Action History Retained | Last 5 AI decisions |
| 🎯 Confidence Score Range | 1 – 100% |
| ⏱ Simulation Speed Range | 1 – 10 seconds per cycle |
| 🔴 Fault Injection Rate | ~90% of cycles simulate a network anomaly |
| ⚡ Latency Critical Threshold | > 200 ms |
| 📉 Packet Loss Critical Threshold | > 5% |
| 🚀 Throughput Critical Threshold | < 50 Mbps |
| ☁️ Deployment Platform | Streamlit Community Cloud (free tier) |
| 🔒 API Key Handling | `.env` locally · `st.secrets` on cloud (zero hardcoding) |

---

## 🚀 What It Does

6G-NetPulse Agent simulates a real-time 6G network monitoring system. A network simulator continuously generates logs (latency, packet loss, throughput, active devices). Google Gemini AI analyzes each log, explains its reasoning, gives a confidence score, and autonomously triggers corrective actions — all displayed on a live Streamlit dashboard.

---

## ✨ Features

- 📊 **Live Metrics** — Real-time KPI cards with delta indicators (↑↓)
- 📈 **3 Separate Charts** — Independent Y-axis charts for Latency, Throughput, and Packet Loss
- 🧠 **AI Reasoning Panel** — Gemini explains *why* it made each decision (not just what)
- 🎯 **Confidence Score** — Progress bar showing how confident the AI is (0–100%)
- 🔴 **Critical Flash** — Screen flashes red when a critical network event is detected
- 🚨 **Action History** — Expandable log of the last 5 AI decisions with reasoning
- ⏱ **Speed Slider** — Control how fast the simulation runs (1–10 seconds per cycle)
- ⬇️ **CSV Export** — Download the entire session's network logs as a CSV file
- 🔒 **Secure API Key** — Stored in `.env`, never hardcoded

---

## 🗂 Project Structure

```
Agent/
├── simulator.py       # Generates fake network logs with injected failures
├── agent.py           # Simple rule-based agent (baseline, no AI)
├── ai_agent.py        # Google Gemini AI agent (returns action + reasoning + confidence)
├── main.py            # Terminal-only loop for testing without UI
├── app.py             # Streamlit dashboard (main entry point)
├── requirements.txt   # All dependencies
├── .env               # Your API key (never commit this!)
├── .gitignore         # Excludes .env and venv from Git
└── README.md          # This file
```

---

## ⚡ Quickstart

### 1. Clone / Download the project

```bash
git clone https://github.com/YOUR_USERNAME/6g-netpulse-agent.git
cd 6g-netpulse-agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:
- **Windows (PowerShell):** `.\venv\Scripts\Activate.ps1`
- **Mac/Linux:** `source venv/bin/activate`

> If PowerShell blocks scripts, run once: `Set-ExecutionPolicy Unrestricted -Scope CurrentUser`

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your Gemini API Key

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_api_key_here
```

Get a free key at: https://aistudio.google.com/

### 5. Run the dashboard

```bash
streamlit run app.py
```

Or via venv Python directly:
```bash
.\venv\Scripts\python.exe -m streamlit run app.py
```

---

## 🛠 Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.10+ | Core language |
| Google Gemini 2.5 Flash (`google-genai`) | AI decision-making + reasoning |
| Streamlit | Interactive web dashboard |
| Pandas | Data handling for charts |
| python-dotenv | Secure API key management |

---

## 🧠 How the AI Works

Unlike simple rule-based systems, the Gemini agent:
1. **Reads the full network log** as context
2. **Reasons** about what the anomaly likely means
3. **Chooses an action** from: `allocate_bandwidth`, `block_ip`, `reboot_tower`, or `no_action`
4. **Returns a confidence score** (1–100%)
5. **Explains its decision** in plain English

All of this is displayed live in the dashboard.

---

## ☁️ Deploy on Streamlit Cloud (Share with Everyone)

1. Push this repo to **GitHub** (make sure `.env` is in `.gitignore` ✅)
2. Go to **[share.streamlit.io](https://share.streamlit.io)** and sign in with GitHub
3. Click **New app** → select your repo, branch `main`, file `app.py`
4. Go to **Settings → Secrets** and add:
   ```toml
   GEMINI_API_KEY = "your_api_key_here"
   ```
5. Click **Deploy** — you'll get a public URL like `https://your-app.streamlit.app` 🎉

> **Note:** The app uses `st.secrets["GEMINI_API_KEY"]` when running on Streamlit Cloud, and falls back to `.env` locally via `python-dotenv`.

---

## 📄 License

MIT — free to use, modify, and share.
