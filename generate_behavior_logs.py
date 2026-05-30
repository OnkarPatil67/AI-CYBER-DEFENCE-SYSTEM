import pandas as pd
import random
from datetime import datetime, timedelta

# SETTINGS

NUM_RECORDS = 5000

users = [
    "soham",
    "prachi",
    "rahul",
    "aditya",
    "neha",
    "amit",
    "john",
    "alice"
]

locations = [
    "Pune",
    "Mumbai",
    "Delhi",
    "Bangalore"
]

devices = [
    "Windows",
    "MacBook",
    "Android",
    "iPhone"
]

statuses = [
    "success",
    "failed"
]

# START TIME

base_time = datetime.now()

data = []

# NORMAL BEHAVIOR GENERATION

for i in range(NUM_RECORDS):

    user = random.choice(users)

    # normal users usually use same city
    if user == "soham":
        location = "Pune"
    elif user == "prachi":
        location = "Mumbai"
    else:
        location = random.choice(locations)

    device = random.choice(devices)

    # mostly successful logins
    status = random.choices(
        statuses,
        weights=[90, 10]
    )[0]

    # realistic login timing
    timestamp = base_time + timedelta(
        minutes=random.randint(1, 100000)
    )

    # generate IP
    ip = f"192.168.{random.randint(1,10)}.{random.randint(1,255)}"

    data.append([
        timestamp,
        user,
        ip,
        location,
        device,
        status,
        0  # normal
    ])

# ATTACK / ANOMALY GENERATION

for i in range(500):

    user = random.choice(users)

    # suspicious foreign-like location
    location = random.choice([
        "Russia",
        "China",
        "Unknown"
    ])

    device = random.choice(devices)

    # more failed attempts
    status = random.choices(
        statuses,
        weights=[20, 80]
    )[0]

    timestamp = base_time + timedelta(
        minutes=random.randint(1, 100000)
    )

    # weird IP range
    ip = f"10.0.{random.randint(50,99)}.{random.randint(1,255)}"

    data.append([
        timestamp,
        user,
        ip,
        location,
        device,
        status,
        1  # anomaly
    ])

# CREATE DATAFRAME

df = pd.DataFrame(data, columns=[
    "timestamp",
    "username",
    "ip_address",
    "location",
    "device",
    "login_status",
    "anomaly"
])

# shuffle dataset
df = df.sample(frac=1).reset_index(drop=True)

# SAVE

df.to_csv("behavior_log_dataset.csv", index=False)

print("\nDataset Created Successfully")
print(df.head())
print("\nShape:", df.shape)