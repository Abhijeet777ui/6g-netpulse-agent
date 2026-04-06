import random
import time
import json

def generate_network_log():
    log = {
        "latency": random.randint(10, 100),
        "packet_loss": round(random.uniform(0, 1), 2),
        "throughput": random.randint(100, 1000),
        "devices": random.randint(50, 500),
        "status": "normal"
    }

    # Inject failures
    issue_trigger = random.random()

    if issue_trigger < 0.3:
        log["latency"] = random.randint(300, 600)
        log["status"] = "HIGH_LATENCY"

    elif issue_trigger < 0.6:
        log["packet_loss"] = round(random.uniform(5, 20), 2)
        log["status"] = "PACKET_LOSS"

    elif issue_trigger < 0.9:
        log["throughput"] = random.randint(1, 40)
        log["status"] = "LOW_THROUGHPUT"

    return log


if __name__ == "__main__":
    while True:
        log = generate_network_log()
        print(json.dumps(log, indent=2))
        time.sleep(5)