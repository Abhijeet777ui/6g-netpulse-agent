import time
from simulator import generate_network_log
# FIX: Removed unused 'simple_agent' import
from ai_agent import run_ai_agent

while True:
    log = generate_network_log()

    print("\n📡 NETWORK LOG:")
    print(log)

    decision = run_ai_agent(log)

    print("🤖 AGENT DECISION:")
    print(decision)

    time.sleep(5)