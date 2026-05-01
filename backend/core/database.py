import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "ids.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Packets log
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS packets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            src_ip TEXT,
            dst_ip TEXT,
            src_port INTEGER,
            dst_port INTEGER,
            protocol TEXT,
            length INTEGER,
            payload TEXT
        )
    """)
    
    # Alerts log
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            src_ip TEXT,
            dst_ip TEXT,
            threat_type TEXT,
            severity TEXT,
            description TEXT,
            action_taken TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def log_packet(src_ip, dst_ip, src_port, dst_port, protocol, length, payload):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO packets (src_ip, dst_ip, src_port, dst_port, protocol, length, payload)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (src_ip, dst_ip, src_port, dst_port, protocol, length, payload))
    conn.commit()
    conn.close()

def log_alert(src_ip, dst_ip, threat_type, severity, description, action_taken):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO alerts (src_ip, dst_ip, threat_type, severity, description, action_taken)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (src_ip, dst_ip, threat_type, severity, description, action_taken))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
