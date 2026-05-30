import torch
import numpy as np
import json
from datetime import datetime
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification

# 1. LOAD MODEL

model_path = "distilbert_final_model"

tokenizer = DistilBertTokenizerFast.from_pretrained(model_path)
model = DistilBertForSequenceClassification.from_pretrained(model_path)
model.eval()

# 2. SOFTMAX

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

# 3. SAVE ALERT (SOC PIPELINE)

def save_alert(alert):
    try:
        with open("alerts.json", "r") as f:
            data = json.load(f)
    except:
        data = []

    data.insert(0, alert)
    data = data[:50]

    with open("alerts.json", "w") as f:
        json.dump(data, f, indent=4)

# 4. PREDICTION FUNCTION

def predict_email(text):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits.numpy()[0]

    probs = softmax(logits)

    safe_prob = probs[0]
    phish_prob = probs[1]

    # RISK SCORE
    
    risk_score = phish_prob * 100
    risk_score = max(0, min(100, risk_score))

    # LABEL LOGIC
    
    if risk_score >= 75:
        label = "⚠️ PHISHING EMAIL"
        threat = "HIGH"
    elif risk_score >= 40:
        label = "⚠️ SUSPICIOUS EMAIL"
        threat = "MEDIUM"
    else:
        label = "✅ SAFE EMAIL"
        threat = "LOW"

    # EXPLANATION LAYER
    
    indicators = []
    text_lower = text.lower()

    if "http" in text_lower:
        indicators.append("Contains URL")

    if "urgent" in text_lower:
        indicators.append("Urgency detected")

    if "password" in text_lower or "login" in text_lower:
        indicators.append("Credential request pattern")

    # ALERT GENERATION (IMPORTANT)

    if threat in ["HIGH", "MEDIUM"]:

        alert = {
            "title": "Phishing Email Detection",
            "description": text[:120],
            "label": label,
            "risk_score": round(risk_score, 2),
            "threat_level": threat,
            "indicators": indicators,
            "time": str(datetime.now())
        }

        save_alert(alert)

    # RETURN RESULT

    return {
        "label": label,
        "risk_score": round(risk_score, 2),
        "safe_probability": round(float(safe_prob), 4),
        "phishing_probability": round(float(phish_prob), 4),
        "threat_level": threat,
        "indicators": indicators
    }

# 5. TEST LOOP

if __name__ == "__main__":

    while True:
        print("\nEnter Email Text:")
        text = input()

        result = predict_email(text)

        print("\n=========================")
        print(result["label"])
        print("Risk Score:", result["risk_score"], "%")
        print("Threat Level:", result["threat_level"])
        print("Phishing Prob:", result["phishing_probability"])
        print("Safe Prob:", result["safe_probability"])

        print("\nDetected Indicators:")
        for i in result["indicators"]:
            print("-", i)

        print("=========================")
        