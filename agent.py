def allocate_bandwidth():
    return "✅ Action: Bandwidth increased to reduce latency"

def block_ip():
    return "🚫 Action: Suspicious IP blocked due to packet loss"

def reboot_tower():
    return "🔄 Action: Tower rebooted to restore throughput"


def simple_agent(log):
    if log["latency"] > 200:
        return allocate_bandwidth()

    elif log["packet_loss"] > 5:
        return block_ip()

    elif log["throughput"] < 50:
        return reboot_tower()

    else:
        return "✅ No issues detected. Network stable."