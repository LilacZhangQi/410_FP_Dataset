import pandas as pd

enron_df = pd.read_csv("../data/enron_spam_data.csv", index_col=0)

enron_df = enron_df.rename(columns={
    "Subject": "subject",
    "Message": "message",
    "Spam/Ham": "label",
    "Date": "date"
})

enron_df["label"] = enron_df["label"].map({
    "spam": 1,
    "ham": 0
})

spamassassin_df = pd.read_csv("../data/spamassassin.csv")

combined_df = pd.concat([enron_df, spamassassin_df], ignore_index=True)

combined_df = combined_df.dropna(subset=["message"])

combined_df = combined_df.drop_duplicates(subset=["subject", "message"])

print(combined_df.head())
print(combined_df.shape)
print(combined_df["label"].value_counts())

print(combined_df.columns.tolist())
print(combined_df.isnull().sum())
print(combined_df["label"].unique())

combined_df.to_csv("../data/combined_email_dataset.csv", index=False)
print("Saved to ../data/combined_email_dataset.csv")