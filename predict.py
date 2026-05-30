import pandas as pd
import numpy as np
import re
import string
import joblib

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from scipy.sparse import hstack

# LOAD MODEL + TFIDF

model = joblib.load("xgboost_phishing_model.pkl")
tfidf = joblib.load("tfidf_vectorizer.pkl")

# NLP TOOLS

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# PHISHING KEYWORDS

urgent_keywords = [
    'urgent',
    'verify',
    'login',
    'password',
    'bank',
    'account',
    'click',
    'security',
    'limited',
    'immediately',
    'suspended',
    'confirm',
    'update',
    'credential',
    'ssn',
    'payment',
    'invoice',
    'reset',
    'alert',
    'unlock',
    'authenticate',
    'wallet',
    'otp',
    'expire',
    'deactivate',
    'restricted',
    'unauthorized',
    'signin',
    'validate'
]

# CLEAN TEXT FUNCTION

def clean_text(text):

    text = str(text).lower()

    # Remove URLs
    text = re.sub(r'http\S+', '', text)

    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)

    # Remove numbers
    text = re.sub(r'\d+', '', text)

    # Remove punctuation
    text = text.translate(
        str.maketrans('', '', string.punctuation)
    )

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    # Tokenization
    words = text.split()

    # Remove stopwords + lemmatize
    words = [
        lemmatizer.lemmatize(word)
        for word in words
        if word not in stop_words
    ]

    return " ".join(words)

# FEATURE ENGINEERING

def extract_features(text):

    url_count = len(
        re.findall(r'http[s]?://', str(text))
    )

    email_count = len(
        re.findall(r'\S+@\S+', str(text))
    )

    special_char_count = len(
        re.findall(r'[!#$%^&*(),.?":{}|<>]', str(text))
    )

    uppercase_count = sum(
        1 for c in str(text) if c.isupper()
    )

    text_length = len(str(text))

    urgent_keyword_count = sum(
        word in str(text).lower()
        for word in urgent_keywords
    )

    return [
        url_count,
        email_count,
        special_char_count,
        uppercase_count,
        text_length,
        urgent_keyword_count
    ]

# USER INPUT

email_input = input("\nEnter Email Text:\n")

# PREPROCESS

cleaned = clean_text(email_input)

# TF-IDF
text_vector = tfidf.transform([cleaned])

# Engineered Features
features = np.array(
    [extract_features(email_input)]
)

# Combine
final_input = hstack([
    text_vector,
    features
])

# MODEL PROBABILITY

probability = model.predict_proba(
    final_input
)[0][1]

# BASE AI SCORE

base_score = probability * 100

# HEURISTIC RULES

heuristic_score = 0

text_lower = email_input.lower()

# URL detection
if "http://" in text_lower or "https://" in text_lower:
    heuristic_score += 15

# Urgent keywords
urgent_matches = sum(
    word in text_lower
    for word in urgent_keywords
)

heuristic_score += urgent_matches * 3

# Excessive uppercase
uppercase_ratio = sum(
    1 for c in email_input if c.isupper()
) / max(len(email_input), 1)

if uppercase_ratio > 0.2:
    heuristic_score += 10

# Excessive special characters
special_count = len(
    re.findall(r'[!#$%^&*(),.?":{}|<>]', email_input)
)

if special_count > 10:
    heuristic_score += 5

# Very short suspicious email
if len(email_input.split()) < 10 and urgent_matches > 1:
    heuristic_score += 10

# SAFE EMAIL REDUCTIONS

safe_score_reduction = 0

professional_words = [
    'regards',
    'meeting',
    'project',
    'schedule',
    'team',
    'discussion',
    'attached'
]

professional_matches = sum(
    word in text_lower
    for word in professional_words
)

safe_score_reduction += professional_matches * 2

# Long structured emails
if len(email_input.split()) > 50:
    safe_score_reduction += 5

# FINAL RISK SCORE

risk_score = (
    base_score
    + heuristic_score
    - safe_score_reduction
)

# Normalize
risk_score = max(0, min(risk_score, 100))

risk_score = round(risk_score, 2)

# FINAL PREDICTION

if risk_score >= 60:
    prediction = 1
else:
    prediction = 0

# OUTPUT

print("\n=========================")

if prediction == 1:
    print("⚠️ PHISHING EMAIL DETECTED")
else:
    print("✅ SAFE EMAIL")

print(f"Risk Score: {risk_score:.2f}%")

# THREAT LEVEL

if risk_score >= 75:
    print("Threat Level: HIGH")

elif risk_score >= 40:
    print("Threat Level: MEDIUM")

else:
    print("Threat Level: LOW")

# SECURITY EXPLANATION

print("\nDetected Indicators:")

if "http://" in text_lower or "https://" in text_lower:
    print("- Suspicious URL detected")

if urgent_matches > 0:
    print(f"- {urgent_matches} phishing-related keywords found")

if uppercase_ratio > 0.2:
    print("- Excessive uppercase usage")

if special_count > 10:
    print("- Excessive special characters")

if professional_matches > 0:
    print("- Professional/corporate language detected")

print("=========================")