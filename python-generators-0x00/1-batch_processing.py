import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import connect

# ---------------------------
# 1. Connect to the database
# ---------------------------
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

# ------------------------------------------------------
# 2. Generator to fetch rows in batches using fetchmany
# ------------------------------------------------------
def stream_users_in_batches(batch_size):
    """
    Generator that fetches users in batches from the database.
    Yields a list of rows, each batch containing up to batch_size rows.
    """
    conn = connect_to_prodev()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM user_data;")
        while True:
            batch = cur.fetchmany(batch_size)  # fetch up to batch_size rows
            if not batch:  # stop when no more rows
                break
            yield batch
    conn.close()

# -------------------------------------------------------
# 3. Process batches to filter users over the age of 25
# -------------------------------------------------------
def batch_processing(batch_size):
    """
    Processes each batch and filters users whose age > 25.
    """
    for batch in stream_users_in_batches(batch_size):  # loop 1
        filtered_batch = [user for user in batch if user['age'] > 25]  # loop 2 (inside comprehension)
        yield filtered_batch  # yield the filtered batch

# -------------------------------------------------------
# 4. Run the batch processing
# -------------------------------------------------------
if __name__ == "__main__":
    batch_size = 10  # process 10 rows at a time

    print(f"Processing users in batches of {batch_size}...\n")

    for processed_batch in batch_processing(batch_size):  # loop 3
        print("Filtered Batch:")
        for user in processed_batch:
            print(user)
        print("-" * 40)