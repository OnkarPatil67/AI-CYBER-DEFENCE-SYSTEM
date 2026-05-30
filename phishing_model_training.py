import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from scipy.sparse import hstack

from xgboost import XGBClassifier

# LOAD DATASET


df = pd.read_csv("final_preprocessed_emails.csv")

# INPUTS

df.dropna(subset=['cleaned_text'], inplace=True)
X_text = df['cleaned_text'].fillna('')

# Engineered numerical features
X_features = df[
    [
        'url_count',
        'email_count',
        'special_char_count',
        'uppercase_count',
        'text_length',
        'urgent_keyword_count'
    ]
]

y = df['label']

# TF-IDF VECTORIZATION

tfidf = TfidfVectorizer(
    max_features=5000
)

X_tfidf = tfidf.fit_transform(X_text)

# COMBINE FEATURES

X_final = hstack([X_tfidf, X_features])

# TRAIN TEST SPLIT

X_train, X_test, y_train, y_test = train_test_split(
    X_final,
    y,
    test_size=0.2,
    random_state=42
)
# MODEL


model = XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    use_label_encoder=False,
    eval_metric='logloss'
)

# TRAIN

model.fit(X_train, y_train)

# PREDICTIONS

y_pred = model.predict(X_test)

# Probability scores
y_prob = model.predict_proba(X_test)[:, 1]

# EVALUATION

accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:")
print(accuracy)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# SAMPLE RISK SCORES

print("\nSample Risk Scores:")

for i in range(5):

    print(
        f"Prediction: {y_pred[i]} | "
        f"Risk Score: {round(y_prob[i] * 100, 2)}%"
    )

# SAVE MODEL + TFIDF


joblib.dump(model, "xgboost_phishing_model.pkl")
joblib.dump(tfidf, "tfidf_vectorizer.pkl")

print("\nModel and TF-IDF vectorizer saved successfully.")