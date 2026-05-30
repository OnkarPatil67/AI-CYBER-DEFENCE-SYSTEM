import pandas as pd
import joblib
import time

# LOAD MODEL + SCALER

model = joblib.load("anomaly_model.pkl")
scaler = joblib.load("anomaly_scaler.pkl")

# LOAD FEATURE DATASET

df = pd.read_csv("processed_behavior_logs.csv")

# FEATURE COLUMNS

feature_columns = [
    "login_hour",
    "failed_attempt",
    "foreign_login",
    "suspicious_ip",
    "device_change",
    "rapid_login",
    "odd_hour_login"
]

# REAL-TIME MONITORING

print("\n======================================")
print(" REAL-TIME CYBER MONITORING STARTED ")
print("======================================\n")

alert_count = 0

# stream records one-by-one
for index, row in df.iterrows():

    # extract features
    features = row[feature_columns].values.reshape(1, -1)

    # scale
    scaled_features = scaler.transform(features)

    # predict
    prediction = model.predict(scaled_features)[0]

    # anomaly score
    score = model.decision_function(scaled_features)[0]

    username = row["username"]
    location = row["location"]
    ip = row["ip_address"]
    status = row["login_status"]

    print("\n----------------------------------")
    print(f"User: {username}")
    print(f"Location: {location}")
    print(f"IP Address: {ip}")
    print(f"Login Status: {status}")

    # anomaly detected
    if prediction == -1:

        alert_count += 1

        print("\n🚨 ALERT: ANOMALOUS LOGIN DETECTED")

        print(f"Anomaly Score: {score:.4f}")

        # threat level
        if score < -0.20:
            threat = "HIGH"
        elif score < 0:
            threat = "MEDIUM"
        else:
            threat = "LOW"

        print(f"Threat Level: {threat}")

    else:
        print("\n✅ Normal Activity")

    print("----------------------------------")

    # simulate live stream
    time.sleep(0.5)

# FINAL SUMMARY

print("\n======================================")
print(" MONITORING SESSION COMPLETE ")
print("======================================")

print(f"\nTotal Alerts Generated: {alert_count}")