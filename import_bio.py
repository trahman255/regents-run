import json
from core.database import SessionLocal
from sqlalchemy import text

def import_questions():
    db = SessionLocal()
    
    with open('biology_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    query = text("""
        INSERT INTO questions (course, topic, question, options, answer, image_url)
        VALUES (:course, :topic, :question, :options, :answer, :image_url)
    """)
    
    count = 0
    for item in data:
        img_path = item.get('image_url', '').strip()
        
        # Foolproof auto-formatting for images
        if img_path:
            # If it's a local Windows path, extract just the relative structure / filename
            if "images" in img_path:
                # Get everything from 'images' onwards and normalize slashes for the web
                relative_part = img_path.split("images")[-1].replace("\\", "/")
                img_url = f"https://regents-run-api.onrender.com/images{relative_part}"
            else:
                img_url = img_path
        else:
            img_url = ""

        db.execute(query, {
            "course": "Biology",
            "topic": item['topic'],
            "question": item['question'],
            "options": item['options'],
            "answer": str(item['answer']),
            "image_url": img_url
        })
        count += 1
        
    db.commit()
    db.close()
    print(f"Successfully imported {count} Biology questions with auto-formatted image URLs to Neon!")

if __name__ == "__main__":
    import_questions()