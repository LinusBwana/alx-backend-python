import psycopg2
from psycopg2.extras import RealDictCursor

# Function to connect to the database
def connect_to_prodev():
    """
    Connect to the ALX_prodev PostgreSQL database.
    """
    return psycopg2.connect(
        dbname="ALX_prodev",
        user="postgres",
        password="Blue@1996",
        host="localhost",
        port="5432"
    )

# REQUIRED function: exact signature
def paginate_users(page_size, offset):
    """
    Fetch a single page of users using LIMIT and OFFSET.
    """
    conn = connect_to_prodev()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM user_data LIMIT %s OFFSET %s;", (page_size, offset))
        rows = cur.fetchall()
    conn.close()
    return rows

# Lazy pagination generator
def lazy_paginate(page_size):
    """
    Lazily fetch pages of users one at a time using the paginate_users function.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:  # Stop when no data left
            break
        yield page
        offset += page_size  # Move to next page

# Example usage
if __name__ == "__main__":
    print("Lazy pagination demo...\n")

    for page in lazy_paginate(5):  # page_size = 5
        print("\n--- Page ---")
        for user in page:
            print(user)