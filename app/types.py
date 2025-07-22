from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    from_: str
    task: str
    created_at: datetime

@dataclass
class Event:
    from_: str
    event: str
    created_at: datetime
    remind_at: datetime