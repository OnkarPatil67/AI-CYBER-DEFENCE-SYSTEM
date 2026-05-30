import pandas as pd
import joblib

# LOAD TRAINED MODEL

model = joblib.load("anomaly_model.pkl")
scaler = joblib.load("anomaly_scaler.pkl")

# REAL-TIME LOGIN INPUT

print("\n====== REAL-TIME LOGIN MONITOR ======\n")

login_hour = int(input("Login Hour (0-23): "))
failed_attempt = int(input("Failed Login? (1=yes, 0=no): "))
foreign_login = int(input("Foreign Login? (1=yes, 0=no): "))
suspicious_ip = int(input("Suspicious IP? (1=yes, 0=no): "))
device_change = int(input("New Device? (1=yes, 0=no): "))
rapid_login = int(input("Rapid Login Activity? (1=yes, 0=no): "))
odd_hour_login = int(input("Odd Hour Login? (1=yes, 0=no): "))

# CREATE FEATURE VECTOR

features = pd.DataFrame([[
    login_hour,
    failed_attempt,
    foreign_login,
    suspicious_ip,
    device_change,
    rapid_login,
    odd_hour_login
]], columns=[
    "login_hour",
    "failed_attempt",
    "foreign_login",
    "suspicious_ip",
    "device_change",
    "rapid_login",
    "odd_hour_login"
])

# SCALE FEATURES

scaled_features = scaler.transform(features)

# PREDICT

prediction = model.predict(scaled_features)[0]

# anomaly score
score = model.decision_function(scaled_features)[0]

# RESULTS

print("\n=========================")

if prediction == -1:
    print("🚨 ANOMALY DETECTED")
else:
    print("✅ NORMAL LOGIN ACTIVITY")

print(f"Anomaly Score: {score:.4f}")

# lower score = more suspicious
if score < -0.15:
    threat = "HIGH"
elif score < 0:
    threat = "MEDIUM"
else:
    threat = "LOW"

print(f"Threat Level: {threat}")

print("=========================")