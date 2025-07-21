from getmail import loading_credentials, connect_to_gmail_imap
from parse_mail import n_recent_emails, tasks_from_emails, events_from_emails

from pprint import pprint

def main():
    email, password = loading_credentials('./email_creds.yaml')
    mail = connect_to_gmail_imap(email, password)

    # performs duties on 20 most recent emails
    MIME_emails = n_recent_emails(mail, 2)
    email_tasks = tasks_from_emails(MIME_emails)
    email_events = events_from_emails(MIME_emails)

    print("email tasks:")
    pprint(email_tasks)
    print("email events:")
    pprint(email_events)

if __name__ == "__main__":
    main()