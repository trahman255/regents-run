from core.database import SessionLocal
from sqlalchemy import text

def delete_aug25_biology():
    db = SessionLocal()
    
    # Deletes only the rows where the course is Biology
    db.execute(text("DELETE FROM questions WHERE course = 'Biology';"))
    db.commit()
    db.close()
    
    print("All Biology questions have been completely deleted from the database.")

if __name__ == "__main__":
    delete_aug25_biology()