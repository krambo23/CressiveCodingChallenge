import scrapy


class AmazonspiderSpider(scrapy.Spider):
    name = "amazonspider"
    allowed_domains = ["amazon.co.uk"]
    start_urls = ["http://amazon.co.uk/"]

    def parse(self, response):
        pass
