import pandas as pd

df = pd.read_csv("final_dataset_clean.csv")

print("Initial shape:", df.shape)
print(df['label'].value_counts())
def is_valid_email(text):
    text = str(text).lower()

    # must look like email-ish text
    email_signals = ["@", "meeting", "regards", "dear", "team", "subject"]

    return any(sig in text for sig in email_signals)

df = df[df['text'].apply(is_valid_email)]
df = df.dropna()
df = df[df['text'].str.len() > 30]
df = df.drop_duplicates()
safe_df = df[df['label'] == 0]

def is_good_safe_email(text):
    text = text.lower()

    # must NOT contain phishing signals
    bad_signals = ["http", "login", "password", "verify", "otp", "bank"]

    if any(b in text for b in bad_signals):
        return False

    # must look like communication
    structure_signals = ["regards", "dear", "team", "meeting", "thanks"]

    return any(s in text for s in structure_signals)

safe_df = safe_df[safe_df['text'].apply(is_good_safe_email)]
phish_df = df[df['label'] == 1]

def is_good_phishing(text):
    text = text.lower()

    signals = ["login", "password", "verify", "urgent", "account", "click", "http"]

    return any(s in text for s in signals)

phish_df = phish_df[phish_df['text'].apply(is_good_phishing)]
final_df = pd.concat([safe_df, phish_df])

final_df = final_df.sample(frac=1, random_state=42)

print("Final shape:", final_df.shape)
print(final_df['label'].value_counts())
final_df.to_csv("clean_email_dataset_v2.csv", index=False)
print("Saved clean_email_dataset_v2.csv")
