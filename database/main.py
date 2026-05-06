from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel

from database import get_db

app = FastAPI()


class StudentUpdate(BaseModel):
    name: str
    age: int

@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM student"))
    
    students = []
    for row in result:
        students.append(dict(row._mapping))
    
    return students



@app.put("/students/{id}")
def update_student(id: int, payload: StudentUpdate, db: Session = Depends(get_db)):
    result = db.execute(
        text("UPDATE student SET name = :name, age = :age WHERE id = :id"),
        {"name": payload.name, "age": payload.age, "id": id},
    )
    db.commit()

    if not (result.rowcount and result.rowcount > 0):
        raise HTTPException(status_code=404, detail="Student not found")

    return {"message": "Student updated successfully", "id": id}





@app.post("/students")
def create_student(id: int, name: str , age:int, db: Session = Depends(get_db)):
    try:
        result = db.execute(
            text("INSERT INTO student (id, name, age) VALUES (:id, :name, :age)"),
            {"id": id, "name": name, "age": age},
        )
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"Student with id {id} already exists")

    if result.rowcount and result.rowcount > 0:
        return {"message": "Student created successfully"}

    return {"message": "Failed to create student"}







@app.delete("/students/{id}")
def delete_student(id: int, db: Session = Depends(get_db)):
    result = db.execute(
        text("DELETE FROM student WHERE id = :id"),
        {"id": id},
    )
    db.commit()

    if result.rowcount and result.rowcount > 0:
        return {"message": "Student deleted successfully"}

    return {"message": "Student not found"}