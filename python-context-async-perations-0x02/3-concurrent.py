import asyncio
import asyncpg
import aiosqlite

DB_CONFIG = {
    "user": "postgres",
    "password": "Blue@1996",
    "database": "ALX_prodev",
    "host": "localhost",
    "port": 5432,
}

# Function to log access
async def log_access():
    conn = await asyncpg.connect(**DB_CONFIG)
    try:
        # Using execute() for a statement that doesn't return rows
        await conn.execute("INSERT INTO logs(message) VALUES('Fetched users')")
        print("Log entry added using execute()")
    finally:
        await conn.close()

# Fetch all users
async def async_fetch_users():
    conn = await asyncpg.connect(**DB_CONFIG)
    try:
        results = await conn.fetch("SELECT * FROM users")
        print("All Users:", results)
        return results
    finally:
        await conn.close()

# Fetch users older than 40
async def async_fetch_older_users():
    conn = await asyncpg.connect(**DB_CONFIG)
    try:
        results = await conn.fetch("SELECT * FROM users WHERE age > 40")
        print("Users older than 40:", results)
        return results
    finally:
        await conn.close()

# Run both queries concurrently
async def fetch_concurrently():
    # First, log the query execution using execute()
    await log_access()

    # Run both queries concurrently
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("\nFinal combined results:")
    print(results)

# Entry point
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())