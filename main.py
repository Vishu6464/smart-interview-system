from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models

from routers import question_router, attempt_router, analytics_router
from seed_all_questions import seed_data


# Create tables
models.Base.metadata.create_all(bind=engine)

# Initialize app
app = FastAPI()


# Startup event (ONLY ONE — SAFE)
@app.on_event("startup")
def startup_event():
    try:
        print("🚀 Running DB seed on startup...")
        seed_data()
        print("✅ Startup completed successfully")
    except Exception as e:
        print("❌ Startup error:", e)


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # fine for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers (NO CHANGE)
app.include_router(question_router.router)
app.include_router(attempt_router.router)
app.include_router(analytics_router.router)


# Health check
@app.get("/")
def health_check():
    return {"status": "Smart Interview Backend is Running"}