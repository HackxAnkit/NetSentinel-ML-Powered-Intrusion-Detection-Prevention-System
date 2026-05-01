import json
import re
import os
from database import log_alert

SIGNATURES_FILE = os.path.join(os.path.dirname(__file__), "..", "rules", "signatures.json")

class SignatureEngine:
    def __init__(self):
        self.rules = []
        self.load_rules()

    def load_rules(self):
        try:
            with open(SIGNATURES_FILE, 'r') as f:
                self.rules = json.load(f)
            
            # Precompile regex for speed
            for rule in self.rules:
                rule['regex'] = re.compile(rule['pattern'])
                
            print(f"Loaded {len(self.rules)} signatures.")
        except Exception as e:
            print(f"Error loading signatures: {e}")

    def analyze(self, src_ip, dst_ip, protocol, payload):
        """
        Analyze a packet payload against loaded signatures.
        Returns a list of alerts if a match is found.
        """
        if not payload:
            return []

        alerts_generated = []
        
        for rule in self.rules:
            if protocol == rule['protocol'] or rule['protocol'] == 'ALL':
                if rule['regex'].search(payload):
                    alert_desc = f"Signature Match: {rule['name']} - {rule['description']}"
                    # Log alert to DB
                    log_alert(
                        src_ip=src_ip,
                        dst_ip=dst_ip,
                        threat_type="Signature Match",
                        severity=rule['severity'],
                        description=alert_desc,
                        action_taken="LOGGED"
                    )
                    alerts_generated.append(rule)
                    print(f"[ALERT] {rule['severity']} Threat detected! {src_ip} -> {dst_ip} : {rule['name']}")
        
        return alerts_generated

if __name__ == "__main__":
    engine = SignatureEngine()
    test_payload = "GET /user?id=1' OR '1'='1 HTTP/1.1\r\nHost: example.com"
    engine.analyze("192.168.1.10", "10.0.0.5", "TCP", test_payload)
