import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")
if not db_url:
    print("No DATABASE_URL found.")
    exit(1)

print(f"Connecting to {db_url}")
engine = create_engine(db_url)

try:
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE briefings RENAME COLUMN channel_id TO creator_id;"))
        conn.commit()
    print("Successfully renamed 'channel_id' to 'creator_id' in 'briefings' table.")
except Exception as e:
    print(f"Migration failed or already applied: {e}")
