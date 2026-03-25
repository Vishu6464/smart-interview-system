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

    try:
        # Only seed if no questions exist
        question_count = db.query(models.Question).count()

        if question_count == 0:

            df = pd.read_csv("Python Programming Questions Dataset.csv")

            for _, row in df.iterrows():

                question = models.Question(
                    domain="python",
                    difficulty=str(row.get("Difficulty", "Medium")).capitalize(),
                    question_text=str(row.get("Instruction")),
                    ideal_answer=str(row.get("Output"))
                )

                db.add(question)

            db.commit()
            print("Database seeded successfully.")

        else:
            print("Database already contains questions. Skipping seed.")

    except Exception as e:
        print("Error loading CSV:", e)

    finally:
        db.close()
