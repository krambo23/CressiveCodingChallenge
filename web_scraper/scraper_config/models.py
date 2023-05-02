from django.db import models


class Keywords(models.Model):
    keyword = models.CharField("Keywords to be Scraped", max_length=200, primary_key=True)

    class Meta:
        verbose_name = "Keyword"
        verbose_name_plural = "Keywords"


class ScraperStatus(models.Model):
    scraper_status = models.CharField("Scraper Status", max_length=200)
    scraper_last_ran = models.DateTimeField("Last Time the Scraper Was Started")

    class Meta:
        verbose_name = "Scraper Status"
        verbose_name_plural = "Scraper Status"


class ScrapedTable(models.Model):
    title = models.CharField("Title", max_length=200)
    description = models.CharField("Description", max_length=500)
    price = models.FloatField("Price")
    rating = models.FloatField("Rating")
    asin = models.CharField("ASIN", max_length=10)
    page_number = models.IntegerField("Page Number")
    search_result_position = models.IntegerField("Search Result Position")
    is_sponsored = models.BooleanField("Is Product Sponsored")
    keyword = models.ForeignKey(Keywords, on_delete=models.PROTECT)
    date_time_scraped = models.DateTimeField("Date and Time of Scraping", primary_key=True)
