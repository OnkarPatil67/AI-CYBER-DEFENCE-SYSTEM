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

# MEMORY STRUCTURES

last_device = {}

# user threat intelligence database
user_profiles = {}

# EVENT GENERATORS

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

    username = event["username"]

    previous_device = last_device.get(username)

    device_change = (
        1 if previous_device and previous_device != event["device"]
        else 0
    )

    last_device[username] = event["device"]

    rapid_login = random.choice([0, 0, 0, 1])

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

# THREAT LEVEL LOGIC

def get_threat_level(risk_score):

    if risk_score >= 80:
        return "CRITICAL"

    elif risk_score >= 60:
        return "HIGH"

    elif risk_score >= 30:
        return "MEDIUM"

    else:
        return "LOW"

# START MONITORING

print("\n==========================================")
print(" AI THREAT INTELLIGENCE ENGINE STARTED ")
print("==========================================\n")

while True:

    # generate traffic
    if random.random() < 0.85:
        event = generate_normal_event()
        event_type = "NORMAL"

    else:
        event = generate_attack_event()
        event_type = "ATTACK"

    username = event["username"]

    # initialize user profile
    if username not in user_profiles:

        user_profiles[username] = {
            "risk_score": 0,
            "anomaly_count": 0,
            "total_logins": 0,
            "last_location": None
        }

    profile = user_profiles[username]

    # total activity
    profile["total_logins"] += 1

    print("\n----------------------------------")
    print(f"[{event_type}] LOGIN EVENT")
    print("----------------------------------")

    print(f"User: {username}")
    print(f"Location: {event['location']}")
    print(f"Device: {event['device']}")
    print(f"Status: {event['login_status']}")

    # FEATURE EXTRACTION

    features = extract_features(event)

    scaled_features = scaler.transform(features)

    prediction = model.predict(scaled_features)[0]

    score = model.decision_function(scaled_features)[0]

    # THREAT INTELLIGENCE

    if prediction == -1:

        print("\n🚨 ANOMALOUS BEHAVIOR DETECTED")

        profile["anomaly_count"] += 1

        # risk escalation
        profile["risk_score"] += 15

        # failed login escalation
        if event["login_status"] == "failed":
            profile["risk_score"] += 10

        # foreign login escalation
        if event["location"] in attack_locations:
            profile["risk_score"] += 15

        # successful suspicious login
        if (
            event["location"] in attack_locations
            and event["login_status"] == "success"
        ):
            print("\n⚠ POSSIBLE ACCOUNT TAKEOVER")

            profile["risk_score"] += 25

    else:

        # slight recovery
        profile["risk_score"] = max(
            0,
            profile["risk_score"] - 2
        )

        print("\n✅ Normal Behavior")

    # THREAT LEVEL
    
    threat_level = get_threat_level(
        profile["risk_score"]
    )

    # DISPLAY PROFILE
    
    print("\n========== USER PROFILE ==========")

    print(f"User: {username}")
    print(f"Risk Score: {profile['risk_score']}")
    print(f"Threat Level: {threat_level}")
    print(f"Anomaly Count: {profile['anomaly_count']}")
    print(f"Total Logins: {profile['total_logins']}")

    print("==================================")

    time.sleep(1)