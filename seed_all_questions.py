import pandas as pd
import re
from database import SessionLocal
import models


def parse_markdown_questions(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    questions = []

    # Split by question headers like ## Q1
    blocks = re.split(r"\n## Q\d+:", content)

    for block in blocks[1:]:
        lines = block.strip().split("\n")
        question_text = lines[0].strip()

        answer = "\n".join(lines[1:]).strip()

        # Decide category automatically
        coding_keywords = ["Write", "Implement", "function", "code"]
        if any(word.lower() in question_text.lower() for word in coding_keywords):
            category = "coding"
            difficulty = "Medium"
        else:
            category = "mock"
            difficulty = "Medium"

        questions.append({
            "category": category,
            "domain": "python",
            "difficulty": difficulty,
            "question_text": question_text,
            "ideal_answer": answer
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
