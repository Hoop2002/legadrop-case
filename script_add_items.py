from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Item, ItemCompound, RarityCategory
import requests
import json

URL = "postgresql+psycopg2://lega_drop:hoophoop2002@localhost:5432/lega_drop_db"

engine = create_engine(URL, echo=True)


with open("cost.json") as file_costs, open("items.json") as file_items:
    costs = json.load(file_costs)
    items = json.load(file_items)

    with Session(bind=engine, autoflush=True) as session:
        COMMON = (
            session.query(RarityCategory)
            .filter(RarityCategory.ext_id == "COMMON")
            .first()
        )
        UNCOMMON = (
            session.query(RarityCategory)
            .filter(RarityCategory.ext_id == "UNCOMMON")
            .first()
        )
        RARE = (
            session.query(RarityCategory)
            .filter(RarityCategory.ext_id == "RARE")
            .first()
        )
        MYTHICAL = (
            session.query(RarityCategory)
            .filter(RarityCategory.ext_id == "MYTHICAL")
            .first()
        )
        LEGENDARY = (
            session.query(RarityCategory)
            .filter(RarityCategory.ext_id == "LEGENDARY")
            .first()
        )
        ULTRALEGENDARY = (
            session.query(RarityCategory)
            .filter(RarityCategory.ext_id == "ULTRALEGENDARY")
            .first()
        )

        for item_name, elements in items.items():
            new_item = Item(name=item_name)
            cost = float(0.0)

            session.add(new_item)
            session.commit()

            for element_name, quantities in elements.items():
                for quantity in quantities:
                    for name, price in costs.items():
                        if name == element_name:
                            cost += price * quantity

                        new_compound = ItemCompound(
                            name=element_name,
                            quantity=quantity,
                            item_id=new_item.item_id,
                        )
                        session.add(new_compound)
            cost = round(cost, 2)

            if cost < 5.0:
                new_item.rarity_category = COMMON
            if cost > 5.0 and cost < 14.0:
                new_item.rarity_category = UNCOMMON
            if cost > 14.0 and cost < 27.0:
                new_item.rarity_category = RARE
            if cost > 27.0 and cost < 45.0:
                new_item.rarity_category = MYTHICAL
            if cost > 45.0 and cost < 65.0:
                new_item.rarity_category = LEGENDARY
            if cost > 65.0:
                new_item.rarity_category = ULTRALEGENDARY

            new_item.cost = cost

        session.commit()
