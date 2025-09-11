import psycopg2

class ExecuteQuery:
    def __init__(self, dbname, user, password, host, port, query, params=None):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.query = query
        self.params = params if params else ()
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        # Open PostgreSQL connection
        self.conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.cursor = self.conn.cursor()
        print("Database connection opened.")

        # Execute query
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results  # Return the fetched rows directly

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
            print(f"Transaction rolled back due to error: {exc_val}")
        else:
            self.conn.commit()
            print("Transaction committed successfully.")

        self.cursor.close()
        self.conn.close()
        print("Database connection closed.")


# Example usage
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > %s"
    params = (25,)

    with ExecuteQuery(
        dbname="ALX_prodev",
        user="postgres",
        password="Blue@1996",
        host="localhost",
        port="5432",
        query=query,
        params=params
    ) as results:
        print("Query Results:")
        for row in results:
            print(row)