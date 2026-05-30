import pandas as pd
import numpy as np
import torch

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments,
    EarlyStoppingCallback
)

# 1. LOAD CLEAN DATASET

df = pd.read_csv("clean_email_dataset_v2.csv")

df = df.dropna()
df = df.drop_duplicates()

texts = df["text"].tolist()
labels = df["label"].tolist()

# 2. TRAIN / TEST SPLIT (STRATIFIED)

train_texts, val_texts, train_labels, val_labels = train_test_split(
    texts,
    labels,
    test_size=0.2,
    random_state=42,
    stratify=labels
)

# 3. TOKENIZER

tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")

train_encodings = tokenizer(
    train_texts,
    truncation=True,
    padding=True,
    max_length=128
)

val_encodings = tokenizer(
    val_texts,
    truncation=True,
    padding=True,
    max_length=128
)

# 4. DATASET CLASS

class EmailDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = EmailDataset(train_encodings, train_labels)
val_dataset = EmailDataset(val_encodings, val_labels)

# 5. MODEL

model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=2
)

# 6. METRICS FUNCTION (IMPORTANT)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=1)

    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average="binary"
    )
    acc = accuracy_score(labels, preds)

    return {
        "accuracy": acc,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }

# 7. TRAINING ARGS (PRODUCTION STYLE)

training_args = TrainingArguments(
    output_dir="./distilbert_model",

    # core training
    num_train_epochs=2,
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,

    # evaluation control
    eval_strategy="epoch",
    save_strategy="epoch",

    # best model saving
    load_best_model_at_end=True,
    metric_for_best_model="f1",

    # stability
    weight_decay=0.01,

    # logging
    logging_dir="./logs",
    logging_steps=100,

    # performance
    fp16=torch.cuda.is_available()
)

# 8. TRAINER

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
)

# 9. TRAIN

trainer.train()

# 10. SAVE MODEL

model.save_pretrained("distilbert_final_model")
tokenizer.save_pretrained("distilbert_final_model")

print("\nTraining complete. Model saved as distilbert_final_model")