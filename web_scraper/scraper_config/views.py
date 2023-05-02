from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import ScrapedTable
from .serializers import ScrapedTableSerializers


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
    return HttpResponse("Hello World")


def start_scraping(request):
    return HttpResponse("Scraping Started! - Check Progress On get_scraper_logs()")


def get_scraper_logs(request):
    return HttpResponse("Scraper Logs")
