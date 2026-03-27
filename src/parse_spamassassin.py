import os
import pandas as pd
from email import policy
from email.parser import BytesParser

def extract_email_content(file_path):
    with open(file_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)

    subject = msg['subject'] or ""
    body_parts = []

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition", ""))

            if content_type == "text/plain" and "attachment" not in content_disposition:
                try:
                    payload = part.get_payload(decode=True)
                    if payload:
                        charset = part.get_content_charset() or "latin-1"
                        body_parts.append(payload.decode(charset, errors="ignore"))
                except Exception:
                    pass
    else :
        try:
            payload = msg.get_payload(decode=True)
            if payload:
                charset = msg.get_content_charset() or "latin-1"
                body_parts.append(payload.decode(charset, errors="ignore"))
        except Exception:
            pass
    message = "\n".join(body_parts).strip()
    return subject.strip(), message

def parse_folder(folder_path, label):
    rows = []

    for filename in os.listdir(folder_path):
        if filename.startswith(".") or filename.startswith("._"):
            continue
        file_path = os.path.join(folder_path, filename)

        if not os.path.isfile(file_path):
            continue

        try:
            subject, message = extract_email_content(file_path)
            rows.append({
                "subject": subject,
                "message": message,
                "label": label,
                "date": None
            })
        except Exception as e:
            print(f"skip {filename}: {e}")

    return pd.DataFrame(rows)

easy_ham_path = "../data/easy_ham"
hard_ham_path = "../data/hard_ham"
spam_path = "../data/spam_2"

easy_ham_df = parse_folder(easy_ham_path, 0)
hard_ham_df = parse_folder(hard_ham_path, 0)
spam_df = parse_folder(spam_path, 1)

spamassassin_df = pd.concat(
    [easy_ham_df, hard_ham_df, spam_df],
    ignore_index=True
)

print(spamassassin_df.head())
print(spamassassin_df.shape)
print(spamassassin_df["label"].value_counts())

spamassassin_df.to_csv("../data/spamassassin.csv", index=False)
print("Save to ../data/spamassassin.csv")
