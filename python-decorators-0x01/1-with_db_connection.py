import psycopg2
import functools

# Decorator to manage PostgreSQL database connections
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            # Open PostgreSQL connection
            conn = psycopg2.connect(
                dbname="ALX_prodev",   
                user="postgres",               
                password="Blue@1996",
                host="localhost",
                port="5432"
            )
            # Pass the connection as the first argument to the wrapped function
            return func(conn, *args, **kwargs)
        finally:
            # Ensure the connection is always closed
            if conn:
                conn.close()
                print("Database connection closed.")
    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data WHERE user_id = %s", (user_id,))
    return cursor.fetchone()


# Example usage
if __name__ == "__main__":
    user = get_user_by_id(user_id="00324946-9a80-446b-90af-2b43bc1ade37")
    print("Final Output:", user)