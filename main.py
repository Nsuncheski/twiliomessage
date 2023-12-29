import os
from twilio.rest import Client
import time
import pandas as pd
from decouple import config
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


# import pandas as pd
import requests
from bs4  import BeautifulSoup
from tqdm import tqdm

from datetime import datetime

query = '-34.519508,-58.516771'
api_key = config('API_KEY_WAPI')

url_clima = 'http://api.weatherapi.com/v1/forecast.json?key='+api_key+'&q='+query+'&days=1&aqi=no&alerts=no'
url_clima

response = requests.get(url_clima).json()

response
response.keys()
response['forecast']['forecastday'][0].keys()
fecha = response['forecast']['forecastday'][0]['hour'][1]['time'].split()[0]
hora = int(response['forecast']['forecastday'][0]['hour'][1]['time'].split()[1].split(':')[0])

def get_forecast(response,i):
    
    fecha = response['forecast']['forecastday'][0]['hour'][i]['time'].split()[0]
    hora = int(response['forecast']['forecastday'][0]['hour'][i]['time'].split()[1].split(':')[0])
    condicion = response['forecast']['forecastday'][0]['hour'][i]['condition']['text']
    tempe = float(response['forecast']['forecastday'][0]['hour'][i]['temp_c'])
    rain = response['forecast']['forecastday'][0]['hour'][i]['will_it_rain']
    prob_rain = response['forecast']['forecastday'][0]['hour'][i]['chance_of_rain']
    
    return fecha,hora,condicion,tempe,rain,prob_rain

datos = []

for i in tqdm(range(len(response['forecast']['forecastday'][0]['hour'])),colour = 'green'):
    
    datos.append(get_forecast(response,i))

col = ['Fecha','Hora','Condición', 'Temperatura','Lluvia','Prob_lluvia']
df = pd.DataFrame(datos, columns=col)
df_pos_rain = df
df_rain = df_pos_rain[['Hora','Condición', 'Temperatura', 'Prob_lluvia']]
df_rain.set_index('Hora', inplace=True)

mensaje = '\nHola! \n\n\n El pronostico del tiempo hoy '+ df['Fecha'][0] +' en ' + query +' es : \n\n\n ' + str(df_rain)

time.sleep(2)
account_sid = config('TWILIO_ACCOUNT_SID') 
auth_token = config('TWILIO_AUTH_TOKEN')

client = Client(account_sid, auth_token)

message = client.messages.create(
  from_=config('FROM'),
  body='\nHola! \n\n\n El pronostico de lluvia hoy '+ df['Fecha'][0] +' en Munro es :\n\n\n ' + str(df_rain),
  to=config('TO')
)
print('Mensaje Enviado ' + message.sid)