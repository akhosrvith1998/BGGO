import requests
from datetime import datetime, timezone, timedelta
import json
from constants import BOT_TOKEN, BASE_URL
from logger import logger

IRST_OFFSET = timedelta(hours=3, minutes=30)
PROFILE_PHOTO_CACHE = {}  # Cache for profile photos

def escape_markdown(text):
    """Escapes MarkdownV2 special characters in a string."""
    escape_chars = '_*[]()~`>#+-=|{}.!'
    return ''.join(['\\' + char if char in escape_chars else char for char in text])

def get_irst_time(timestamp):
    """Converts a timestamp to IRST (Iran Standard Time)."""
    utc_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    irst_time = utc_time + IRST_OFFSET
    return irst_time.strftime("%H:%M")

def get_user_profile_photo(user_id):
    """Retrieves the file_id of the user's profile photo from Telegram."""
    if user_id in PROFILE_PHOTO_CACHE:
        logger.debug(f"Serving cached profile photo for user {user_id}")
        return PROFILE_PHOTO_CACHE[user_id]

    url = BASE_URL + "getUserProfilePhotos"
    params = {"user_id": user_id, "limit": 1}
    try:
        resp = requests.get(url, params=params).json()
        if resp.get("ok") and resp["result"]["total_count"] > 0:
            photo = resp["result"]["photos"][0][0]["file_id"]
            PROFILE_PHOTO_CACHE[user_id] = photo
            logger.debug(f"Cached profile photo for user {user_id}")
            return photo
        PROFILE_PHOTO_CACHE[user_id] = None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching profile photo for user {user_id}: {e}")
        PROFILE_PHOTO_CACHE[user_id] = None
    return None

def answer_inline_query(inline_query_id, results):
    """Sends the results of an inline query back to Telegram."""
    url = BASE_URL + "answerInlineQuery"
    data = {
        "inline_query_id": inline_query_id,
        "results": json.dumps(results),
        "cache_time": 0,
        "is_personal": True
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        logger.info(f"Answered inline query {inline_query_id}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error answering inline query {inline_query_id}: {e}")

def answer_callback_query(callback_query_id, text, show_alert=False):
    """Sends an answer to a callback query."""
    url = BASE_URL + "answerCallbackQuery"
    data = {
        "callback_query_id": callback_query_id,
        "text": text,
        "show_alert": show_alert
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        logger.info(f"Answered callback query {callback_query_id}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error answering callback query {callback_query_id}: {e}")

def edit_message_text(chat_id=None, message_id=None, inline_message_id=None, text=None, reply_markup=None):
    """Edits the text of a message."""
    url = BASE_URL + "editMessageText"
    data = {
        "text": text,
        "parse_mode": "MarkdownV2",
        "reply_markup": json.dumps(reply_markup) if reply_markup else None
    }
    if chat_id and message_id:
        data["chat_id"] = chat_id
        data["message_id"] = message_id
    elif inline_message_id:
        data["inline_message_id"] = inline_message_id
    else:
        raise ValueError("Either (chat_id and message_id) or inline_message_id must be provided.")
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        logger.info(f"Edited message text in chat {chat_id or inline_message_id}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error editing message text in chat {chat_id or inline_message_id}: {e}")

def format_block_code(whisper_data):
    """Formats the whisper data into a block code."""
    receiver_display_name = whisper_data['receiver_display_name']
    view_times = whisper_data.get("receiver_views", [])
    view_count = len(view_times)
    view_time_str = get_irst_time(view_times[-1]) if view_times else "هنوز دیده نشده"
    code_content = f"{escape_markdown(receiver_display_name)} {view_count} | {view_time_str}\n___"
    code_content += "\n" + ("\n".join([escape_markdown(user) for user in whisper_data["curious_users"]]) if whisper_data["curious_users"] else "Nothing")
    return code_content
