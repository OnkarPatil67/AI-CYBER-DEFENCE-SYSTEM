import pandas as pd

data = [
    ["Hi team, meeting is scheduled tomorrow. Regards", 0],
    ["Please find attached report for review", 0],
    ["Your account has been suspended. Click link to verify http://fake.com", 1],
    ["Urgent: login to your account immediately", 1],
    ["Project update has been shared in drive", 0],
    ["Security alert: verify password now", 1]
]

df = pd.DataFrame(data, columns=["text", "label"])

df.to_csv("test_similar_data.csv", index=False)

print("CSV created successfully")