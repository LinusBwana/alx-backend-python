import psycopg2
import functools


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


# Decorator to manage transactions

def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  
            print("Transaction committed successfully.")
            return result
        except Exception as e:
            conn.rollback()
            print(f"Transaction rolled back due to error: {e}")
            raise
    return wrapper


# Example function using both decorators

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE user_data SET email = %s WHERE user_id = %s",
        (new_email, user_id)
    )
    print(f"Updated email for user_id {user_id} to {new_email}")


# Run Example

if __name__ == "__main__":
    update_user_email(
        user_id="00324946-9a80-446b-90af-2b43bc1ade37",
        new_email="Crawford_Cartwright@hotmail.com"
    )
