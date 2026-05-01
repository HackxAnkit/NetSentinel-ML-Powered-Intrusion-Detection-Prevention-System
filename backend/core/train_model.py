import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "isolation_forest.pkl")

def generate_synthetic_data(num_samples=1000):
    """
    Generate synthetic data for normal network traffic.
    Features:
    - packet_count: number of packets in a 10s window (normal: 5 to 50)
    - byte_count: total bytes in a 10s window (normal: 200 to 50000)
    """
    np.random.seed(42)
    
    # Normal traffic
    normal_packet_count = np.random.randint(5, 50, size=num_samples)
    normal_byte_count = normal_packet_count * np.random.randint(40, 1000, size=num_samples)
    
    normal_data = pd.DataFrame({
        'packet_count': normal_packet_count,
        'byte_count': normal_byte_count
    })
    
    # Anomalous traffic (for testing/visualization, though IsolationForest doesn't need labeled anomalies strictly for training)
    # Ping flood, DOS, large data exfil
    anomaly_packet_count = np.random.randint(200, 1000, size=int(num_samples * 0.05))
    anomaly_byte_count = anomaly_packet_count * np.random.randint(40, 1500, size=int(num_samples * 0.05))
    
    anomaly_data = pd.DataFrame({
        'packet_count': anomaly_packet_count,
        'byte_count': anomaly_byte_count
    })
    
    train_data = normal_data # Train mainly on normal traffic
    test_data = pd.concat([normal_data.sample(frac=0.2), anomaly_data])
    
    return train_data, test_data

def train_and_save():
    print("Generating synthetic network traffic data...")
    train_data, test_data = generate_synthetic_data()
    
    print(f"Training Isolation Forest on {len(train_data)} samples of normal traffic...")
    # contamination is the expected proportion of outliers. In our training set (pure normal), we set it low.
    model = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
    model.fit(train_data)
    
    # Test
    test_preds = model.predict(test_data)
    anomalies = test_data[test_preds == -1]
    
    print(f"Testing Model: Found {len(anomalies)} anomalies out of {len(test_data)} test samples.")
    
    # Save Model
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_and_save()
