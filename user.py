from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    username: str
    password: str  # This should be hashed in production
    created_at: datetime = datetime.now()

# In-memory user storage for demonstration
# In production, this should use a proper database
users = {}

def create_user(username: str, password: str) -> bool:
    if username in users:
        return False
    users[username] = User(username=username, password=password)
    return True

def verify_user(username: str, password: str) -> bool:
    if username not in users:
        return False
    return users[username].password == password
