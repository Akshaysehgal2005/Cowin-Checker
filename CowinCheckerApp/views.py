from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from CowinCheckerApp.logic import get_by_pin, get_by_district

# Create your views here.

def index(request):
        return HttpResponse("<h1>Welcome to Cowin-Checker App</h1> "
                            "The goal of this app is to help people get quick and easy updates for Vaccination."
                            "<br><br>"
                            "www.akshaysehgal.com © 2021")

def bypin(request):
        pin = request.GET.get("pin",'122001')
        result = get_by_pin(pin)
        return JsonResponse(result)

def bydistrict(request):
        district = request.GET.get("district",'188')
        result = get_by_district(district)
        return JsonResponse(result)

