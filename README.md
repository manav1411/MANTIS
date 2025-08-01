# MANTIS  
Mail Automated Notification & Task Integrated System

---

MANTIS is a self-hosted, lightweight, AI-free productivity assistant that helps you make sense of your inbox.  
It parses incoming emails to automatically extract and manage tasks and reminders, allowing you to keep organized without leaving your terminal.

---

## Features

- Connects securely to your email inbox (Gmail IMAP supported)
- Parses specially formatted emails to extract **tasks** and **events**
- Stores extracted items in a local SQLite database
- Interactive terminal shell to:
  - Fetch and parse emails on demand
  - View, manage, and update tasks and events
  - Mark tasks as done/undone
  - Clear all data when needed
- Uses natural language processing with SpaCy for intelligent parsing
- Clean, user-friendly CLI powered by Rich for beautiful tables and prompts

---

## Screenshots

<img width="392" height="332" alt="Screenshot 2025-08-01 at 8 58 54 pm" src="https://github.com/user-attachments/assets/4091e300-487b-496b-93d7-06c9da20b389" />

*Welcome screen with ASCII art and prompt*

<img width="745" height="307" alt="Screenshot 2025-08-01 at 8 59 08 pm" src="https://github.com/user-attachments/assets/aee25359-023e-4dd5-b508-503db6730804" />


*List of all commands via the help menu*

<img width="1023" height="624" alt="Screenshot 2025-08-01 at 9 04 20 pm" src="https://github.com/user-attachments/assets/813b1cb1-0c33-4d4a-bbc8-c3d03099d6ef" />


*Fetching emails, viewing tasks from those emails, marking tasks as done*

---

## Getting Started

### Prerequisites

- Python 3.8+
- Gmail account with **App Password** enabled (enable [here](https://myaccount.google.com/apppasswords))
- type your email credentials in the `email_creds.yaml` (see below)

### Installation
1. Clone the repository
`git clone git@github.com:manav1411/MANTIS.git`
`cd mantis`
2. Install dependencies
`pip install -r requirements.txt`
3. fill in `email_creds.yaml` in the project root with your email and app password credentials.


## Usage

Run the main program.

You can type '?' to see the list of commands.

The idea is to fetch your emails, which gets stored in the database, and then directly be able to view tasks and events through MANTIS.

### example workflow
1. Fetch the 10 most recent unread emails and parse tasks/events: `fetch 10 unread`
2. View your current tasks: `list tasks`
3. Mark a task as done: `task 3 done`
4. Exit the program `quit`


---

## Design and Implementation Highlights

- **Modular codebase:**  
  - `getmail.py` handles secure email fetching via IMAP  
  - `parse_mail.py` processes and extracts meaningful task and event data using SpaCy NLP  
  - `database.py` manages persistent storage with SQLite, including schema for tasks and events  
  - `main.py` runs the interactive shell and orchestrates the commands

- **Rich-powered CLI:** Uses the `rich` library for colorful, formatted terminal output including tables and prompts.

- **Configurable and secure:** Credentials are loaded from an external YAML file to keep secrets out of code.

---

## Roadmap & Future Ideas

- Test support for other email providers via IMAP (and consider SMTP) 
- Implement automated scheduled fetching (e.g., cron jobs)  
- Support for reminder notifications via desktop or emailing one's self  
- More advanced NLP parsing for free-form emails  
- Refine precision of task differentiation  

---

### Thank you for reading this far - here's an Easter egg!

You are able to use short hand for most commands (e.g. 'q' instead of 'quit', or 'l t' instead of 'list tasks')
