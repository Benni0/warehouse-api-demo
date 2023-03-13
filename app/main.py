from . import schemas, models
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import get_db, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get('/initialize')
def init_db(db: Session = Depends(get_db)):
    articles = [
        models.Article(article_name="Piercing", article_number=10001, items_available=51),
        models.Article(article_name="Diamant Ring", article_number=10002, items_available=50),
        models.Article(article_name="Bonze Brille", article_number=10007, items_available=5),
    ]
    for article in articles:
        article_query = db.query(models.Article).filter(models.Article.article_number == article.article_number)
        db_article = article_query.one_or_none()
        if db_article:
            update_data = article.dict(exclude_unset=True)
            article_query.filter(models.Article.article_number == article.article_number).update(update_data, synchronize_session=False)
            db.commit()
        else:
            db.add(article)
            db.commit()


@app.get('/article', response_model=list[schemas.Article])
async def get_all_articles(db: Session = Depends(get_db)):
    articles = db.query(models.Article).all()
    return articles


@app.get('/article/{article_number}', response_model=schemas.Article)
def get_article_by_id(article_number: int, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.article_number == article_number).one_or_none()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No article with number {article_number} found")
    return article


@app.put('/article/{article_number}', responses={406: {"detail": "Item not available"}}, response_model=schemas.Article)
def order_article(article_number: int, db: Session = Depends(get_db)) -> schemas.Article:
    article_query = db.query(models.Article).filter(models.Article.article_number == article_number)
    article = article_query.one_or_none()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No article with number {article_number} found")

    if article.items_available < 1:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"Article not available")
    article.items_available = article.items_available - 1
    db.commit()
    db.refresh(article)
    return article


@app.post('/article', status_code=status.HTTP_201_CREATED)
def create_article(payload: schemas.Article, db: Session = Depends(get_db)) -> schemas.Article:
    article = models.Article(**payload.dict())
    article_query = db.query(models.Article).filter(models.Article.article_number == article.article_number)
    db_article = article_query.one_or_none()
    if db_article:
        update_data = payload.dict(exclude_unset=True)
        article_query.filter(models.Article.article_number == article.article_number).update(update_data, synchronize_session=False)
        db.commit()
        db.refresh(db_article)
        return db_article

    db.add(article)
    db.commit()
    db.refresh(article)
    return article
