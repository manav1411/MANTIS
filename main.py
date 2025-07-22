from app.getmail import loading_credentials, connect_to_gmail_imap
from app.parse_mail import n_recent_emails, tasks_from_emails, events_from_emails
from app.database import database_init, insert_task, view_all_tasks, insert_event, view_all_events
from pprint import pprint

def main():
    email, password = loading_credentials('../email_creds.yaml')
    mail = connect_to_gmail_imap(email, password)

    # performs operations on 2 most recent emails
    MIME_emails = n_recent_emails(mail, 2)
    email_tasks = tasks_from_emails(MIME_emails)
    email_events = events_from_emails(MIME_emails)

    # print("email tasks:")
    # pprint(email_tasks)
    # print("email events:")
    # pprint(email_events)

    database_init()
    # insert tasks and events into db
    for task in email_tasks:
        insert_task(task)
    for event in email_events:
        insert_event(event)
    
    print("tasks in db:")
    pprint(view_all_tasks())
    print("events in db:")
    pprint(view_all_events())

if __name__ == "__main__":
    main()