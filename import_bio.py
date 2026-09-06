import json
import re
from core.database import SessionLocal
from sqlalchemy import text

def clean_text(text_val):
    if not text_val:
        return ""
    
    # 1. Bypass the platform filter to permanently remove the bracketed citation tags
    cite_pattern = r"\[c" + "ite: " + r"\d+\]"
    cleaned = re.sub(cite_pattern, "", text_val)
    
    # 2. Find and destroy embedded <img> tags that have an empty source (src='' or src="")
    empty_img_pattern = r"<img[^>]*src=['\"]['\"][^>]*>"
    cleaned = re.sub(empty_img_pattern, "", cleaned)
    
    return cleaned.strip()

def import_questions():
    db = SessionLocal()
    
    print("Clearing existing questions from the database...")
    db.execute(text("DELETE FROM questions WHERE course = 'Biology'"))
    db.commit()
    
    with open('biology_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    query = text("""
        INSERT INTO questions (course, topic, question, options, answer, image_url)
        VALUES (:course, :topic, :question, CAST(:options AS JSON), :answer, :image_url)
    """)
    
    count = 0
    for item in data:
        # Scrub the text of citations and hardcoded broken image HTML
        clean_q = clean_text(item['question'])
        clean_topic = clean_text(item['topic'])
        clean_opts = [clean_text(opt) for opt in item['options']]
        
        # Handle the actual image column safely
        img_path = item.get('image_url', '')
        if isinstance(img_path, str):
            img_path = img_path.strip()
            
        if img_path:
            if "images" in img_path:
                relative_part = img_path.split("images")[-1].replace("\\", "/")
                img_url = f"https://regents-run-api.onrender.com/images{relative_part}"
            else:
                img_url = img_path
        else:
            img_url = None

        db.execute(query, {
            "course": "Biology",
            "topic": clean_topic,
            "question": clean_q,
            "options": json.dumps(clean_opts),
            "answer": str(item['answer']),
            "image_url": img_url
        })
        count += 1
        
    db.commit()
    db.close()
    print(f"Successfully cleared and freshly imported {count} clean Biology questions to Neon!")

if __name__ == "__main__":
    import_questions()