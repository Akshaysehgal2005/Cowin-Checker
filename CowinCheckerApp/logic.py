import time
import pandas as pd
from datetime import datetime
import requests
import json
import pickle

token = "1888108921:AAErkMkgi1SZQoazLxk4cP2tQ0AEv_S2PfI"
group_id = '-407207987'  #'-570867631'

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
    url_district_fill = url_district + '?district_id=' + str(district) + '&date=' + get_today()
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
    return df

def nlg(district, age, vaccine, fee):
    df = get_by_district(district, age, vaccine, fee)
    try:
        if len(df) > 0:
            return "I found {} slots available across {} centers for the {} district in the next few days for your search parameters".format(
                    df['available_capacity'].sum(), len(df), df['district_name'][0])
        else:
            return "No available slots in this district. Please check again later."
    except:
        return "No available slots in this district. Please check again later."



#import district dictionary
# districts_dict = fetch_districts()
# districts_dict_inv = dict((v,k) for k,v in districts_dict.items())
#
# with open('districts_dict.pickle', 'wb') as handle:
#     pickle.dump(districts_dict_inv, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('districts_dict.pickle', 'rb') as handle:
    districts_dict = pickle.load(handle)


class telegram_chatbot():

    def __init__(self, token):
        self.token = token
        self.base = "https://api.telegram.org/bot{}/".format(self.token)

    def get_updates(self, offset=None):
        url = self.base + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        r = requests.get(url)
        return json.loads(r.content)

    def send_message(self, msg):
        url = self.base + "sendMessage?chat_id="+group_id+"&text={}".format(msg)
        if msg is not None:
            requests.get(url)

bot = telegram_chatbot(token)

slot_flag = 0
inp_params = ['140','skip','skip','skip']

#Responses
def make_reply(msg):
    global slot_flag
    global inp_params
    reply = None
    if msg is not None and msg.split()[0]=='@VacHelperBot':
        msg = ' '.join(msg.split()[1:])
        if msg.lower() in ['hello','hi','hi there']:
            reply = "hello"
        elif msg.lower() in ['thanks','thank you']:
            reply = "You are welcome!"
        elif msg.lower() == '!slot':
            slot_flag = 1
            reply = "Please enter district name"
        elif msg in list(districts_dict.keys()) and slot_flag==1:
            inp_params[0] = districts_dict.get(str(msg),'140')
            slot_flag=2
            reply = "Please enter age group (skip, 18, 45)"
        elif msg.lower() in ['skip','18','45'] and slot_flag==2:
            inp_params[1] = msg
            slot_flag=3
            reply = "Please enter vaccine type (skip, covaxin, covishield)"
        elif msg.lower() in ['skip', 'covaxin', 'covishield'] and slot_flag==3:
            inp_params[2] = msg.upper()
            slot_flag=4
            reply = "Please enter fee type (skip, free, paid)"
        elif msg.lower() in ['skip', 'free', 'paid'] and slot_flag==4:
            inp_params[3] = msg[0].upper()+msg[1:].lower()
            print(inp_params)
            slot_flag = 0
            reply = nlg(*inp_params)
            inp_params = ['140', 'skip', 'skip', 'skip']

        elif msg.lower() == '!clear':
            inp_params = ['140', 'skip', 'skip', 'skip']
            reply = "All inputs cleared!"
        elif msg.lower() == '!help':
            reply = "Try the following commands: \n NOTE!! Please make sure to include @VacHelperBot before each response to the bot! \n !help - Helpful commands \n !slot - Check slot availability \n !clear - Clear inputs"
        else:
            reply = "Invalid input!"
    return reply

# def send_msg(m, token):
#     base = "https://api.telegram.org/bot{}/".format(token)
#     url = base + "sendMessage?chat_id=-570867631&text={}".format(m)
#     if m is not None:
#         requests.get(url)
#

def get_resp(token):
    base = "https://api.telegram.org/bot{}/".format(token)
    url = base + "getUpdates"
    item = requests.get(url).json()['result'][-1]
    return item

# update_id = None
try: update_id = get_resp(token).get('update_id',None)
except: update_id = None

print("Bot is running!")
while True:
#for i in range(20):
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