import psycopg2
import functools

# Global cache dictionary

query_cache = {}


# Decorator to handle DB connection

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



# Cache decorator

def cache_query(func):
    """
    Caches query results to avoid redundant database calls.
    Cache key is the SQL query string passed to the function.
    """
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        # Check if query result is already cached
        if query in query_cache:
            print(f"[CACHE HIT] Returning cached result for query: {query}")
            return query_cache[query]

        print(f"[CACHE MISS] Executing query and caching result: {query}")
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result  # Store in cache
        return result
    return wrapper


# Example function using cache

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# Run Example
if __name__ == "__main__":
    # First call will hit the database
    users = fetch_users_with_cache(query="SELECT * FROM user_data")
    print("First call result:", users)

    print("\n--- Calling again with same query ---\n")

    # Second call will use the cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM user_data")
    print("Second call result:", users_again)
