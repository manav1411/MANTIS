import email
import re
from email.utils import parsedate_to_datetime
from datetime import datetime

# helper function - extracts just the body from a raw MIME email
def extract_email_body(MIME_email):
    if MIME_email.is_multipart():
        for part in MIME_email.walk():
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode(errors="ignore")
    else:
        return MIME_email.get_payload(decode=True).decode(errors="ignore")


# parses first emails from mail object to parsed email messages
# returns: list of n emails
def n_recent_emails(mail, n):
    mail.select('inbox')
    result, data = mail.search(None, "ALL")
    if result != "OK":
        return []
    
    email_ids = data[0].split()[-n:]
    emails = []

    for email_id in email_ids:
        result, data = mail.fetch(email_id, "(RFC822)")
        if result != "OK":
            continue
        raw_email = data[0][1]
        message = email.message_from_bytes(raw_email)
        emails.append(message)
    
    return emails





# given list of emails identifies and return list of tasks
def tasks_from_emails(MIME_emails):
    
    task_list = []
    for MIME_email in MIME_emails:
        email_subject = MIME_email["subject"] or ""
        email_body = extract_email_body(MIME_email)
        full_email_text = email_subject + "\n" + email_body

        tasks = re.findall(r"\[task\](.+)", full_email_text, flags=re.IGNORECASE)
        for task in tasks:
            task_list.append({
                "task": task.strip(),
                "created_at": parsedate_to_datetime(MIME_email["date"]),
                "from": MIME_email["from"]
            })

    return task_list


# given list of emails identifies and return list of events
def events_from_emails(MIME_emails):
    
    event_list = []
    for MIME_email in MIME_emails:
        email_subject = MIME_email["subject"] or ""
        email_body = extract_email_body(MIME_email)
        full_email_text = email_subject + "\n" + email_body

        events = re.findall(r"\[remind:(.+?)\]\s*(.+)", full_email_text, flags=re.IGNORECASE)
        for datetime_str, event in events:
            try:
                remind_at = datetime.strptime(datetime_str.strip(), "%Y-%m-%d %H:%M")
            except ValueError:
                continue
            
            event_list.append({
                "event": event.strip(),
                "remind_at": remind_at,
                "created_at": parsedate_to_datetime(MIME_email["date"]),
                "from": MIME_email["from"]
            })
            
    return event_list
