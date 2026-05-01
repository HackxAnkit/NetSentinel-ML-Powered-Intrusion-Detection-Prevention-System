import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os
import time

MODEL_PATH = os.path.join(os.path.dirname(__file__), "isolation_forest.pkl")

class AnomalyDetector:
    def __init__(self):
        self.model = None
        self.traffic_stats = {}  # Store running stats per IP
        """
        traffic_stats structure:
        {
            "192.168.1.10": {
                "window_start": float,
                "packet_count": int,
                "byte_count": int
            }
        }
        """
        self.load_model()

    def load_model(self):
        if os.path.exists(MODEL_PATH):
            self.model = joblib.load(MODEL_PATH)
            print("Loaded Anomaly Detection Model.")
        else:
            print("No ML model found. Run train_model.py first! Running without ML anomaly detection.")

    def update_stats(self, src_ip, length):
        current_time = time.time()
        # 10 second window
        WINDOW_SIZE = 10.0
        
        if src_ip not in self.traffic_stats:
            self.traffic_stats[src_ip] = {
                "window_start": current_time,
                "packet_count": 0,
                "byte_count": 0
            }
            
        stats = self.traffic_stats[src_ip]
        
        # Reset window if expired
        if current_time - stats["window_start"] > WINDOW_SIZE:
            # Here we could record the completed window for history/training
            stats["window_start"] = current_time
            stats["packet_count"] = 0
            stats["byte_count"] = 0
            
        stats["packet_count"] += 1
        stats["byte_count"] += length

    def analyze(self, src_ip):
        """
        Analyze current stats for an IP and determine if it's anomalous.
        Returns Boolean (True if anomalous) and the anomaly score.
        """
        if not self.model or src_ip not in self.traffic_stats:
            return False, 0.0
            
        stats = self.traffic_stats[src_ip]
        
        # We need a minimum amount of traffic to make a judgment
        if stats["packet_count"] < 5:
            return False, 0.0
            
        # Features: [packet_count, byte_count]
        features = pd.DataFrame([{
            "packet_count": stats["packet_count"],
            "byte_count": stats["byte_count"]
        }])
        
        prediction = self.model.predict(features)[0] # 1 for normal, -1 for anomaly
        # score_samples returns negative distances. Lower values mean more anomalous.
        score = self.model.score_samples(features)[0] 
        
        if prediction == -1:
            return True, score
            
        return False, score

if __name__ == "__main__":
    detector = AnomalyDetector()
    detector.update_stats("10.0.0.5", 1500)
    print(detector.analyze("10.0.0.5"))
