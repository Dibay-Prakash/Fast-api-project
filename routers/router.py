from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Book
from schemas import BookSchema
from auth import get_current_user

router = APIRouter(
    prefix="/books",
    tags=["Books"],
    dependencies=[Depends(get_current_user)]
)