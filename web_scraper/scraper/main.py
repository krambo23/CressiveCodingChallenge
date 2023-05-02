import asyncio

from scrapy import signals
from scrapy.crawler import Crawler, CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.reactor import install_reactor

from scraper.settings import DOWNLOADER_MIDDLEWARES, ITEM_PIPELINES, SCRAPEOPS_API_KEY, \
    SCRAPEOPS_PROXY_SETTINGS, SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT, SCRAPEOPS_FAKE_USER_AGENT_ENABLED, \
    SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT, SCRAPEOPS_FAKE_BROWSER_HEADERS_ENABLED, SCRAPEOPS_NUM_RESULTS, \
    SCRAPEOPS_PROXY_ENABLED
from scraper.spiders.amazonspider import AmazonSpider


def handle_engine_started():
    print("=" * 12)
    print("handle_engine_started")
    print("Engine Started!")
    print("=" * 12)


def handle_engine_stopped():
    print("=" * 12)
    print("handle_engine_stopped")
    print("Engine Stopped!")
    print("=" * 12)


def handle_item_scraped(item, response, spider):
    print("=" * 12)
    print("handle_item_scraped")
    print(f"Item Scraped: {item}")
    print(f"Response: {response.status} @ {response.url})")
    print(f"Spider: {spider.name}")
    print("=" * 12)


def handle_item_dropped(item, response, exception, spider):
    print("=" * 12)
    print("handle_item_dropped")
    print(f"Item Dropped: {item}")
    print(f"Response: {response.status} @ {response.url})")
    print(f"Exception: {exception}")
    print(f"Spider: {spider.name}")
    print("=" * 12)


def handle_item_error(item, response, spider, failure):
    print("=" * 12)
    print("handle_item_error")
    print(f"Item Dropped: {item}")
    print(f"Response: {response.status} @ {response.url})")
    print(f"Failure: {failure}")
    print(f"Spider: {spider.name}")
    print("=" * 12)


def handle_spider_opened(spider):
    print("=" * 12)
    print("handle_spider_opened")
    print(f"Spider {spider.name} Started!")
    print("=" * 12)


def handle_spider_closed(spider, reason):
    print("=" * 12)
    print("handle_spider_closed")
    print(f"Spider {spider.name} Closed!")
    print(f"Reason: {reason}")
    print("=" * 12)


def handle_spider_idle(spider):
    print("=" * 12)
    print("handle_spider_idle")
    print(f"Spider {spider.name} Is Idle!")
    print("=" * 12)


def handle_spider_error(failure, response, spider):
    print("=" * 12)
    print("handle_spider_error")
    print(f"Spider {spider.name} Errored!")
    print(f"Failure: {failure}")
    print(f"Response: {response.status} @ {response.url})")
    print("=" * 12)


def main():
    install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

    settings = get_project_settings()
    settings = {
        **settings,
        "DOWNLOADER_MIDDLEWARES": DOWNLOADER_MIDDLEWARES,
        "ITEM_PIPELINES": ITEM_PIPELINES,
        "SCRAPEOPS_API_KEY": SCRAPEOPS_API_KEY,
        "SCRAPEOPS_PROXY_SETTINGS": SCRAPEOPS_PROXY_SETTINGS,
        "SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT": SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT,
        "SCRAPEOPS_FAKE_USER_AGENT_ENABLED": SCRAPEOPS_FAKE_USER_AGENT_ENABLED,
        "SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT": SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT,
        "SCRAPEOPS_FAKE_BROWSER_HEADERS_ENABLED": SCRAPEOPS_FAKE_BROWSER_HEADERS_ENABLED,
        "SCRAPEOPS_NUM_RESULTS": SCRAPEOPS_NUM_RESULTS,
        "SCRAPEOPS_PROXY_ENABLED": SCRAPEOPS_PROXY_ENABLED
    }

    process = CrawlerProcess(settings=settings)

    amazon_crawler = Crawler(AmazonSpider, settings=settings)

    amazon_crawler.signals.connect(handle_engine_started, signal=signals.engine_started)
    amazon_crawler.signals.connect(handle_engine_stopped, signal=signals.engine_stopped)
    amazon_crawler.signals.connect(handle_item_scraped, signal=signals.item_scraped)
    amazon_crawler.signals.connect(handle_item_dropped, signal=signals.item_dropped)
    amazon_crawler.signals.connect(handle_item_error, signal=signals.item_error)
    amazon_crawler.signals.connect(handle_spider_opened, signal=signals.spider_opened)
    amazon_crawler.signals.connect(handle_spider_closed, signal=signals.spider_closed)
    amazon_crawler.signals.connect(handle_spider_idle, signal=signals.spider_idle)
    amazon_crawler.signals.connect(handle_spider_error, signal=signals.spider_error)

    process.crawl(amazon_crawler)

    process.start()


if __name__ == '__main__':
    main()
