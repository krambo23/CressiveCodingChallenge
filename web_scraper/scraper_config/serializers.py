from rest_framework import serializers
from .models import ScrapedTable


class ScrapedTableSerializers(serializers.ModelSerializer):
    class Meta:
        model = ScrapedTable
        fields = [
            "title",
            "description",
            "price",
            "rating",
            "asin",
            "page_number",
            "search_result_position",
            "is_sponsored",
            "keyword",
            "date_time_scraped"
        ]
