from core.database import SessionLocal
from sqlalchemy import text

def add_column():
    db = SessionLocal()
    try:
        db.execute(text("ALTER TABLE questions ADD COLUMN IF NOT EXISTS explanation TEXT;"))
        db.commit()
        print("Successfully added the 'explanation' column!")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_column()