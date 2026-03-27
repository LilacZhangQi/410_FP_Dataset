import pandas as pd

df = pd.read_csv("../data/enron_spam_data.csv", index_col=0)

print("=== BEFORE ===")
print(df.head())

print(df.columns.tolist())

print(df["Spam/Ham"].value_counts())

#rename + label

df = df.rename(columns={
    "Subject": "subject",
"Message": "message",
"Spam/Ham": "label",
"Date": "date"
})

df["label"] = df["label"].map({"spam": 1, "ham": 0})

print("=== AFTER ===")
print(df.head())
print(df.head())
print(df["label"].value_counts())