from sqlalchemy import Column, Integer, String
from .database import Base

class Article(Base):
    __tablename__ = "articles"
    article_number = Column(Integer, primary_key=True, unique=True, index=True, autoincrement=False)
    article_name = Column(String(60), index=True)
    items_available = Column(Integer)
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
