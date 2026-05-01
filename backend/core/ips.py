import time

# In-memory blocklist
# In a real scenario, this would interface with pf (macOS firewall) or iptables:
# os.system(f"pfctl -t blocklist -T add {ip}")
BLOCKLIST = {}

# Time to block an IP (seconds) - e.g., 5 minutes
BLOCK_DURATION = 300

def block_ip(ip, reason=""):
    """
    Adds an IP to the blocklist.
    """
    print(f"[IPS] ACTION TAKEN: Blocking IP {ip}. Reason: {reason}")
    BLOCKLIST[ip] = time.time() + BLOCK_DURATION

def is_blocked(ip):
    """
    Checks if an IP is currently blocked.
    Returns True if blocked, False otherwise.
    """
    if ip in BLOCKLIST:
        if time.time() > BLOCKLIST[ip]:
            # Block expired
            del BLOCKLIST[ip]
            return False
        return True
    return False
