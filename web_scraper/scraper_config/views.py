from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import ScrapedTable, ScraperStatus
from .serializers import ScrapedTableSerializers
# from scraper import main


# API Endpoints
def get_scraped_data(request):

    try:
        keywords = request.GET["keywords"]
        date_time_scraped = request.GET["date_time_scraped"]
        data = ScrapedTable.objects.filter(keyword=keywords, date_time_scraped=date_time_scraped)
        serializer = ScrapedTableSerializers(data, many=True)
        return JsonResponse({"data": serializer.data}, safe=False)
    except:
        try:
            keywords = request.GET["keywords"]
            data = ScrapedTable.objects.filter(keyword=keywords)
            serializer = ScrapedTableSerializers(data, many=True)
            return JsonResponse({"data": serializer.data}, safe=False)
        except:
            try:
                date_time_scraped = request.GET["date_time_scraped"]
                data = ScrapedTable.objects.filter(date_time_scraped=date_time_scraped)
                serializer = ScrapedTableSerializers(data, many=True)
                return JsonResponse({"data": serializer.data}, safe=False)
            except:
                data = ScrapedTable.objects.all()
                serializer = ScrapedTableSerializers(data, many=True)
                return JsonResponse({"data": serializer.data}, safe=False)


# Views
def index(request):
    return render(request, "index.html")


def start_scraping(request):
    # TODO : Add Code For Triggering Scraper
    # main.main()
    return render(request, "start.html")


def get_scraper_logs(request):
    latest_scraper_logs = ScraperStatus.objects.order_by("scraper_last_ran")
    context = {
        "latest_scraper_logs": latest_scraper_logs
    }
    return render(request, "logs.html", context)
