import time
import os
import telebot
from flask import Flask, request
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
#
from fbprophet import Prophet


TOKEN = "YOUR-TOKEN-HERE" # mybot
bot = telebot.TeleBot(token=TOKEN)

today = str(date.today())

server = Flask(__name__)


# Install yfinance package. 
#!pip install yfinance

import yfinance as yf
#
# Get values for

stocks = ['PETR4.SA', 'TAEE4.SA', 'ITSA4.SA']

# Download data

data = {}
for i in range(len(stocks)):
    temp = yf.download(stocks[i], '2020-01-01', today)
    if stocks[i] == 'PETR4.SA':
        df_petr4 = temp[['Open','Close']]
  
    if stocks[i] == 'TAEE4.SA':
        df_taee4 = temp[['Open','Close']]

    if stocks[i] == 'ITSA4.SA':
        df_itsa4 = temp[['Open','Close']]

    data.update({stocks[i]:temp.Close})

df = pd.DataFrame(data, columns=stocks)
#
for i, col in enumerate(df.columns):
    df[col].plot(grid=True, title='PETR4.SA, TAEE4.SA e ITSA4.SA\nCotação de Fechamento das Ações em 2020\nPeriodo: de 01/jan até hoje')

plt.xticks(rotation=70)
plt.legend(df.columns)
plt.savefig('all.png', bbox_inches='tight')

#####################################################

# Graphics
df_petr4.plot(grid=True, title='Cotação da PETR4 em 2020\nPeriodo: de 01/jan até hoje' )
plt.savefig('petr4.png')
#
df_taee4[['Open', 'Close']].plot(grid=True, title='Cotação da TAEE4 em 2020\nPeriodo: de 01/jan até hoje' )
plt.savefig('taee4.png')
#
df_itsa4[['Open','Close']].plot(grid=True, title='Cotação da ITSA4 em 2020\nPeriodo: de 01/jan até hoje' )
#
plt.savefig('itsa4.png')

##################### Função Forecast ################################

# Forecast by Prophet

prediction_size = 30 # dias

def stock(stock):
    stock.reset_index(inplace=True)
    df = pd.DataFrame()
    df['ds'] = stock['Date']
    df['y']  = stock['Close']
    return df

def predict_stock(model,df,prediction_size, stock):
    model.fit(df)
    future = model.make_future_dataframe(periods=prediction_size)
    forecast = model.predict(future)
    fig = model.plot(forecast, figsize=(10,5))
    ax = fig.gca()
    ax.set_title(stock+"\nForecast by Prophet\nPeriod: next 30 days from today", size=18)
    ax.set_xlabel("Date", size=14)
    ax.set_ylabel("Close", size=14)
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    fig.savefig('prophet-'+stock+'.png', bbox_inches='tight')
    #
    fig = model.plot_components(forecast, figsize=(10,5))
    fig.savefig('components-'+stock+'.png')

##################### Previsões ################################

# PETR4
model1 = Prophet(interval_width=0.95)
df = stock(df_petr4)
predict_stock(model1,df,prediction_size,'PETR4')
#
# TAEE4
model2 = Prophet(interval_width=0.95)
df = stock(df_taee4)
predict_stock(model2,df,prediction_size,'TAEE4')
#
# ITSA4
model3 = Prophet(interval_width=0.95)
df = stock(df_itsa4)
predict_stock(model3,df,prediction_size,'ITSA4')
 
##################### Mensagens ################################

@bot.message_handler(commands=['start']) # welcome message
def send_welcome(message):               # handler
    photo = open('bot-b3.png', 'rb')
    bot.send_photo(message.chat.id, photo)
    texto = 'BEM VINDO\nEste bot traz a cotação de: 
    \nPETR4, TAEE4 e ITSA4.\nPeriodo: desde janeiro de 2020 
    até a data atual.\nTraz também a previsão de fechamento 
    nos próximos 30 dias.\nVeja: /menu'
    bot.reply_to(message, texto)

@bot.message_handler(commands=['bot']) # bot-b3
def send_welcome(message):  
    photo = open('bot-b3.png', 'rb')
    bot.send_photo(message.chat.id, photo)

@bot.message_handler(commands=['menu']) # Menu
def send_welcome(message):   
    photo = open('menu.png', 'rb')
    bot.send_photo(message.chat.id, photo)
    texto = 'PETR4 -> /petr4    /fore_petr4\nTAEE4 -> /taee4 
    /fore_taee4\nITSA4 -> /itsa4     /fore_itsa4\nAll -> /all'
    bot.reply_to(message, texto)

##################### Cotação ################################

@bot.message_handler(commands=['all']) # todas ações
def send_welcome(message):   
    photo = open('all.png', 'rb')
    bot.send_photo(message.chat.id, photo)


@bot.message_handler(commands=['petr4']) # PETR4
def send_welcome(message):   
    photo = open('petr4.png', 'rb')
    bot.send_photo(message.chat.id, photo)


@bot.message_handler(commands=['taee4']) # TAEE4
def send_welcome(message):  
    photo = open('taee4.png', 'rb')
    bot.send_photo(message.chat.id, photo)


@bot.message_handler(commands=['itsa4']) # ITSA4
def send_welcome(message):  
    photo = open('itsa4.png', 'rb')
    bot.send_photo(message.chat.id, photo)


##################### Forecast ################################

@bot.message_handler(commands=['fore_petr4'])
def send_welcome(message):  
    photo = open('prophet-PETR4.png', 'rb')
    bot.send_photo(message.chat.id, photo)
    photo = open('components-PETR4.png', 'rb')
    bot.send_photo(message.chat.id, photo)

@bot.message_handler(commands=['fore_taee4'])
def send_welcome(message):   
    photo = open('prophet-TAEE4.png', 'rb')
    bot.send_photo(message.chat.id, photo)
    photo = open('components-TAEE4.png', 'rb')
    bot.send_photo(message.chat.id, photo)

@bot.message_handler(commands=['fore_itsa4'])
def send_welcome(message):  
    photo = open('prophet-ITSA4.png', 'rb')
    bot.send_photo(message.chat.id, photo)
    photo = open('components-ITSA4.png', 'rb')
    bot.send_photo(message.chat.id, photo)
    
#####################################################

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json
                         (request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://YOUR-APP.herokuapp.com/'+TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
