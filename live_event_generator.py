import random
import time
from datetime import datetime

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

# GENERATE NORMAL EVENT

def generate_normal_event():

    user = random.choice(users)

    event = {
        "timestamp": str(datetime.now()),
        "username": user,
        "location": normal_locations[user],
        "device": random.choice(devices),
        "login_status": random.choices(
            ["success", "failed"],
            weights=[95, 5]
        )[0],
        "ip_address": f"192.168.{random.randint(1,10)}.{random.randint(1,255)}"
    }

    return event

# GENERATE ATTACK EVENT

def generate_attack_event():

    user = random.choice(users)

    event = {
        "timestamp": str(datetime.now()),
        "username": user,
        "location": random.choice(attack_locations),
        "device": random.choice(devices),
        "login_status": random.choices(
            ["success", "failed"],
            weights=[20, 80]
        )[0],
        "ip_address": f"10.0.{random.randint(50,99)}.{random.randint(1,255)}"
    }

    return event

# LIVE EVENT STREAM

print("\n====================================")
print(" LIVE CYBER EVENT GENERATOR STARTED ")
print("====================================\n")

while True:

    # 85% normal traffic
    if random.random() < 0.85:
        event = generate_normal_event()
        event_type = "NORMAL"

    # 15% attack traffic
    else:
        event = generate_attack_event()
        event_type = "ATTACK"

    print(f"\n[{event_type}] EVENT DETECTED")
    print(event)

    # simulate real-time traffic
    time.sleep(1)