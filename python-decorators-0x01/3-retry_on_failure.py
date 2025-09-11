import psycopg2
import functools
import time


# Decorator: Handle DB connection

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = psycopg2.connect(
                dbname="ALX_prodev",  
                user="postgres",              
                password="Blue@1996",    
                host="localhost",
                port="5432"
            )
            return func(conn, *args, **kwargs)
        finally:
            if conn:
                conn.close()
                print("Database connection closed.")
    return wrapper


# Decorator: Retry on failure

def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except psycopg2.OperationalError as e:
                    attempt += 1
                    print(f"Attempt {attempt} failed with error: {e}")
                    if attempt >= retries:
                        print("Max retries reached. Raising exception.")
                        raise
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
        return wrapper
    return decorator


# Function with retry logic

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data")  # Use correct table name
    return cursor.fetchall()


# Run Example
if __name__ == "__main__":
    users = fetch_users_with_retry()
    print("Users:", users)