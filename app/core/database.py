from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

# 1. Create the Engine
# 'check_same_thread': False is specific to SQLite (it allows multiple threads)
engine = create_engine(
    settings.DATABASE_URL,
    connect_args = {"check_same_thread":False}
)

# 2. Create Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Modern SQLAlchemy 2.0 Base Class
class Base(DeclarativeBase):
    """
    All our database models will inherit from this class.
    It acts as a registry for our tables.
    """
    pass

# 4. Dependency Injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()