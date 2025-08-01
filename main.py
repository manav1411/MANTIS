from app.getmail import loading_credentials, connect_to_gmail_imap
from app.parse_mail import n_recent_emails, tasks_from_emails, events_from_emails, extract_email_body, intellegent_parse_email
from app.database import database_init, insert_task, mark_task, view_all_tasks, insert_event, view_all_events
from pprint import pprint

CREDENTIALS_PATH = './email_creds.yaml'

def interactive_shell():
    
    print("Hi, I am MANTIS! I will help make your email life easier.")
    print(r"""
⠀⣤⡀⠀⠀⠀⠀⠀⠀⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠘⢷⡄⠀⠀⠀⠀⢰⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠈⠻⠆⢀⣀⣀⣈⣁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣤⣈⠙⢿⣿⣿⣷⠘⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢹⣿⣿⡇⠘⣿⣿⣿⡆⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢀⣠⣄⡉⠛⠁⠼⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⡄⠀⠀⠀⠀⠀
⠀⣿⣿⡟⢁⠀⠀⠀⠀⠙⠛⠿⡆⠸⣦⠀⠀⠀⠀⠀⢀⠞⠋⣀⡤⡀⠀⠀⠀⠀
⠀⡿⠋⣀⠘⢷⣄⠀⠀⢹⡇⠀⠀⠀⠈⠆⠀⠀⠀⠀⣠⣴⣿⣿⢁⡇⠀⠀⠀⠀
⠀⠀⠀⢹⣷⡌⠻⣦⡀⠀⠙⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⡿⠁⢸⡇⢸⡆⠀⠀
⠀⠀⠀⠀⢿⣿⣆⠙⢿⣆⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⠟⠁⠀⣾⡇⢸⣿⡄⠀
⠀⠀⠀⠀⠈⢿⣿⣧⠈⢿⣷⡀⠀⠀⢀⣴⣿⣿⣿⡿⠃⠀⠀⢰⣿⡇⠘⠻⣷⠀
⠀⠀⠀⠀⠀⠀⠻⣿⣷⡀⠻⣿⠂⣠⣿⣿⣿⣿⠟⠀⠀⠀⠀⣼⣿⠃⠀⢀⣿⠀
⠀⠀⠀⠀⠀⠀⠀⠙⢿⣷⡄⠀⣴⣿⣿⣿⠟⠁⠀⠀⠀⠀⢀⣼⠋⠀⠀⠸⡇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠃⣸⣿⣿⠟⢁⡴⠂⠀⠀⠀⠴⠛⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠋⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    """)

    print("Type '?' to see the full commands list.\n")
    while True:
        user_command = input("> ").strip().lower()

        parts = user_command.split()
        if not parts:
            continue
        command = parts[0]
        args = parts[1:]


        if command == "quit" or command == "q":
            print("Goodbye!")
            break
        
        elif command == "fetch":
            if len(args) > 1:
                print("Invalid command. Usage: fetch [n]")
                continue
            try:
                n = int(args[0]) if len(args) == 1 else 5  # default = 5 most recent emails if no n specified.
            except ValueError:
                print("Invalid number. Usage: fetch [n]")
                continue

            # gets and parses emails into tasks and events
            try:
                email, password = loading_credentials(CREDENTIALS_PATH)
                mail = connect_to_gmail_imap(email, password)
                MIME_emails = n_recent_emails(mail, n)
            except Exception as e:
                print(f"Error fetching emails: {e}")
                continue
            email_tasks = tasks_from_emails(MIME_emails)
            email_events = events_from_emails(MIME_emails)

            # use NLP to detect more tasks and events
            for mime_email in MIME_emails:
                if not any(marker in extract_email_body(mime_email) for marker in ["[task]", "[remind:]"]):
                    nlp_tasks, nlp_events = intellegent_parse_email(mime_email)
                    email_tasks.extend(nlp_tasks)
                    email_events.extend(nlp_events)

            # insert tasks and events into db
            task_count, event_count = len(email_tasks), len(email_events)
            for task in email_tasks:
                inserted_task = insert_task(task)
                if not inserted_task:
                    task_count -= 1
            for event in email_events:
                insert_success = insert_event(event)
                if not insert_success:
                    event_count -= 1
            print(f"Fetched and inserted {task_count} task(s) and {event_count} event(s). From {n} emails.")
        
        elif command == "list":
            if len(args) != 1:
                print("Invalid command. Usage: list [tasks/events]")
                continue
            
            # lists all tasks
            if args[0] == "tasks":
                tasks = view_all_tasks()
                if not tasks:
                    print("No tasks found.")
                    continue
                for task in tasks:
                    status = "completed" if task[4] else "uncompleted"
                    print(f"{task[0]}. {task[2]} -> {status}")
            
            # lists all events
            elif args[0] == "events":
                events = view_all_events()
                if not events:
                    print("No events found.")
                    continue
                for event in events:
                    print(f"{event[0]}. {event[2]} on {event[4]}")
            else:
                print("Invalid command. Usage: list [tasks/events]")
                continue

        elif command == "task":
            if len(args) != 2:
                print("Invalid command. Usage: task [task number] [done/undone]")
                continue
            try:
                task_id = int(args[0])
                status_str = args[1]
                if status_str not in ["done", "undone"]:
                    print("Invalid task status. Usage: task [task number] [done/undone]")
                    continue
            except ValueError:
                print("Invalid task number. Usage: task [task number] [done/undone]")
                continue
            task_status = 1 if status_str == "done" else 0
            if mark_task(task_id, task_status):
                print(f"Task {task_id} marked as {status_str}.")
            else:
                print(f"Task {task_id} not found.")

        elif command == "?":
            print('''
    fetch [n] : Fetch and parse the n most recent emails (default: 5).
    Example: fetch 3

    list tasks : List all tasks with their status (done/undone).

    list events : List all events with their dates.

    task [task_id] [done|undone] : Mark the specified task as done or undone.
    Example : task 2 done

    quit : Exit the program.

    ? : Show this help message.
            ''')
        
        else:
            print("Unknown command. type '?' for help.")



if __name__ == "__main__":
    database_init()
    interactive_shell()