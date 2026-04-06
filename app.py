import streamlit as st
import time
import pandas as pd
from collections import deque
from simulator import generate_network_log
from ai_agent import run_ai_agent
from datetime import datetime

st.set_page_config(
    page_title="6G Self-Healing Network Agent",
    layout="wide",
    page_icon="📡"
)

# ── Custom CSS for visual flash on critical status ──────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.critical-flash {
    animation: flashRed 1s ease-in-out 3;
    border-radius: 8px;
}
@keyframes flashRed {
    0%   { background-color: transparent; }
    50%  { background-color: rgba(255, 75, 75, 0.25); }
    100% { background-color: transparent; }
}

.reasoning-box {
    background: #1e2130;
    border-left: 4px solid #4e9af1;
    padding: 12px 16px;
    border-radius: 6px;
    color: #c9d1d9;
    font-size: 0.9rem;
    margin-top: 8px;
}

.confidence-label {
    font-size: 0.85rem;
    color: #8b949e;
    margin-bottom: 4px;
}
</style>
""", unsafe_allow_html=True)

# ── Session State ────────────────────────────────────────────────────────────
if "logs" not in st.session_state:
    st.session_state.logs = deque(maxlen=50)
if "actions" not in st.session_state:
    st.session_state.actions = deque(maxlen=5)
if "sim_running" not in st.session_state:
    st.session_state.sim_running = False

# ── Header ───────────────────────────────────────────────────────────────────
st.title("📡 6G Self-Healing Network Agent")
st.caption("Powered by Google Gemini AI · Real-time autonomous network management")
st.markdown("---")

# ── Controls ─────────────────────────────────────────────────────────────────
ctrl_col1, ctrl_col2 = st.columns([1, 3])
with ctrl_col1:
    if st.button("▶ Start / ⏹ Stop Simulation", use_container_width=True):
        st.session_state.sim_running = not st.session_state.sim_running

with ctrl_col2:
    refresh_speed = st.slider(
        "⏱ Simulation Speed (seconds per cycle)",
        min_value=1, max_value=10, value=3, step=1
    )

st.markdown("---")

# ── Safe default for decision ─────────────────────────────────────────────────
decision = {
    "action": "✅ No Action Needed",
    "reasoning": "Simulation not started yet.",
    "confidence": 0
}
is_critical = False

# ── Run simulation tick ───────────────────────────────────────────────────────
if st.session_state.sim_running:
    log = generate_network_log()
    decision = run_ai_agent(log)
    timestamp = datetime.now().strftime("%H:%M:%S")

    log_data = {"time": timestamp, **log}
    st.session_state.logs.append(log_data)

    is_critical = log.get("status") not in ("normal",)

    if decision and "No Action" not in decision["action"] and "Error" not in decision["action"]:
        st.session_state.actions.append({
            "time": timestamp,
            "action": decision["action"],
            "reasoning": decision["reasoning"],
            "confidence": decision["confidence"]
        })

# ── Metrics Row ───────────────────────────────────────────────────────────────
if st.session_state.logs:
    latest = list(st.session_state.logs)[-1]

    # Visual flash div when critical
    if is_critical:
        st.markdown('<div class="critical-flash">', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    prev = list(st.session_state.logs)[-2] if len(st.session_state.logs) >= 2 else latest
    m1.metric("⚡ Latency (ms)",      latest['latency'],     delta=latest['latency'] - prev['latency'],     delta_color="inverse")
    m2.metric("📉 Packet Loss (%)",   latest['packet_loss'], delta=latest['packet_loss'] - prev['packet_loss'], delta_color="inverse")
    m3.metric("🚀 Throughput (Mbps)", latest['throughput'],  delta=latest['throughput'] - prev['throughput'])
    m4.metric("📱 Active Devices",    latest['devices'],     delta=latest['devices'] - prev['devices'])

    if is_critical:
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("▶ Press **Start / Stop Simulation** to begin live monitoring.")

st.markdown("---")

# ── Charts Row (3 charts, each on its own Y-axis) ────────────────────────────
if st.session_state.logs:
    df = pd.DataFrame(list(st.session_state.logs)).set_index("time")
    ch1, ch2, ch3 = st.columns(3)
    with ch1:
        st.subheader("📈 Latency (ms)")
        st.line_chart(df[['latency']], height=200)
    with ch2:
        st.subheader("📈 Throughput (Mbps)")
        st.line_chart(df[['throughput']], height=200)
    with ch3:
        st.subheader("📈 Packet Loss (%)")
        st.line_chart(df[['packet_loss']], height=200)

st.markdown("---")

# ── AI Decision Panel + Action History ───────────────────────────────────────
ai_col, hist_col = st.columns(2)

with ai_col:
    st.subheader("🧠 AI Decision Panel")
    if st.session_state.logs:
        status = list(st.session_state.logs)[-1].get("status", "normal")

        # Status badge
        if status == "normal":
            st.success(f"🟢 **Network Status:** NORMAL")
        elif status == "HIGH_LATENCY":
            st.warning(f"🟡 **Network Status:** HIGH LATENCY")
        else:
            st.error(f"🔴 **Network Status:** {status.replace('_', ' ')}")

        # Action result
        action_text = decision["action"]
        if "No Action" in action_text:
            st.success(f"**Action:** {action_text}")
        elif "Error" in action_text or "Parse" in action_text:
            st.warning(f"**Action:** {action_text}")
        else:
            st.error(f"**Action:** {action_text}")

        # AI Reasoning (the real upgrade!)
        st.markdown(
            f'<div class="reasoning-box">💬 <strong>AI Reasoning:</strong><br>{decision["reasoning"]}</div>',
            unsafe_allow_html=True
        )

        # Confidence score
        conf = decision["confidence"]
        st.markdown(f'<p class="confidence-label">🎯 Confidence Score: {conf}%</p>', unsafe_allow_html=True)
        conf_color = "normal" if conf >= 70 else ("off" if conf < 40 else "normal")
        st.progress(conf / 100)

        # Raw log expander
        with st.expander("🔍 Raw Network Log"):
            st.json(list(st.session_state.logs)[-1])

with hist_col:
    st.subheader("🚨 Action History (Last 5)")
    if st.session_state.actions:
        for act in reversed(list(st.session_state.actions)):
            conf = act.get("confidence", 0)
            with st.expander(f"[{act['time']}] {act['action']}  · {conf}% confidence"):
                st.write(act.get("reasoning", "—"))
    else:
        st.write("No actions taken yet.")

    # ── Download Logs Button ──────────────────────────────────────────────
    st.markdown("---")
    if st.session_state.logs:
        df_export = pd.DataFrame(list(st.session_state.logs))
        csv = df_export.to_csv(index=False)
        st.download_button(
            label="⬇️ Export Session Logs as CSV",
            data=csv,
            file_name=f"netpulse_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

# ── Auto-refresh ──────────────────────────────────────────────────────────────
if st.session_state.sim_running:
    time.sleep(refresh_speed)
    st.rerun()
