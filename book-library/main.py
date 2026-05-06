from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base, Book
from schemas import BookSchema
from auth import verify_password, create_access_token, fake_user, get_current_user
from routers.router import router

app = FastAPI()


app.include_router(router)
# ---------------- AUTH ----------------

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = fake_user  # later replace with DB user

    # check username
    if form_data.username != user["username"]:
        raise HTTPException(status_code=400, detail="Invalid username")

    # check password
    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid password")

    # create token
    token = create_access_token(data={"sub": user["username"]})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# create tables
Base.metadata.create_all(bind=engine)

# ---------------- READ ----------------

@app.get("/all_books/", dependencies=[Depends(get_current_user)])
def read_all_books(db: Session = Depends(get_db)):
    return db.query(Book).all()


@app.get("/books_by_author/{author_name}", dependencies=[Depends(get_current_user)])
def read_books_by_author(author_name: str, db: Session = Depends(get_db)):
    return db.query(Book).filter(Book.author == author_name).all()


@app.get("/books_by_language/{language}", dependencies=[Depends(get_current_user)])
def read_books_by_language(language: str, db: Session = Depends(get_db)):
    return db.query(Book).filter(Book.language == language).all()


# ---------------- CREATE ----------------

@app.post("/add_book/", dependencies=[Depends(get_current_user)])
def add_book(book: BookSchema, db: Session = Depends(get_db)):

    db_book = Book(
        title=book.title,
        author=book.author,
        genre=book.genre,
        publication_year=book.publication_year,
        language=book.language
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return {"message": "Book added successfully", "book": db_book}


# ---------------- UPDATE ----------------

@app.put("/update_book/{book_id}", dependencies=[Depends(get_current_user)])
def update_book(book_id: int, book: BookSchema, db: Session = Depends(get_db)):

    db_book = db.query(Book).filter(Book.id == book_id).first()

    if not db_book:
        return {"message": "Book not found"}

    db_book.title = book.title
    db_book.author = book.author
    db_book.genre = book.genre
    db_book.publication_year = book.publication_year
    db_book.language = book.language

    db.commit()
    db.refresh(db_book)

    return {"message": "Book updated successfully", "book": db_book}


# ---------------- DELETE ----------------

@app.delete("/delete_book/{book_id}", dependencies=[Depends(get_current_user)])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db.query(Book).filter(Book.id == book_id).delete()
    db.commit()
    return {"message": "Book deleted successfully"}


@app.delete("/delete_book/author/{author_name}", dependencies=[Depends(get_current_user)])
def delete_book_by_author(author_name: str, db: Session = Depends(get_db)):
    db.query(Book).filter(Book.author == author_name).delete()
    db.commit()
    return {"message": "Books deleted successfully"}




