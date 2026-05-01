from scapy.all import sniff, IP, TCP, UDP, raw
from database import log_packet, log_alert, init_db
from signature import SignatureEngine
from anomaly import AnomalyDetector
from ips import block_ip, is_blocked
import threading
import time

signature_engine = SignatureEngine()
anomaly_detector = AnomalyDetector()

def process_packet(packet):
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        
        # IPS Check - Drop packet if blocked
        if is_blocked(src_ip):
            return
            
        protocol = "Other"
        src_port = 0
        dst_port = 0
        payload = ""
        length = len(packet)

        if TCP in packet:
            protocol = "TCP"
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
            try:
                payload = raw(packet[TCP].payload).decode('utf-8', errors='ignore')
            except Exception:
                pass
        elif UDP in packet:
            protocol = "UDP"
            src_port = packet[UDP].sport
            dst_port = packet[UDP].dport
            try:
                payload = raw(packet[UDP].payload).decode('utf-8', errors='ignore')
            except Exception:
                pass
        
        # ML Anomaly Detection update
        anomaly_detector.update_stats(src_ip, length)
        is_anomalous, score = anomaly_detector.analyze(src_ip)
        
        if is_anomalous:
            # We don't want to log every single anomalous packet to alerts to prevent DB spam, 
            # maybe log periodically. But for this build, we'll log it if the score is very low.
            if score < -0.1: # Just a heuristic threshold to reduce spam
                desc = f"Anomalous Traffic volume detected. ML Score: {score:.2f}"
                log_alert(src_ip, dst_ip, "Traffic Anomaly", "MEDIUM", desc, "LOGGED")
                print(f"[ALERT] ML ANOMALY: {src_ip} -> {dst_ip} (Score: {score:.2f})")
        
        # Check for signatures
        alerts = signature_engine.analyze(src_ip, dst_ip, protocol, payload)
        
        if alerts:
            # Block the IP due to signature match
            block_ip(src_ip, f"Signature match: {alerts[0]['name']}")
        
        # Log to DB
        log_packet(src_ip, dst_ip, src_port, dst_port, protocol, length, payload)
        
        # For terminal output
        if alerts:
            print(f"[!] MALICIOUS PACKET: {protocol} {src_ip}:{src_port} -> {dst_ip}:{dst_port} | Len: {length}")
        else:
            print(f"[{protocol}] {src_ip}:{src_port} -> {dst_ip}:{dst_port} | Len: {length}")

def start_sniffing(interface=None):
    print(f"Starting packet capture on interface: {interface if interface else 'default'}")
    # Run sniff in a separate thread so it doesn't block entirely if used as a module
    sniff(iface=interface, prn=process_packet, store=False)

if __name__ == "__main__":
    init_db()
    # On macOS, en0 is typical for Wi-Fi. 
    # Must be run with sudo for raw sockets!
    start_sniffing(interface="en0")
