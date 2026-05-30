import pandas as pd
import re
import string

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# LOAD DATASET

df = pd.read_csv("cleaned_emails.csv")

# NLP TOOLS

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# PHISHING KEYWORDS

urgent_keywords = [
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
]

# FEATURE ENGINEERING

# URL count
df['url_count'] = df['text'].apply(
    lambda x: len(re.findall(r'http[s]?://', str(x)))
)

# Email address count
df['email_count'] = df['text'].apply(
    lambda x: len(re.findall(r'\S+@\S+', str(x)))
)

# Special character count
df['special_char_count'] = df['text'].apply(
    lambda x: len(re.findall(r'[!#$%^&*(),.?":{}|<>]', str(x)))
)

# Uppercase count
df['uppercase_count'] = df['text'].apply(
    lambda x: sum(1 for c in str(x) if c.isupper())
)

# Text length
df['text_length'] = df['text'].apply(len)

# Urgent keyword count
df['urgent_keyword_count'] = df['text'].apply(
    lambda x: sum(word in str(x).lower() for word in urgent_keywords)
)

# TEXT CLEANING FUNCTION

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

# APPLY CLEANING

df['cleaned_text'] = df['text'].apply(clean_text)

# LABEL ENCODING

df['label'] = df['label'].map({
    'safe': 0,
    'phishing': 1
})


# SHOW RESULTS

print(df.head())

print("\nDataset Shape:", df.shape)

# SAVE FINAL DATASET

df.to_csv("final_preprocessed_emails.csv", index=False)

print("\nFinal dataset saved as final_preprocessed_emails.csv")