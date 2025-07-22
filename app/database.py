import sqlite3
import logging
from app.types import Task, Event

DB_PATH = "./MANTIS.db"

# Attempts to create and initialise the sqlite database.
# returns True if successful, returns False if not
def database_init():
    
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        # creates tasks and events db tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY,
                sender TEXT,
                task TEXT,
                created_at TEXT,
                is_done BOOLEAN DEFAULT 0,
                UNIQUE(sender, task, created_at)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events(
                id INTEGER PRIMARY KEY,
                sender TEXT,
                event TEXT,
                created_at TEXT,
                remind_at TEXT,
                UNIQUE(sender, event, created_at)
            )
        ''')

        connection.commit()
        connection.close()

        return True
    except Exception as e:
        logging.error(f"error occured when initialising db: {e}")
        return False



# Attempts to insert a given task object into the tasks table in the db
def insert_task(task: Task):
    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO tasks(sender, task, created_at)
                VALUES (?, ?, ?)
            ''', (
                task.from_,
                task.task,
                task.created_at.isoformat()
            ))
        return True
    except sqlite3.IntegrityError:
        logging.warning("Duplicate task skipped.")
        return False
    except Exception as e:
        logging.error(f"couldn't insert task because: {e}")
        return False


# returns a list of all tasks in the database
def view_all_tasks():
    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()

            cursor.execute('''
                SELECT * FROM tasks
            ''')
            result = cursor.fetchall()
        return result
    except Exception as e:
        logging.error(f"couldn't read tasks because: {e}")
        return []

# marks task of given id as complete (1) or incomplete (0)
def mark_task(task_id, status):
    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                UPDATE tasks
                SET is_done = ?
                WHERE id = ?
            ''', (status, task_id))

            cursor.execute('select changes()')
            changes = cursor.fetchone()[0]

            if changes == 0:
                logging.warning(f"No task updated with ID {task_id}. It may not exist.")
                return False
            else:
                connection.commit()
                return True
    except Exception as e:
        logging.error(f"couldn't mark task because: {e}")
        return False


# Attempts to insert a given event object into the events table in the db
def insert_event(event: Event):
    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO events(sender, event, created_at, remind_at)
                VALUES (?, ?, ?, ?)
            ''', (
                event.from_,
                event.event,
                event.created_at.isoformat(),
                event.remind_at.isoformat()
            ))
        return True
    except sqlite3.IntegrityError:
        logging.warning("Duplicate event skipped.")
        return False
    except Exception as e:
        logging.error(f"couldn't insert event because: {e}")
        return False


# returns a list of all events in the database
def view_all_events():
    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                SELECT * FROM events
            ''')
            result = cursor.fetchall()
        return result
    except Exception as e:
        logging.error(f"couldn't read events because: {e}")
        return []