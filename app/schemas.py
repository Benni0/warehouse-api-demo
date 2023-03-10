from pydantic import BaseModel


class Article(BaseModel):
    article_number: int
    article_name: str
    items_available: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
