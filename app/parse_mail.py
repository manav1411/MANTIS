import email
import re
import spacy
from dateparser import parse as parse_date
from email.utils import parsedate_to_datetime
from datetime import datetime
from app.types import Task, Event

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
            task_object = Task(
                from_=MIME_email["from"],
                task=task.strip(),
                created_at=parsedate_to_datetime(MIME_email["date"])
            )
            task_list.append(task_object)

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
            
            event_object = Event(
                from_=MIME_email["from"],
                event=event.strip(),
                created_at=parsedate_to_datetime(MIME_email["date"]),
                remind_at=remind_at
            )
            event_list.append(event_object)


    return event_list


# uses an NLP library to parse AN email and returns likely tasks and events
def intellegent_parse_email(MIME_email):
    tasks, events = [], []

    # parse MIME to be NLP readable format
    email_subject = MIME_email["subject"] or ""
    email_body = extract_email_body(MIME_email)
    full_text = email_subject + email_body
    nlp = spacy.load("en_core_web_sm")
    document = nlp(full_text)

    for sent in document.sents:
        text = sent.text.strip()

        # 1: does it sound like a task? (verb root sentence, like 'buy')
        if sent.root.tag_ == "VB" or sent.root.tag_ == "VBJ":
            tasks.append(Task(
                from_=MIME_email["from"],
                task=text,
                created_at=parsedate_to_datetime(MIME_email["date"])
            ))

        # 2: does it sound like an event? (mentions date or time)
        for ent in sent.ents:
            if ent.label_ in ["DATE", "TIME"]:
                try:
                    parsed_datetime = parse_date(ent.text)
                    if parsed_datetime:
                        events.append(Event(
                            from_=MIME_email["from"],
                            event=text,
                            created_at=parsedate_to_datetime(MIME_email["date"]),
                            remind_at=parsed_datetime
                        ))
                    break
                except:
                    continue



    return tasks, events
