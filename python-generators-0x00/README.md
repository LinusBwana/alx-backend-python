# Python PostgreSQL Generator Example

This project demonstrates how to use **Python generators** to stream rows from a PostgreSQL database. It includes scripts to set up a database, create tables, insert sample data, and stream data row by row.

## Features

- Connects to a PostgreSQL database
- Creates a database (`ALX_prodev`) if it does not exist
- Creates a table `user_data` with the following fields:
  - `user_id` (UUID, primary key)
  - `name` (VARCHAR, not null)
  - `email` (VARCHAR, not null)
  - `age` (DECIMAL, not null)
- Populates the table with sample data
- Streams rows using a Python generator function for memory-efficient processing

## Requirements

- Python 3.8+
- `psycopg2` library
- PostgreSQL server

Install dependencies:

```bash
pip install psycopg2-binary
```

## Usage

### Set up the database and table:

```bash
python seed.py
```

This script will:
- Connect to PostgreSQL
- Create the ALX_prodev database if it doesn't exist
- Create the user_data table
- Insert sample data

### Stream data using a generator:

```python
from seed import stream_users, connect_to_prodev

conn = connect_to_prodev()
for user in stream_users(conn):
    print(user)
```

This will print each row one by one without loading the entire table into memory.

## Sample Data

The database is populated with realistic sample users:

```python
sample_data = [
    {"name": "Alice", "email": "alice@example.com", "age": 25},
    {"name": "Bob", "email": "bob@example.com", "age": 30},
    {"name": "Charlie", "email": "charlie@example.com", "age": 22},
    {"name": "Diana", "email": "diana@example.com", "age": 28},
    # ... more users
]
```

*(Full list of users is included in seed.py.)*