from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI(title="Hybrid IDS/IPS Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.path.join(os.path.dirname(__file__), "ids.db")

def query_db(query: str, args=(), one=False):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    try:
        cur.execute(query, args)
        rv = cur.fetchall()
        return (rv[0] if rv else None) if one else rv
    except Exception as e:
        print(f"DB Error: {e}")
        return None
    finally:
        conn.close()

@app.get("/api/stats")
def get_stats():
    """Returns basic stats for dashboard overview."""
    total_packets_res = query_db("SELECT COUNT(*) as count FROM packets", one=True)
    total_alerts_res = query_db("SELECT COUNT(*) as count FROM alerts", one=True)
    
    return {
        "total_packets": total_packets_res['count'] if total_packets_res else 0,
        "total_alerts": total_alerts_res['count'] if total_alerts_res else 0,
        "active_threats": query_db("SELECT COUNT(*) as count FROM alerts WHERE timestamp > datetime('now', '-1 hour')", one=True)['count']
    }

@app.get("/api/alerts")
def get_alerts(limit: int = 50):
    """Returns latest alerts."""
    res = query_db(f"SELECT * FROM alerts ORDER BY timestamp DESC LIMIT {limit}")
    return [dict(row) for row in res] if res else []

@app.get("/api/traffic")
def get_traffic(limit: int = 50):
    """Returns latest captured packets."""
    res = query_db(f"SELECT id, timestamp, src_ip, dst_ip, src_port, dst_port, protocol, length FROM packets ORDER BY timestamp DESC LIMIT {limit}")
    return [dict(row) for row in res] if res else []

if __name__ == "__main__":
    import uvicorn
    # Start the FastAPI server locally on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
