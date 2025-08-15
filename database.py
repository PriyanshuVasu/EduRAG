import sqlite3

DB_NAME = "conversation_history.db"

def init_db():
    """Initializes the database and creates the table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Create the table only if it doesn't already exist.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversation_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        session_id TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def add_message_to_history(user_id, session_id, role, content):
    """Adds a message to the conversation history, including the user_id."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO conversation_history (user_id, session_id, role, content) VALUES (?, ?, ?, ?)",
        (user_id, session_id, role, content)
    )
    conn.commit()
    conn.close()

def get_user_history(user_id, limit=10):
    """Retrieves the last 'limit' messages for a given user_id across all their sessions."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content FROM conversation_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
        (user_id, limit)
    )
    # The results are fetched in descending order, so we reverse them to get the correct conversational order
    history = reversed(cursor.fetchall())
    conn.close()
    return [{"role": role, "content": content} for role, content in history]