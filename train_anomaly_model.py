import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

# LOAD FEATURE DATASET

df = pd.read_csv("anomaly_features.csv")

# SCALE FEATURES

scaler = StandardScaler()

X_scaled = scaler.fit_transform(df)

# TRAIN ISOLATION FOREST

model = IsolationForest(
    n_estimators=100,
    contamination=0.1,
    random_state=42
)

model.fit(X_scaled)

# PREDICTIONS

predictions = model.predict(X_scaled)

# Isolation Forest:
# -1 = anomaly
#  1 = normal

df["prediction"] = predictions

# ANOMALY COUNT

anomalies = df[df["prediction"] == -1]

print("\nTraining Complete")

print("\nTotal Records:", len(df))
print("Detected Anomalies:", len(anomalies))

# SAVE MODEL

joblib.dump(model, "anomaly_model.pkl")
joblib.dump(scaler, "anomaly_scaler.pkl")

print("\nModel Saved Successfully")