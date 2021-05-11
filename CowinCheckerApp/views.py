from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from CowinCheckerApp.logic import get_by_district, fetch_districts

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
        result = get_by_district(district, age, vaccine, fee)
        return HttpResponse(result)

def getdistricts(request):
    return HttpResponse(fetch_districts())



class telegram_chatbot():

    def __init__(self, config):
        self.token = self.read_token_from_config_file(config)
        self.base = "https://api.telegram.org/bot{}/".format(self.token)

    def get_updates(self, offset=None):
        url = self.base + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        r = requests.get(url)
        return json.loads(r.content)

    def send_message(self, msg, chat_id):
        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        if msg is not None:
            requests.get(url)

    def read_token_from_config_file(self, config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', 'token')