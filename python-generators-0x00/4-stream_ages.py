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

# Generator to stream user ages one by one
def stream_user_ages():
    """
    Generator that yields ages of users from the user_data table one by one.
    This avoids loading the entire dataset into memory.
    """
    conn = connect_to_prodev()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT age FROM user_data;")
        while True:
            row = cur.fetchone()
            if row is None:  # Stop when there are no more rows
                break
            yield row['age']
    conn.close()

# Function to compute average age using the generator
def compute_average_age():
    """
    Compute the average age of all users without loading
    the entire dataset into memory.
    """
    total_age = 0
    count = 0

    # First loop: Iterate through generator
    for age in stream_user_ages():
        total_age += age
        count += 1

    # Avoid division by zero
    if count == 0:
        print("No users found in the database.")
        return

    average_age = total_age / count
    print(f"Average age of users: {average_age:.2f}")

# Main execution
if __name__ == "__main__":
    compute_average_age()