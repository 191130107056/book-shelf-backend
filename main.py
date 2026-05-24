from fastapi import FastAPI, HTTPException
from app.core.config import settings
from app.core.database import engine, Base
from app.models.book import Book # Import models to register them
from app.routers import books, stats
from app.core.exception import business_exception_handler
from app.core.middlerware import RateLimitMiddleware
from fastapi.middleware.cors import CORSMiddleware

# This line tells SQLAlchemy to create all tables defined in models
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = settings.PROJECT_NAME,
    description="A professional Bookshelf API built with FastAPI and SQLAlchemy",
    version="1.0.0"
)

# Register custom error handler for a professional look
app.add_exception_handler(HTTPException, business_exception_handler)

# Register rate limit middleware
app.add_middleware(RateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Register Routers
app.include_router(books.router)
app.include_router(stats.router)

# @app.get("/health", tags=["Health"])
# def health_check():
#     return {
#         "status": "online",
#          "project": settings.PROJECT_NAME,
#          "database" : "connected" if engine else "error"
#          }

if __name__ == "__main__":
    import uvicorn
    # This allows you to run the app by just running: python main.py (instead of uvicorn main:app --reload || uvicorn main:app --host 0.0.0.0 --port 8000 --reload)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
        
