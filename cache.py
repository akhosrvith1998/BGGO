import time
from collections import defaultdict
from logger import logger

INLINE_QUERY_CACHE = defaultdict(dict)
CACHE_TTL = 10  # seconds

def get_cached_inline_query(sender_id, query):
    """
    Retrieves cached inline query results if available and not expired.

    Args:
        sender_id (str): The ID of the user who sent the inline query.
        query (str): The text of the inline query.

    Returns:
        list: The cached results if available and not expired, otherwise None.
    """
    if sender_id in INLINE_QUERY_CACHE and query in INLINE_QUERY_CACHE[sender_id]:
        cache_entry = INLINE_QUERY_CACHE[sender_id][query]
        if time.time() - cache_entry["timestamp"] < CACHE_TTL:
            logger.debug(f"Serving cached inline query for {sender_id}: {query}")
            return cache_entry["results"]
    return None

def set_cached_inline_query(sender_id, query, results):
    """
    Caches the results of an inline query.

    Args:
        sender_id (str): The ID of the user who sent the inline query.
        query (str): The text of the inline query.
        results (list): The results of the inline query.
    """
    INLINE_QUERY_CACHE[sender_id][query] = {
        "results": results,
        "timestamp": time.time()
    }
    logger.debug(f"Cached inline query for {sender_id}: {query}")
  
