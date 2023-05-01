# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


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

        # Convert "Price" to Float
        try:
            price = adapter.get("price")

            if price is "":
                price = -1

            price = price.replace("£", "")
            adapter["price"] = float(price)
        except:
            adapter["price"] = -1

        # Convert "Rating" to Float
        try:
            rating = adapter.get("rating").strip()

            if rating is "":
                rating = -1

            rating = rating.replace(" out of 5 stars", "")
            adapter["rating"] = float(rating)
        except:
            adapter["rating"] = -1

        return item
