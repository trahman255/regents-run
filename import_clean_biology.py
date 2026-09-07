import json
from core.database import SessionLocal
from sqlalchemy import text

def import_clean_biology():
    db = SessionLocal()
    
    with open('clean_biology.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
            
    # Updated SQL to include the new image_urls and explanation columns
    query = text("""
        INSERT INTO questions (course, topic, context, question, options, answer, image_url, image_urls, explanation)
        VALUES (:course, :topic, :context, :question, CAST(:options AS JSON), :answer, :image_url, CAST(:image_urls AS JSON), :explanation)
    """)
    
    count = 0
    for item in data:
        options_json = json.dumps(item.get('options', []))
        
        # Safely handle the multiple images list
        img_urls = item.get('image_urls')
        image_urls_json = json.dumps(img_urls) if img_urls else None
        
        db.execute(query, {
            "course": item['course'],
            "topic": item['topic'],
            "context": item.get('context'),
            "question": item['question'],
            "options": options_json,
            "answer": item['answer'],
            "image_url": item.get('image_url'),
            "image_urls": image_urls_json,
            "explanation": item.get('explanation') # Added the explanation mapping
        })
        count += 1
        
    db.commit()
    db.close()
    print(f"Successfully imported {count} Biology questions with explanations!")

if __name__ == "__main__":
    import_clean_biology()