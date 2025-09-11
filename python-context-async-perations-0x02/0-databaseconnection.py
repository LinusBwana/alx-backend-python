import psycopg2


class DatabaseConnection:
    """
    Custom context manager to handle PostgreSQL DB connection.
    Automatically opens and closes the connection.
    """

    def __init__(self, dbname, user, password, host="localhost", port="5432"):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cursor = None

    def __enter__(self):
        # Open database connection
        self.conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.cursor = self.conn.cursor()
        print("Database connection opened.")
        return self.cursor  # Return the cursor to be used in the `with` block

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Commit changes if no exceptions, rollback if there was an error
        if self.conn:
            if exc_type is None:
                self.conn.commit()
                print("Transaction committed.")
            else:
                self.conn.rollback()
                print(f"Transaction rolled back due to error: {exc_val}")

            # Close the cursor and connection
            self.cursor.close()
            self.conn.close()
            print("Database connection closed.")
        return False  # Propagate exceptions if they occur


# Example Usage
if __name__ == "__main__":
    with DatabaseConnection(
        dbname="ALX_prodev",
        user="postgres",
        password="Blue@1996",
        host="localhost",
        port="5432"
    ) as cursor:
        cursor.execute("SELECT * FROM users") 
        results = cursor.fetchall()
        print("Query Results:")
        for row in results:
            print(row)