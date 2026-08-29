from sqlalchemy import create_engine, Column, Integer, String, Text, JSON
from sqlalchemy.orm import declarative_base

# 1. Your Neon connection URL
NEON_URL = "postgresql://neondb_owner:npg_KcY52rksWyPv@ep-delicate-smoke-ayh5fdj7-pooler.c-5.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# 2. Database Engine & Base
engine = create_engine(NEON_URL)
Base = declarative_base()

# 3. Questions Table Model
class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True)
    course = Column(String, index=True)
    topic = Column(String, index=True)
    question = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)
    answer = Column(String, nullable=False)
    explanation = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)

# 4. Create Tables
if __name__ == "__main__":
    print("Connecting to Neon and creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Success! 'questions' table created in Neon PostgreSQL.")