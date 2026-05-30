import pandas as pd

enron_df = pd.read_csv("enron_spam_data.csv")
phishing_df = pd.read_csv("Phishing_Email.csv")

print("ENRON DATASET")
print(enron_df.columns)
print(enron_df.shape)
print(enron_df.head())

print("\nPHISHING DATASET")
print(phishing_df.columns)
print(phishing_df.shape)
print(phishing_df.head())