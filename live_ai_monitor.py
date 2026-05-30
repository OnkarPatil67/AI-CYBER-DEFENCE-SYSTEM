import random
import time
import pandas as pd
import joblib
from datetime import datetime

# LOAD MODEL + SCALER

model = joblib.load("anomaly_model.pkl")
scaler = joblib.load("anomaly_scaler.pkl")

# USERS

users = [
    "soham",
    "prachi",
    "rahul",
    "aditya",
    "neha",
    "amit"
]

# NORMAL LOCATIONS

normal_locations = {
    "soham": "Pune",
    "prachi": "Mumbai",
    "rahul": "Delhi",
    "aditya": "Bangalore",
    "neha": "Pune",
    "amit": "Mumbai"
}

# DEVICES

devices = [
    "Windows",
    "MacBook",
    "Android",
    "iPhone"
]

# ATTACK LOCATIONS

attack_locations = [
    "Russia",
    "China",
    "Unknown"
]

# TRACK LAST DEVICE

last_device = {}

# GENERATE NORMAL EVENT

def generate_normal_event():

    user = random.choice(users)

    return {
        "timestamp": datetime.now(),
        "username": user,
        "location": normal_locations[user],
        "device": random.choice(devices),
        "login_status": random.choices(
            ["success", "failed"],
            weights=[95, 5]
        )[0],
        "ip_address": f"192.168.{random.randint(1,10)}.{random.randint(1,255)}"
    }

# GENERATE ATTACK EVENT

def generate_attack_event():

    user = random.choice(users)

    return {
        "timestamp": datetime.now(),
        "username": user,
        "location": random.choice(attack_locations),
        "device": random.choice(devices),
        "login_status": random.choices(
            ["success", "failed"],
            weights=[20, 80]
        )[0],
        "ip_address": f"10.0.{random.randint(50,99)}.{random.randint(1,255)}"
    }

# FEATURE EXTRACTION

def extract_features(event):

    login_hour = event["timestamp"].hour

    failed_attempt = (
        1 if event["login_status"] == "failed"
        else 0
    )

    foreign_login = (
        1 if event["location"] in attack_locations
        else 0
    )

    suspicious_ip = (
        1 if event["ip_address"].startswith("10.0.")
        else 0
    )

    # device change
    username = event["username"]

    previous_device = last_device.get(username)

    device_change = (
        1 if previous_device and previous_device != event["device"]
        else 0
    )

    last_device[username] = event["device"]

    # rapid login simulation
    rapid_login = random.choice([0, 0, 0, 1])

    # odd hour detection
    odd_hour_login = (
        1 if login_hour < 5 or login_hour > 23
        else 0
    )

    return pd.DataFrame([[
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

# LIVE MONITORING

print("\n======================================")
print(" LIVE AI CYBER DEFENSE SYSTEM STARTED ")
print("======================================\n")

alert_count = 0

while True:

    # normal vs attack traffic
    if random.random() < 0.85:
        event = generate_normal_event()
        event_type = "NORMAL"

    else:
        event = generate_attack_event()
        event_type = "ATTACK"

    print("\n----------------------------------")
    print(f"[{event_type}] LOGIN EVENT")
    print("----------------------------------")

    print(f"User: {event['username']}")
    print(f"Location: {event['location']}")
    print(f"Device: {event['device']}")
    print(f"IP: {event['ip_address']}")
    print(f"Status: {event['login_status']}")

    # extract features
    features = extract_features(event)

    # scale
    scaled_features = scaler.transform(features)

    # prediction
    prediction = model.predict(scaled_features)[0]

    # anomaly score
    score = model.decision_function(scaled_features)[0]

    # results
    if prediction == -1:

        alert_count += 1

        print("\n🚨 AI ALERT: ANOMALOUS ACTIVITY DETECTED")

        print(f"Anomaly Score: {score:.4f}")

        if score < -0.20:
            threat = "HIGH"
        elif score < 0:
            threat = "MEDIUM"
        else:
            threat = "LOW"

        print(f"Threat Level: {threat}")

    else:
        print("\n✅ Normal User Behavior")

    print(f"\nTotal Alerts Generated: {alert_count}")

    # live stream speed
    time.sleep(1)