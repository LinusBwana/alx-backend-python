import psycopg2
import functools
import logging
from datetime import datetime  # <-- REQUIRED import

# Configure logging to display timestamp and SQL queries
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# Decorator to log SQL queries with timestamp
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the SQL query
        query = kwargs.get("query") if "query" in kwargs else (args[0] if args else None)
        if query:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.info(f"[{timestamp}] Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname="ALX_prodev",
        user="postgres",
        password="Blue@1996",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Example usage
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM user_data;")
    for user in users:
        print(user)