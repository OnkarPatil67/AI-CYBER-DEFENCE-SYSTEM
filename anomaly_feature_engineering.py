import pandas as pd

# LOAD LOGIN DATASET

df = pd.read_csv("behavior_log_dataset.csv")

# CONVERT TIMESTAMP

df["timestamp"] = pd.to_datetime(df["timestamp"])

# FEATURE 1: LOGIN HOUR

df["login_hour"] = df["timestamp"].dt.hour

# FEATURE 2: FAILED LOGIN FLAG
df["failed_attempt"] = df["login_status"].apply(
    lambda x: 1 if x == "failed" else 0
)

# FEATURE 3: FOREIGN LOGIN FLAG

foreign_locations = ["Russia", "China", "Unknown"]

df["foreign_login"] = df["location"].apply(
    lambda x: 1 if x in foreign_locations else 0
)

# FEATURE 4: SUSPICIOUS IP FLAG

df["suspicious_ip"] = df["ip_address"].apply(
    lambda x: 1 if x.startswith("10.0.") else 0
)

# FEATURE 5: DEVICE CHANGE

df = df.sort_values(by=["username", "timestamp"])

df["device_change"] = (
    df.groupby("username")["device"]
    .transform(lambda x: (x != x.shift()).astype(int))
)

# FEATURE 6: RAPID LOGIN DETECTION

df["time_diff"] = (
    df.groupby("username")["timestamp"]
    .diff()
    .dt.total_seconds()
)

df["time_diff"] = df["time_diff"].fillna(999999)

df["rapid_login"] = df["time_diff"].apply(
    lambda x: 1 if x < 60 else 0
)

# FEATURE 7: ODD HOUR LOGIN

df["odd_hour_login"] = df["login_hour"].apply(
    lambda x: 1 if x < 5 or x > 23 else 0
)

# SELECT FINAL FEATURES

feature_columns = [
    "login_hour",
    "failed_attempt",
    "foreign_login",
    "suspicious_ip",
    "device_change",
    "rapid_login",
    "odd_hour_login"
]

X = df[feature_columns]

# SAVE FEATURE DATASET

X.to_csv("anomaly_features.csv", index=False)

# Save full processed logs
df.to_csv("processed_behavior_logs.csv", index=False)

# OUTPUT

print("\nFeature Engineering Complete")
print("\nFeatures Created:")
print(feature_columns)

print("\nDataset Shape:")
print(X.shape)

print("\nSample Features:")
print(X.head())