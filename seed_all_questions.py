import pandas as pd
import re
import os
from database import SessionLocal
import models


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def parse_markdown_questions(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    questions = []

    pattern = r"\* \[Q(\d+): (.*?)\]\("
    matches = re.findall(pattern, content)

    for q_number, question_text in matches:
        q_number = int(q_number)

        if q_number in [1,2,3,4,6,7,8,10,11,12]:
            category = "coding"
        else:
            category = "mock"

        if q_number in [1,2,5,10]:
            difficulty = "Easy"
        elif q_number in [3,4,7,9,11,14]:
            difficulty = "Medium"
        else:
            difficulty = "Hard"

        questions.append({
            "category": category,
            "domain": "python",
            "difficulty": difficulty,
            "question_text": question_text.strip(),
            "ideal_answer": "Refer to markdown source for full answer."
        })

    return questions


def seed_data():
    db = SessionLocal()

    try:
        print("🚀 Seeding started...")

        if db.query(models.Question).count() > 0:
            print("Questions already exist. Skipping seed.")
            return

        # ✅ FIXED PATHS
        csv_path = os.path.join(BASE_DIR, "questions.csv")
        md_path = os.path.join(BASE_DIR, "questions.md")

        print("CSV path:", csv_path)
        print("MD path:", md_path)

        # Load CSV
        df = pd.read_csv(csv_path)

        for _, row in df.iterrows():
            db.add(models.Question(
                category="coding",
                domain="python",
                difficulty=str(row.get("Difficulty", "Medium")).capitalize(),
                question_text=str(row.get("Instruction")),
                ideal_answer=str(row.get("Output"))
            ))

        # Load Markdown
        md_questions = parse_markdown_questions(md_path)

        for q in md_questions:
            db.add(models.Question(**q))

        # ✅ FALLBACK (VERY IMPORTANT FOR DEMO)
        if db.query(models.Question).count() == 0:
            print("⚠️ No data found, inserting fallback question")
            db.add(models.Question(
                category="coding",
                domain="python",
                difficulty="Easy",
                question_text="Write a function to add two numbers",
                ideal_answer="def add(a,b): return a+b"
            ))

        db.commit()
        print("✅ Seeding completed successfully")

    except Exception as e:
        print("❌ Error seeding:", e)

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()