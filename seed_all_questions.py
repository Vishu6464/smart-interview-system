import pandas as pd
import re
from database import SessionLocal
import models
import re

def parse_markdown_questions(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    questions = []

    # Match lines like:
    # * [Q1: Question text](...)
    pattern = r"\* \[Q(\d+): (.*?)\]\("

    matches = re.findall(pattern, content)

    for q_number, question_text in matches:

        q_number = int(q_number)

        # Manual classification
        if q_number in [1,2,3,4,6,7,8,10,11,12]:
            category = "coding"
        else:
            category = "mock"

        # Manual difficulty mapping
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
        if db.query(models.Question).count() > 0:
            print("Questions already exist. Skipping seed.")
            return

        # Load CSV Coding Dataset
        df = pd.read_csv("Python Programming Questions Dataset.csv")

        for _, row in df.iterrows():
            question = models.Question(
                category="coding",
                domain="python",
                difficulty=str(row.get("Difficulty", "Medium")).capitalize(),
                question_text=str(row.get("Instruction")),
                ideal_answer=str(row.get("Output"))
            )
            db.add(question)

        # Load Markdown Dataset
        md_questions = parse_markdown_questions(
            "Python Interview Questions & Answers for Data Scientists.md"
        )

        for q in md_questions:
            db.add(models.Question(**q))

        db.commit()
        print("All datasets merged and seeded successfully.")

    except Exception as e:
        print("Error seeding:", e)

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
