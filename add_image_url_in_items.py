import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Item


URL = os.getenv("DATABASE_URL_PS", "postgresql+psycopg2://postgres@localhost/legadrop")

engine = create_engine(URL, echo=True)
url_image = "images/items/crystal.png"


def add_image_url():
    with Session(bind=engine, autoflush=True) as db:
        items = db.query(Item).all()

        for item in items:
            item.image = url_image

        db.commit()


add_image_url()
