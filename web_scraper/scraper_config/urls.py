from django.urls import path
from . import views


app_name = "scraper_config"
urlpatterns = [
    path("", views.index, name="index"),
    path("api/", views.get_scraped_data, name="api"),
]
