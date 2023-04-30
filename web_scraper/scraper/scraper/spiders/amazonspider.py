import scrapy
from urllib.parse import quote, urljoin
from datetime import datetime
import os


class AmazonSpider(scrapy.Spider):
    name = "amazonspider"
    allowed_domains = ["amazon.co.uk"]
    start_urls = ["http://amazon.co.uk/"]
    BASE_URL = "https://www.amazon.co.uk/"

    def start_requests(self):
        # TODO : Fetch Keyword List From Database
        keyword_list = ["ipad"]
        for keyword in keyword_list:
            amazon_url = urljoin(self.BASE_URL, f"s?k={quote(keyword)}&page=1")
