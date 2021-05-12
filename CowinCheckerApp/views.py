from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from CowinCheckerApp.logic import fetch_districts, nlg, get_by_district
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def index(request):
    return HttpResponse("<h1>Welcome to Cowin-Checker App</h1> "
                        "The goal of this app is to help people get quick and easy updates for Vaccination."
                        "<br><br>"
                        "www.akshaysehgal.com © 2021")

# def bypin(request):
#         pin = request.GET.get("pin",'122001')
#         age = request.GET.get("age", '')
#         result = get_by_pin(pin, age)
#         return JsonResponse(result)

def bydistrict(request):
    district = request.GET.get("district",'140')
    age = request.GET.get("age", '')
    vaccine = request.GET.get("vaccine", '')
    fee = request.GET.get("fee", '')
    result = get_by_district(district, age, vaccine, fee).to_html()
    return HttpResponse(result)

def botreply(request):
    district = request.GET.get("district", '140')
    age = request.GET.get("age", '')
    vaccine = request.GET.get("vaccine", '')
    fee = request.GET.get("fee", '')
    result = nlg(get_by_district(district, age, vaccine, fee))
    return HttpResponse(result)

def getdistricts(request):
    return HttpResponse(fetch_districts())

@csrf_exempt
def webhook_endpoint(request):
    params = json.loads(request.body)['queryResult']['parameters']

    district = params.get('geo-city')
    age = params.get('age','skip')
    vaccine = params.get('vaccine','skip')
    fee = params.get('fee','skip')

    output = nlg(get_by_district(district, age, vaccine, fee))
    payload = '''{"fulfillmentMessages": [{"text": {"text": ["''' + output + '''"]}}]}'''
    return HttpResponse(payload)
