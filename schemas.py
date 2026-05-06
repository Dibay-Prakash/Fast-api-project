from pydantic import BaseModel, ConfigDict

class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    publication_year: int
    language: str

    model_config = ConfigDict(from_attributes=True)


class BookSchema(BookBase):
    pass