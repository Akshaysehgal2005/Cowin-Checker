from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from CowinCheckerApp.logic import get_by_pin

# Create your views here.

def index(request):
        return HttpResponse("Hello world!")

def bypin(request):
        pin = request.GET.get("pin",'122001')
        date = request.GET.get("date",'08-05-2021')
        print(request)
        result = get_by_pin(pin, date)
        return JsonResponse(result)


