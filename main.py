from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, SessionLocal
import models
import pandas as pd

from routers import question_router, attempt_router, analytics_router

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(question_router.router)
app.include_router(attempt_router.router)
app.include_router(analytics_router.router)


@app.get("/")
def health_check():
    return {"status": "Smart Interview Backend is Running"}


@app.on_event("startup")
def seed_data():

    db = SessionLocal()

    # Seed only if empty
    if db.query(models.Question).count() == 0:

        try:
            df = pd.read_csv("Python Programming Questions Dataset.csv")

            print("CSV loaded. Columns found:", df.columns)

            for _, row in df.iterrows():

                question_text = row.get("Instruction")
                ideal_answer = row.get("Output")

                # If dataset contains difficulty column
                difficulty = row.get("Difficulty", "Medium")

                if question_text and ideal_answer:

                    question = models.Question(
                        domain="python",
                        difficulty=str(difficulty).capitalize(),
                        question_text=str(question_text),
                        ideal_answer=str(ideal_answer)
                    )

                    db.add(question)

            db.commit()
            print("Questions loaded successfully from CSV.")

        except Exception as e:
            print("Error loading CSV:", e)

    db.close()
