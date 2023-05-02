from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import ScrapedTable
from .serializers import ScrapedTableSerializers


# API Endpoints
def get_scraped_data(request):
    data = ScrapedTable.objects.all()
    serializer = ScrapedTableSerializers(data, many=True)
    return JsonResponse({"data": serializer.data}, safe=False)


# Views
def index(request):
    return HttpResponse("Hello World")
