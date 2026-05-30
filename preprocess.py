import pandas as pd

# LOAD DATASETS

enron_df = pd.read_csv("enron_spam_data.csv")
phishing_df = pd.read_csv("Phishing_Email.csv")

# CLEAN ENRON DATASET

# Keep useful columns only
enron_df = enron_df[['Subject', 'Message', 'Spam/Ham']]

# Rename columns
enron_df.columns = ['subject', 'message', 'label']

# Combine subject + message
enron_df['text'] = (
    enron_df['subject'].fillna('') + " " +
    enron_df['message'].fillna('')
)

# Convert labels
enron_df['label'] = enron_df['label'].map({
    'ham': 'safe',
    'spam': 'phishing'
})

# Keep only needed columns
enron_df = enron_df[['text', 'label']]

# CLEAN PHISHING DATASET

phishing_df = phishing_df[['Email Text', 'Email Type']]

# Rename columns
phishing_df.columns = ['text', 'label']

# Convert labels
phishing_df['label'] = phishing_df['label'].map({
    'Safe Email': 'safe',
    'Phishing Email': 'phishing'
})

# MERGE DATASETS

final_df = pd.concat([enron_df, phishing_df], ignore_index=True)

# REMOVE NULLS

final_df.dropna(inplace=True)

# Remove duplicates
final_df.drop_duplicates(inplace=True)

# BASIC CLEANING

final_df['text'] = final_df['text'].str.lower()

# SHOW DATASET INFO

print(final_df.head())
print("\nDataset Shape:", final_df.shape)

print("\nLabel Distribution:")
print(final_df['label'].value_counts())

# SAVE CLEAN DATASET

final_df.to_csv("cleaned_emails.csv", index=False)

print("\nCleaned dataset saved as cleaned_emails.csv")