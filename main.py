from app.getmail import loading_credentials, connect_to_gmail_imap
from app.parse_mail import n_recent_emails, intellegent_parse_email
from app.database import (
    database_init, insert_task, mark_task, view_all_tasks,
    insert_event, view_all_events, clear_database
)
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.traceback import install

install()  # Better tracebacks in rich

CREDENTIALS_PATH = './email_creds.yaml'
console = Console()

ASCII_ART = r"""[green]
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
[/green]"""

def print_welcome():
    console.print(Panel.fit(ASCII_ART, title="[bold green]MANTIS - Your Email Assistant[/bold green]", border_style="white"))

def fetch_command(args):
    if len(args) < 1 or len(args) > 2:
        console.print("[red]Invalid command. Usage: fetch [n] (optional: 'unread')[/red]")
        return

    unread = False
    try:
        n = int(args[0])
    except ValueError:
        console.print("[red]Invalid number. Usage: fetch [n] (optional: 'unread')[/red]")
        return

    if len(args) == 2:
        if args[1].lower() == "unread":
            unread = True
        else:
            console.print("[red]Invalid second argument. Did you mean 'unread'?[/red]")
            return

    try:
        email, password = loading_credentials(CREDENTIALS_PATH)
        mail = connect_to_gmail_imap(email, password)
        MIME_emails = n_recent_emails(mail, n, unread)
    except Exception as e:
        console.print(f"[red]Error fetching emails: {e}[/red]")
        return

    email_tasks, email_events = intellegent_parse_email(MIME_emails)

    task_count, event_count = len(email_tasks), len(email_events)
    for task in email_tasks:
        inserted_task = insert_task(task)
        if not inserted_task:
            task_count -= 1
    for event in email_events:
        insert_success = insert_event(event)
        if not insert_success:
            event_count -= 1

    console.print(f"[green]Fetched and inserted {task_count} task(s) and {event_count} event(s) from {n} {'unread ' if unread else ''}emails.[/green]")

def list_command(args):
    if len(args) != 1:
        console.print("[red]Invalid command. Usage: list [tasks/events][/red]")
        return
    
    if args[0] in ("tasks", "t"):
        tasks = view_all_tasks()
        if not tasks:
            console.print("[yellow]No tasks found.[/yellow]")
            return

        table = Table(title="Tasks", box=box.ROUNDED)
        table.add_column("ID", justify="right")
        table.add_column("Description", overflow="fold")
        table.add_column("Status", justify="center")

        for task in tasks:
            status = "[green]Done[/green]" if task[4] else "[yellow]Pending[/yellow]"
            table.add_row(str(task[0]), task[2], status)
        console.print(table)

    elif args[0] in ("events", "e"):
        events = view_all_events()
        if not events:
            console.print("[yellow]No events found.[/yellow]")
            return

        table = Table(title="Events", box=box.ROUNDED)
        table.add_column("ID", justify="right")
        table.add_column("Description", overflow="fold")
        table.add_column("Date", justify="center")

        for event in events:
            date = event[4] if event[4] else "N/A"
            table.add_row(str(event[0]), event[2], date)
        console.print(table)
    else:
        console.print("[red]Invalid command. Usage: list [tasks/events][/red]")

def task_command(args):
    if len(args) != 2:
        console.print("[red]Invalid command. Usage: task [task number] [done/undone][/red]")
        return
    try:
        task_id = int(args[0])
        status_str = args[1]
        if status_str not in ["done", "undone"]:
            console.print("[red]Invalid task status. Use 'done' or 'undone'.[/red]")
            return
    except ValueError:
        console.print("[red]Invalid task number. Usage: task [task number] [done/undone][/red]")
        return
    task_status = 1 if status_str == "done" else 0
    if mark_task(task_id, task_status):
        console.print(f"[green]Task {task_id} marked as {status_str}.[/green]")
    else:
        console.print(f"[red]Task {task_id} not found.[/red]")

def clear_command(args):
    result = clear_database()
    if result:
        console.print("[bold red]Database has been cleared![/bold red]")

def print_help():
    help_text = """
[bold cyan]Commands:[/bold cyan]

• fetch [n[n]] (optional: 'unread')    : Fetch and parse the n most recent (optionally unread) emails.

• list tasks                        : List all tasks with their status (done/undone).

• list events                       : List all events with their dates.

• task [task_id[task_id]] [done|undone[done|undone]]      : Mark the specified task as done or undone.

• clear                             : Clear the database of all tasks and events.

• quit                              : Exit the program.

• ?                                 : Show this help message.
"""
    console.print(Panel.fit(help_text, title="Help", border_style="cyan"))

def interactive_shell():
    print_welcome()
    console.print("Type [bold green]'?'[/bold green] to see the full commands list.\n")

    COMMANDS = {
        "fetch": fetch_command,
        "f": fetch_command,
        "list": list_command,
        "l": list_command,
        "task": task_command,
        "t": task_command,
        "clear": clear_command,
        "quit": lambda args: exit_program(),
        "q": lambda args: exit_program(),
        "?": lambda args: print_help(),
    }

    def exit_program():
        console.print("[bold green]Goodbye![/bold green]")
        raise SystemExit()

    while True:
        try:
            user_command = Prompt.ask("[bold cyan]>[/bold cyan]").strip().lower()
        except KeyboardInterrupt:
            console.print("\n[bold green]Goodbye![/bold green]")
            break

        if not user_command:
            continue

        parts = user_command.split()
        command = parts[0]
        args = parts[1:]

        func = COMMANDS.get(command, None)
        if func:
            func(args)
        else:
            console.print("[red]Unknown command. Type '?' for help.[/red]")

if __name__ == "__main__":
    database_init()
    interactive_shell()
