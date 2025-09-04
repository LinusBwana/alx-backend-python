import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import connect

def connect_to_prodev():
    """
    Connect to the ALX_prodev PostgreSQL database.
    """
    return connect(
        dbname="ALX_prodev",
        user="postgres",   
        password="Blue@1996", 
        host="localhost",
        port="5432"
    )

def stream_users():
    """
    Generator function to fetch rows one by one from the user_data table.
    Uses yield to return each row without loading the whole table into memory.
    """
    conn = connect_to_prodev()  # create the connection inside the function
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM user_data;")
        while True:
            row = cur.fetchone()
            if row is None:
                break
            yield row
    conn.close()

if __name__ == "__main__":
    print("Streaming users one by one...\n")
    for user in stream_users():
        print(user)