import time
import requests
import pandas as pd
from collections import ChainMap

def fetch_districts():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    states = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/states', headers=headers)
    states = [i.get('state_id') for i in states.json().get('states')]

    d = []
    for i in st:
        ll = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/districts/'+str(i), headers=headers)
        time.sleep(0.1)
        d.append(ll.json())

    dictionary_districts = {j.get('district_id'):j.get('district_name') for i in d for j in i.get('districts')}
    dictionary_districts = dict(sorted(dictionary_districts.items()))
    return dictionary_districts

#dictionary_districts = fetch_districts()

def get_by_pin(pin, date):
    url_pin = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin'
    #url_district = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict'

    url_pin_fill = url_pin + '?pincode='+ pin + '&date=' + date

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    result = requests.get(url_pin_fill, headers=headers)
    print('response from api setu!!:', result)

    meta = ['center_id', 'name', 'address', 'state_name', 'district_name', 'block_name', 'pincode', 'fee_type']
    df = pd.json_normalize(result.json()['centers'], 'sessions',meta)
    df = df.drop(['slots'], 1)

    return df.to_dict()