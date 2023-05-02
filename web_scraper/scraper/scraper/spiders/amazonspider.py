import scrapy
from urllib.parse import quote, urljoin
from datetime import datetime
import os

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class AmazonSpider(scrapy.Spider):
    name = "amazonspider"
    allowed_domains = ["amazon.co.uk"]
    start_urls = ["http://amazon.co.uk/"]
    base_url = "https://www.amazon.co.uk/"

    def start_requests(self):
        db_directory = os.environ["SQLITE_PATH"]

        # SQLAlchemy
        engine = create_engine(f"sqlite:///{db_directory}", echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        Base = declarative_base()

        class Keywords(Base):
            __tablename__ = "scraper_config_keywords"
            id = Column(Integer, primary_key=True)
            keyword = Column(String(200))

        keywords = session.query(Keywords).all()

        for keyword in keywords:
            keyword = str(keyword.keyword)
            amazon_url = urljoin(self.base_url, f"s?k={quote(keyword)}&page=1")
            yield scrapy.Request(url=amazon_url, callback=self.parse_search, dont_filter=True,
                                 meta={"keyword": keyword, "page": 1})
        session.close()

    def parse_search(self, response):
        keyword = response.meta["keyword"]
        page = response.meta["page"]

        # region Sponsor Type 1
        # Get Sponsor Type 1 Elements
        sponsor_type_1 = response.css('[data-index="0"]').css('::attr(data-asin)').getall()

        # Filter Empty Values
        sponsor_type_1 = list(filter(None, sponsor_type_1))

        for element in sponsor_type_1:
            product_url = urljoin(f"{self.base_url}/dp/", element)
            yield scrapy.Request(url=product_url, callback=self.parse_product_details, dont_filter=True,
                                 meta={
                                     "asin": element,
                                     "page_number": page,
                                     "search_result_position": 0,
                                     "is_sponsored": True,
                                     "keyword": keyword,
                                     "date_time_scraped": datetime.utcnow().isoformat()
                                 })
        # endregion

        # region Sponsor Type 2 and Organic
        # Get All ASINs in Order - Element Must Have A "data-index" Value And A "data-asin" Value

        # Check for 'data-index'
        for node in response.css('[data-index]'):

            title = ""
            price = ""
            rating = ""
            is_sponsored = True
            date_time_scraped = datetime.utcnow().isoformat()

            # Check for 'data-asin'
            if node.css('[data-asin]'):
                asin = node.css('[data-asin] ::attr(data-asin)').get().strip()
                index = node.css('[data-index] ::attr(data-index)').get().strip()

                if asin != "" and index != "":

                    # Grab Result
                    if node.css('.a-section.a-spacing-small.a-spacing-top-small'):

                        # Get Title
                        title = node.css('.a-size-mini.a-spacing-none.a-color-base.s-line-clamp-2 ::text').get()

                        # Get Price
                        price = node.css('.a-price ::text').get()

                        # Get Ratings
                        if node.css('.a-row.a-size-small'):
                            rating = node.css('.a-icon-alt ::text').get()

                        # Check if Sponsored
                        if node.css('.a-row.a-spacing-micro'):
                            if node.css('.puis-sponsored-label-text'):
                                is_sponsored = True
                        else:
                            is_sponsored = False

                        # Get Description
                        product_url = urljoin(f"{self.base_url}/dp/", asin)
                        yield scrapy.Request(url=product_url, callback=self.parse_product_details, dont_filter=True,
                                             meta={
                                                 "title": title,
                                                 "price": price,
                                                 "rating": rating,
                                                 "asin": asin,
                                                 "page_number": page,
                                                 "search_result_position": index,
                                                 "is_sponsored": is_sponsored,
                                                 "keyword": keyword,
                                                 "date_time_scraped": date_time_scraped
                                             })

        # endregion

        if page == 1:
            number_of_pages = int(response.css("span.s-pagination-item.s-pagination-disabled ::text").getall()[1].strip())

            if number_of_pages >= 2:
                for page_number in range(2, (number_of_pages + 1)):
                    amazon_search_url = urljoin(self.base_url, f"s?k={quote(keyword)}&page={page_number}")
                    yield scrapy.Request(url=amazon_search_url, callback=self.parse_search,
                                         meta={"keyword": keyword, "page": page_number})

    def parse_product_details(self, response):
        description = response.css("#feature-bullets li ::text").getall()
        description = "\n".join([bullet.strip().strip() for bullet in description])
        # region Handle Sponsored Type 1 and Issues Caused By Amazon Limiting Scraping (E503)
        # Title
        try:
            title = response.meta["title"]
        except:
            title = response.css("#productTitle::text").get()

        # Price
        try:
            price = response.meta["price"]
        except:
            price = response.css('.a-price span[aria-hidden="true"] ::text').get()
            if not price:
                price = response.css(".a-price .a-offscreen ::text").get()

        # Rating
        try:
            rating = response.meta["rating"]
        except:
            rating = response.css("i[data-hook=average-star-rating] ::text").get()

        # endregion

        yield {
            "title": title,
            "description": description,
            "price": price,
            "rating": rating,
            "asin": response.meta["asin"],
            "page_number": response.meta["page_number"],
            "search_result_position": response.meta["search_result_position"],
            "is_sponsored": response.meta["is_sponsored"],
            "keyword": response.meta["keyword"],
            "date_time_scraped": datetime.utcnow().isoformat(),
        }
