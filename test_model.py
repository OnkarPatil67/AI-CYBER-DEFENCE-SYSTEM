import pandas as pd
from predict_final import predict_email

# LOAD TEST DATA

df = pd.read_csv("test_similar_data.csv")

total = len(df)
correct = 0

print("\n==============================")
print("MODEL TESTING STARTED")
print("==============================\n")

# EVALUATE EACH SAMPLE

for i, row in df.iterrows():

    text = row["text"]
    true_label = row["label"]

    result = predict_email(text)

    # convert model output → binary label
    pred_label = 1 if "PHISHING" in result["label"] else 0

    is_correct = (pred_label == true_label)

    if is_correct:
        correct += 1

    print("TEXT:", text)
    print("TRUE LABEL:", true_label)
    print("PRED LABEL:", pred_label)
    print("RISK SCORE:", result["risk_score"])
    print("CORRECT:", is_correct)
    print("------------------------------")

# FINAL ACCURACY

accuracy = correct / total

print("\n==============================")
print("FINAL RESULTS")
print("==============================")
print(f"Total Samples: {total}")
print(f"Correct Predictions: {correct}")
print(f"Accuracy: {accuracy:.4f}")
print("==============================")