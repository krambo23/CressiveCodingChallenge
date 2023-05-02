# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from datetime import datetime

from itemadapter import ItemAdapter

from sqlalchemy import create_engine, Column, String, Float, Integer, Boolean, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class AmazonScraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        # Strip Whitespace
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != "description":
                value = adapter.get(field_name)
                if isinstance(value, str):
                    adapter[field_name] = value.strip()
                elif isinstance(value, tuple):
                    adapter[field_name] = value[0].strip()

        for field_name in field_names:
            value = adapter.get(field_name)
            if value is None:
                adapter[field_name] = ""

        # Convert "Price" to Float
        try:
            price = adapter.get("price")

            if price == "":
                price = -1

            price = price.replace("£", "")
            adapter["price"] = float(price)
        except:
            adapter["price"] = -1

        # Convert "Rating" to Float
        try:
            rating = adapter.get("rating").strip()

            if rating == "":
                rating = -1

            rating = rating.replace(" out of 5 stars", "")
            adapter["rating"] = float(rating)
        except:
            adapter["rating"] = -1

        return item


class SaveToDatabasePipeline:
    def __init__(self):
        db_directory = os.environ["SQLITE_PATH"]

        # SQLAlchemy
        self.engine = create_engine(f"sqlite:///{db_directory}", echo=True)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    class ScrapedTable(declarative_base()):
        __tablename__ = "scraper_config_scrapedtable"
        id = Column(Integer, primary_key=True)
        title = Column(String(200))
        description = Column(String(500))
        price = Column(Float)
        rating = Column(Float)
        asin = Column(String(10))
        page_number = Column(Integer)
        search_result_position = Column(Integer)
        is_sponsored = Column(Boolean)
        keyword = Column(String(200))
        date_time_scraped = Column(DateTime)

    def process_item(self, item, spider):
        date_time_scraped = datetime.fromisoformat(item["date_time_scraped"])
        self.session.add(self.ScrapedTable(
            title=item["title"],
            description=item["description"],
            price=item["price"],
            rating=item["rating"],
            asin=item["asin"],
            page_number=item["page_number"],
            search_result_position=item["search_result_position"],
            is_sponsored=item["is_sponsored"],
            keyword=item["keyword"],
            date_time_scraped=date_time_scraped
        ))

        self.session.commit()
        return item

    def close_spider(self, spider):
        self.session.close()
