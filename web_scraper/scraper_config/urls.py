from django.urls import path
from . import views


app_name = "scraper_config"
urlpatterns = [
    path("", views.index, name="index"),
    path("api/", views.get_scraped_data, name="api"),
    path("start/", views.start_scraping, name="start_scraping"),
    path("logs/", views.get_scraper_logs, name="scraper_logs")
]
