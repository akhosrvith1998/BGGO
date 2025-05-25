import sqlite3
import json
from logger import logger

DATABASE = "history.db"
history = {}

def init_database():
    """
    Initializes the SQLite database, creating the history table if it doesn't exist.
    """
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                sender_id TEXT,
                receiver_id TEXT,
                display_name TEXT,
                first_name TEXT,
                profile_photo_url TEXT,
                PRIMARY KEY (sender_id, receiver_id)
            )
        """)
        conn.commit()
        logger.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Error initializing database: {e}")
    finally:
        if conn:
            conn.close()

def load_history():
    """
    Loads the chat history from the SQLite database into the 'history' dictionary.
    """
    global history
    history = {}
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT sender_id, receiver_id, display_name, first_name, profile_photo_url FROM history")
        rows = cursor.fetchall()
        for row in rows:
            sender_id, receiver_id, display_name, first_name, profile_photo_url = row
            if sender_id not in history:
                history[sender_id] = []
            history[sender_id].append({
                "receiver_id": receiver_id,
                "display_name": display_name,
                "first_name": first_name,
                "profile_photo_url": profile_photo_url,
                "curious_users": set()  # Compatibility with previous code
            })
        logger.info("History loaded successfully from the database.")
    except sqlite3.Error as e:
        logger.error(f"Error loading history from database: {e}")
    finally:
        if conn:
            conn.close()
    return history

def save_history(sender_id, receiver):
    """
    Saves a new receiver to the chat history in the SQLite database.

    Args:
        sender_id (str): The ID of the user who sent the message.
        receiver (dict): A dictionary containing the receiver's information.
    """
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO history (sender_id, receiver_id, display_name, first_name, profile_photo_url)
            VALUES (?, ?, ?, ?, ?)
        """, (sender_id, receiver["receiver_id"], receiver["display_name"], receiver["first_name"], receiver["profile_photo_url"]))
        conn.commit()
        logger.info(f"Saved history for sender {sender_id} and receiver {receiver['receiver_id']} to the database.")
    except sqlite3.Error as e:
        logger.error(f"Error saving history to database: {e}")
    finally:
        if conn:
            conn.close()

    # Update in-memory history
    if sender_id not in history:
        history[sender_id] = []
    existing = next((r for r in history[sender_id] if r["receiver_id"] == receiver["receiver_id"]), None)
    if not existing:
        history[sender_id].append(receiver)
        history[sender_id] = history[sender_id][-10:]  # Limit to 10 receivers

# Initialize database and load history on startup
init_database()
load_history()
