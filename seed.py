from app.core.database import Base, engine, SessionLocal
from app.models.book import Book, BookStatus
from datetime import datetime, timedelta

def seed_db():
    print("Starting Database Seeding...")
    # 1. Clear existing data to ensure a fresh start
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        books = [
            # --- COMPLETED BOOKS (With Ratings & Timestamps) ---   
            Book(
                title="The Great Gatsby", author="F. Scott Fitzgerald", genre="Fiction",
                total_pages=180, published_year=1925, isbn="9780743273565",
                status=BookStatus.completed, rating=5.0, review="A masterpiece of American literature.",
                started_at=datetime.utcnow() - timedelta(days=30),
                finished_at=datetime.utcnow() - timedelta(days=25)
            ),
            Book(
                title="Atomic Habits", author="James Clear", genre="Self-Help",
                total_pages=320, published_year=2018, isbn="9780735211292",
                status=BookStatus.completed, rating=5.0, review="Life-changing advice.",
                started_at=datetime.utcnow() - timedelta(days=10),
                finished_at=datetime.utcnow() - timedelta(days=2)
            ),

            # --- READING BOOKS (In Progress) ---
            Book(
                title="Dune", author="Frank Herbert", genre="Sci-Fi",
                total_pages=612, published_year=1965, isbn="9780441172719",
                status=BookStatus.reading, started_at=datetime.utcnow() - timedelta(days=5)
            ),
            Book(
                title="Project Hail Mary", author="Andy Weir", genre="Sci-Fi",
                total_pages=476, published_year=2021, isbn="9780593135204",
                status=BookStatus.reading, started_at=datetime.utcnow() - timedelta(days=1)
            ),

            # --- TO READ BOOKS (Backlog) ---
            Book(
                title="The Hobbit", author="J.R.R. Tolkien", genre="Fantasy",
                total_pages=310, published_year=1937, isbn="9780547928227",
                status=BookStatus.to_read
            ),
            Book(
                title="Clean Code", author="Robert C. Martin", genre="Technology",
                total_pages=464, published_year=2008, isbn="9780132350884",
                status=BookStatus.to_read
            ),
            Book(
                title="Deep Work", author="Cal Newport", genre="Self-Help",
                total_pages=304, published_year=2016, isbn="9781455586691",
                status=BookStatus.to_read
            ),
            Book(
                title="The Silent Patient", author="Alex Michaelides", genre="Thriller",
                total_pages=336, published_year=2019, isbn="9781250301697",
                status=BookStatus.to_read
            ),
            Book(
                title="Educated", author="Tara Westover", genre="Memoir",
                total_pages=352, published_year=2018, isbn="9780399590504",
                status=BookStatus.to_read
            ),
            Book(
                title="The Alchemist", author="Paulo Coelho", genre="Fiction",
                total_pages=208, published_year=1988, isbn="9780062315007",
                status=BookStatus.to_read
            ),
            Book(
                title="Sapiens", author="Yuval Noah Harari", genre="History",
                total_pages=512, published_year=2011, isbn="9780062316097",
                status=BookStatus.to_read
            ),
            Book(
                title="The Shining", author="Stephen King", genre="Horror",
                total_pages=447, published_year=1977, isbn="9780307743657",
                status=BookStatus.to_read
            ),
            Book(
                title="Foundation", author="Isaac Asimov", genre="Sci-Fi",
                total_pages=255, published_year=1951, isbn="9780553293357",
                status=BookStatus.to_read
            ),
            Book(
                title="Brave New World", author="Aldous Huxley", genre="Dystopian",
                total_pages=268, published_year=1932, isbn="9780060850524",
                status=BookStatus.to_read
            )
        ]

        db.add_all(books)
        db.commit()
        print(f"Successfully seeded {len(books)} books!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
    #run with python seed.py command

