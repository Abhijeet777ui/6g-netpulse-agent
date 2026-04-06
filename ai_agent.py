import os
import json
from google import genai
from dotenv import load_dotenv

# Load API key — supports both Streamlit Cloud (st.secrets) and local .env
load_dotenv()

def _get_api_key() -> str:
    # 1. Try Streamlit secrets (when deployed on Streamlit Cloud)
    try:
        import streamlit as st
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    # 2. Fall back to .env / system environment variable (local dev)
    return os.getenv("GEMINI_API_KEY", "")

client = genai.Client(api_key=_get_api_key())


# Actions
def allocate_bandwidth():
    return "✅ Bandwidth Allocated"

def block_ip():
    return "🚫 Suspicious IP Blocked"

def reboot_tower():
    return "🔄 Tower Rebooted"


def run_ai_agent(log):
    """
    Calls Gemini with a rich reasoning prompt.
    Returns a dict with keys: action, reasoning, confidence
    """

    # Skip API call for normal logs — saves quota
    if log.get("status") == "normal":
        return {
            "action": "✅ No Action Needed",
            "reasoning": "All network metrics are within normal operating thresholds. No intervention required.",
            "confidence": 95
        }

    prompt = f"""
You are an advanced AI controller for a 6G self-healing network.

Analyze the following real-time network log and decide what action to take:
{json.dumps(log, indent=2)}

Network Health Thresholds:
- Latency     : CRITICAL if > 200 ms
- Packet Loss : CRITICAL if > 5%
- Throughput  : CRITICAL if < 50 Mbps

Available Actions:
- allocate_bandwidth : Use when latency is too high
- block_ip           : Use when packet loss is abnormally high (possible attack or faulty node)
- reboot_tower       : Use when throughput is critically low
- no_action          : Use when all metrics are acceptable

Your response MUST be valid JSON only, no extra text. Example format:
{{
  "action": "allocate_bandwidth",
  "reasoning": "Latency is 420ms, far exceeding the 200ms threshold. Allocating more bandwidth should reduce congestion.",
  "confidence": 92
}}

Rules:
- "action" must be one of: allocate_bandwidth, block_ip, reboot_tower, no_action
- "reasoning" must be 1-2 sentences explaining WHY you chose this action
- "confidence" must be an integer from 1 to 100
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        raw = response.text.strip()

        # Strip markdown code fences if Gemini wraps JSON in ```
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        result = json.loads(raw)

        # Map action string to function result
        action_str = result.get("action", "no_action")
        if action_str == "allocate_bandwidth":
            result["action"] = allocate_bandwidth()
        elif action_str == "block_ip":
            result["action"] = block_ip()
        elif action_str == "reboot_tower":
            result["action"] = reboot_tower()
        else:
            result["action"] = "✅ No Action Needed"

        return result

    except json.JSONDecodeError:
        return {
            "action": "⚠️ Parse Error",
            "reasoning": f"Gemini returned unexpected format: {raw[:200]}",
            "confidence": 0
        }
    except Exception as e:
        return {
            "action": "⚠️ AI Error",
            "reasoning": str(e),
            "confidence": 0
        }