import time
import pandas as pd
from datetime import datetime
import requests
import json
import pickle

def fetch_districts():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    states = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/states', headers=headers)
    states = [i.get('state_id') for i in states.json().get('states')]

    d = []
    for i in states:
        ll = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/districts/'+str(i), headers=headers)
        time.sleep(0.1)
        d.append(ll.json())

    dictionary_districts = {j.get('district_id'):j.get('district_name') for i in d for j in i.get('districts')}
    dictionary_districts = dict(sorted(dictionary_districts.items()))
    result = pd.Series(dictionary_districts).reset_index().set_axis(['district_id','district_name'],1)
    return result.to_html()

def get_today():
    return datetime.today().strftime('%d-%m-%Y')

def get_by_district(district, age, vaccine, fee):
    # Create request and call api setu
    url_district = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict'
    url_district_fill = url_district + '?district_id=' + district + '&date=' + get_today()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    result = requests.get(url_district_fill, headers=headers)

    # Normalize json
    meta = ['center_id', 'name', 'address', 'state_name', 'district_name', 'block_name', 'pincode', 'fee_type']
    df = pd.json_normalize(result.json()['centers'], 'sessions', meta)
    df = df.drop(['slots','block_name','session_id'], 1)

    # Apply input filters
    try: age = int(age)
    except: age = None

    filters = [age, vaccine, fee]
    filter_cols = ['min_age_limit', 'vaccine', 'fee_type']
    valid = [[18, 45], ['COVISHIELD', 'COVAXIN'], ['Paid', 'Free']]

    mask = [i[0] not in i[1] for i in zip(filters, valid)]
    df = df.loc[(df[filter_cols].eq(filters) | mask).all(1)]

    # Filter for available capacity only
    df = df[df['available_capacity'] > 0]
    return df.to_html()

#import district dictionary
with open('districts_dict.pickle', 'rb') as handle:
    districts_dict = pickle.load(handle)

class telegram_chatbot():

    def __init__(self):
        self.token = "1888108921:AAErkMkgi1SZQoazLxk4cP2tQ0AEv_S2PfI"
        self.base = "https://api.telegram.org/bot{}/".format(self.token)

    def get_updates(self, offset=None):
        url = self.base + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        r = requests.get(url)
        return json.loads(r.content)

    def send_message(self, msg):
        url = self.base + "sendMessage?chat_id=-570867631&text={}".format(msg)
        if msg is not None:
            requests.get(url)

bot = telegram_chatbot()

#Responses
def make_reply(msg):
    reply = None
    if msg is not None:
        if msg.lower() in ['hello','hi','hi there']:
            reply = "hello"
        elif msg.lower() in ['thanks','thank you']:
            reply = "You are welcome!"
        elif msg.lower().isnumeric():
            reply = get_by_district(msg, age='', vaccine='', fee='')
    return reply


#update_id = None
u = 'https://api.telegram.org/bot1888108921:AAErkMkgi1SZQoazLxk4cP2tQ0AEv_S2PfI/getUpdates'
update_id = requests.get(u).json()['result'][-1].get('update_id',None)

#while True:
print("Bot is running!")
for i in range(2):
    updates = bot.get_updates(offset=update_id)
    updates = updates["result"]
    if updates:
        for item in updates:
            update_id = item["update_id"]
            try:
                message = str(item["message"]["text"])
            except:
                message = None
            from_ = item["message"]["from"]["id"]
            reply = make_reply(message)
            bot.send_message(reply)
            time.sleep(0.75)