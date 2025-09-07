# seed.py
from app.models.database import SessionLocal, engine
from app.models import models

# Sample questions data
sample_questions = [
    {
        "topic": "Geography",
        "question_text": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome"],
        "correct_answer": "Paris"
    },
    {
        "topic": "Science",
        "question_text": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Venus"],
        "correct_answer": "Mars"
    },
    # ... Add topics to the other questions ...
    {
        "topic": "Java",
        "question_text": "Which keyword is used to define a constant in Java?",
        "options": ["const", "static", "final", "let"],
        "correct_answer": "final"
    },
    {
        "topic": "Java",
        "question_text": "What is the default value of a boolean variable in Java?",
        "options": ["true", "false", "0", "null"],
        "correct_answer": "false"
    }
]
def seed_db():
    # Create tables
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Check if questions already exist
    if db.query(models.Question).count() == 0:
        print("Seeding database with sample questions...")
        for q_data in sample_questions:
            new_question = models.Question(**q_data)
            db.add(new_question)
        db.commit()
        print("Seeding complete.")
    else:
        print("Database already seeded.")
        
    db.close()

if __name__ == "__main__":
    seed_db()