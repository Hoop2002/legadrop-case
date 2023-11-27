from pydantic_core import Url
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Item


URL = "postgresql+psycopg2://lega_drop:hoophoop2002@localhost:5432/lega_drop_db"

engine = create_engine(URL, echo=True)
url_image = "images/items/crystal.png"

def add_image_url():
    with Session(bind=engine, autoflush=True) as db:

        items = db.query(Item).all()
        
        for item in items:
            item.image = url_image

        db.commit()
add_image_url()