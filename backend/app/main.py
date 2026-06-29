from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.api import auth, review

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Code Review Assistant",
    description="Multi-agent AI system for code review",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(review.router, prefix="/api/review", tags=["Review"])

@app.get("/")
def root():
    return {"message": "AI Code Review Assistant is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}