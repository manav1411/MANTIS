
# MANTIS
Mail Automated Notification & Task Integrated System


MANTIS is a self-hosted, lightweight, AI-free productivity assistant that helps you make sense of your inbox. 
<br>It can manage tasks and provide relevant reminders for events by parsing incoming emails.

## How to run
1. clone this repo, 
2. input you email/password into email_creds.yaml (make sure you've created an app password if using gmail)
3. run main.py in a terminal
4. From here, you'll be presented with an interactive shell - welcome to MANTIS :)

Type '?' to see the full command list.


## TODO list
1. CLI integration (mark_done function, delete function, use made function to list tasks <- all CLI)
2. Reminders - send notifications just before (maybe like a day) events to own email address (get notifs on phone like that), consider an automated regular 'fetch' instead of needing to run the program again every time you want updated task/events list
3. Understand natural language rather than '[task]' etc. 
4. consider replacing UNIQUE check with storing a hash and just checking 1 (can make hash the primary key too). hash = hash(sender + subject + created_at) in main.py -> performance too.
5. Testing (db, parser, etc) for different parts of the project.
6. look into SMTP -> alternative to IMAP. (also could use for sending reminders to self)
7. auto-run with `schedule` or `CRON`