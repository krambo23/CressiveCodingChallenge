import scrapy
from urllib.parse import quote, urljoin
from datetime import datetime
import os


class AmazonSpider(scrapy.Spider):
    name = "amazonspider"
    allowed_domains = ["amazon.co.uk"]
    start_urls = ["http://amazon.co.uk/"]
    base_url = "https://www.amazon.co.uk/"

    def start_requests(self):
        # TODO : Fetch Keyword List From Database
        keyword_list = ["ipad"]
        for keyword in keyword_list:
            amazon_url = urljoin(self.base_url, f"s?k={quote(keyword)}&page=1")
            yield scrapy.Request(url=amazon_url, callback=self.parse_search,
                                 meta={"keyword": keyword, "page": 1})

    def parse_search(self, response):
        keyword = response.meta["keyword"]
        page = response.meta["page"]
        output = list()

        # region Sponsor Type 1
        # Get Sponsor Type 1 Elements
        sponsor_type_1 = response.css('[data-index="0"]').css('::attr(data-asin)').getall()

        # Filter Empty Values
        sponsor_type_1 = list(filter(None, sponsor_type_1))

        for element in sponsor_type_1:
            output.append({
                "title": None,
                "description": None,
                "price": None,
                "rating": None,
                "asin": element,
                "page_number": page,
                "search_result_position": 0,
                "is_sponsored": True,
                "keyword": keyword,
                "date_time_scraped": datetime.utcnow().isoformat(),
            })

        # endregion

        # region Sponsor Type 2
        number_sponsored_type_2 = 0
        prev_search_result_position = 0
        # Get All ASINs in Order - Element Must Have A "data-index" Value And A "data-asin" Value
        for node in response.css('[data-index]'):
            if node.css('[data-asin]'):
                if node.css('.a-row.a-spacing-micro'):
                    if node.css('.puis-sponsored-label-text'):
                        asin = node.css('.a-popover-preload ::attr(id)').get()
                        asin = asin.replace("a-popover-sp-info-popover-", "")
                        index = node.css("::attr(data-index)").get()
                        output.append({
                            "title": None,
                            "description": None,
                            "price": None,
                            "rating": None,
                            "asin": asin,
                            "page_number": page,
                            "search_result_position": index,
                            "is_sponsored": True,
                            "keyword": keyword,
                            "date_time_scraped": datetime.utcnow().isoformat(),
                        })
                        number_sponsored_type_2 += 1
                        prev_search_result_position = int(index)
        # endregion

        # region Organic
        data_asins = response.css('[data-index]::attr(data-asin)').getall()

        # Filter Empty Values
        data_asins = list(filter(None, data_asins))

        # Remove Sponsor Type 2 from Organic
        data_asins = data_asins[number_sponsored_type_2:]
        for index, asin in enumerate(data_asins):
            output.append({
                "title": None,
                "description": None,
                "price": None,
                "rating": None,
                "asin": asin,
                "page_number": page,
                "search_result_position": prev_search_result_position + 1 + int(index),
                "is_sponsored": False,
                "keyword": keyword,
                "date_time_scraped": datetime.utcnow().isoformat(),
            })

        # endregion

        if page == 1:
            number_of_pages = int(response.css("span.s-pagination-item.s-pagination-disabled ::text").getall()[1].strip())

            # if number_of_pages >= 2:
            #     for page_number in range(2, (number_of_pages + 1)):
            #         amazon_search_url = urljoin(self.base_url, f"s?k={quote(keyword)}&page={page_number}")
            #         yield scrapy.Request(url=amazon_search_url, callback=self.parse_search,
            #                              meta={"keyword": keyword, "page": page_number})

        for element in output:
            yield {
                "title": element["title"],
                "description": element["description"],
                "price": element["price"],
                "rating": element["rating"],
                "asin": element["asin"],
                "page_number": element["page_number"],
                "search_result_position": element["search_result_position"],
                "is_sponsored": element["is_sponsored"],
                "keyword": element["keyword"],
                "date_time_scraped": element["date_time_scraped"],
            }
