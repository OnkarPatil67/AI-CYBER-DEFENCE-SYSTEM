import torch
import numpy as np
import json

from datetime import datetime

from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification
)

# LOAD MODEL

model_path = "distilbert_final_model"

tokenizer = DistilBertTokenizerFast.from_pretrained(
    model_path
)

model = DistilBertForSequenceClassification.from_pretrained(
    model_path
)

model.eval()

# SOFTMAX

def softmax(x):

    e_x = np.exp(x - np.max(x))

    return e_x / e_x.sum()

# SAVE ALERT

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

# PREDICT EMAIL

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

    # INDICATORS

    indicators = []

    text_lower = text.lower()

    if "http" in text_lower:
        indicators.append("Contains URL")

    if "urgent" in text_lower:
        indicators.append("Urgency detected")

    if "password" in text_lower or "login" in text_lower:
        indicators.append("Credential request pattern")

    # SAVE ALERT
    
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

        "safe_probability": round(
            float(safe_prob), 4
        ),

        "phishing_probability": round(
            float(phish_prob), 4
        ),

        "threat_level": threat,

        "indicators": indicators
    }