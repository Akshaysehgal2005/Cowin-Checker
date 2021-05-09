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


    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': 'https://selfregistration.cowin.gov.in',
        'Authorization': f'Bearer "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiI3ZTk0ZjVkNS0zMmI2LTRmZDItYjM0MC0xOGM4YzY5NTIxNzkiLCJ1c2VyX2lkIjoiN2U5NGY1ZDUtMzJiNi00ZmQyLWIzNDAtMThjOGM2OTUyMTc5IiwidXNlcl90eXBlIjoiQkVORUZJQ0lBUlkiLCJtb2JpbGVfbnVtYmVyIjo5OTE2NTk0Nzc4LCJiZW5lZmljaWFyeV9yZWZlcmVuY2VfaWQiOjMzNTE4NTY1MTk5MzYwLCJzZWNyZXRfa2V5IjoiYjVjYWIxNjctNzk3Ny00ZGYxLTgwMjctYTYzYWExNDRmMDRlIiwidWEiOiJNb3ppbGxhLzUuMCAoTWFjaW50b3NoOyBJbnRlbCBNYWMgT1MgWCAxMF8xNV83KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvOTAuMC40NDMwLjkzIFNhZmFyaS81MzcuMzYiLCJkYXRlX21vZGlmaWVkIjoiMjAyMS0wNS0wOVQwMToxNTozMC4xMjRaIiwiaWF0IjoxNjIwNTIyOTMwLCJleHAiOjE2MjA1MjM4MzB9.KvVMoL8BL1OszBbKzE-lHvsUNMHPCFps0_Wj266PdxA"',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://selfregistration.cowin.gov.in/',
        'Sec-GPC': '1',
        'TE': 'Trailers',
    }

    result = requests.get(url_pin_fill, headers=headers)
    print('response from api setu!!:', result)

    meta = ['center_id', 'name', 'address', 'state_name', 'district_name', 'block_name', 'pincode', 'fee_type']
    df = pd.json_normalize(result.json()['centers'], 'sessions',meta)
    df = df.drop(['slots'], 1)

    return df.to_dict()