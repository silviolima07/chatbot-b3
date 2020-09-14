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
# Import yfinance 
import yfinance as yf
#
# Get values for

stocks = ['PETR4.SA', 'TAEE4.SA', 'ITSA4.SA']

# Download data

df = []
data = {}
for i in range(len(stocks)):
    temp = yf.download(stocks[i], '2020-01-01', today)
    if stocks[i] == 'PETR4.SA':
        df_petr4 = temp[['Open','Close']]
  
    if stocks[i] == 'TAEE4.SA':
        df_taee4 = temp[['Open','Close']]

    if stocks[i] == 'ITSA4.SA':
        df_itsa4 = temp[['Open','Close']]


    df.append(temp.Close)
    data.update({stocks[i]:df[i]})

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

#####################################################

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


@bot.message_handler(commands=['start']) # welcome message handler
def send_welcome(message):
    photo0 = open('bot-b3.png', 'rb')
    bot.send_photo(message.chat.id, photo0)
    texto = 'BEM VINDO\nPara Cotação -> /cotacao\nPara Forecast -> /forecast'
    bot.reply_to(message, texto)
    #photo0 = open('bot-b3.png', 'rb')
    #bot.send_photo(message.chat.id, photo0)

@bot.message_handler(commands=['bot']) # welcome message handler
def send_welcome(message):
    #bot.reply_to(message, 'Seja esperto como uma Águia')   
    photo1 = open('bot-b3.png', 'rb')
    bot.send_photo(message.chat.id, photo1)

@bot.message_handler(commands=['all']) # welcome message handler
def send_welcome(message):   
    photo2 = open('all.png', 'rb')
    bot.send_photo(message.chat.id, photo2)


@bot.message_handler(commands=['petr4']) # welcome message handler
def send_welcome(message):   
    photo3 = open('petr4.png', 'rb')
    bot.send_photo(message.chat.id, photo3)


@bot.message_handler(commands=['taee4']) # welcome message handler
def send_welcome(message):
    #bot.reply_to(message, 'Enviando uma image do grafico')   
    photo4 = open('taee4.png', 'rb')
    bot.send_photo(message.chat.id, photo4)


@bot.message_handler(commands=['itsa4']) # welcome message handler
def send_welcome(message):
    #bot.reply_to(message, 'Enviando uma image do grafico')   
    photo5 = open('itsa4.png', 'rb')
    bot.send_photo(message.chat.id, photo5)

@bot.message_handler(commands=['cotacao']) # welcome message handler
def send_welcome(message):  
    photo6 = open('cotacao.png', 'rb')
    bot.send_photo(message.chat.id, photo6)

@bot.message_handler(commands=['forecast']) # welcome message handler
def send_welcome(message):   
    photo7 = open('forecast.png', 'rb')
    bot.send_photo(message.chat.id, photo7)

#####################################################

@bot.message_handler(commands=['fore_petr4']) # welcome message handler
def send_welcome(message):
    #bot.reply_to(message, 'Enviando uma image do grafico')   
    photo6 = open('prophet-PETR4.png', 'rb')
    bot.send_photo(message.chat.id, photo6)
    photo61 = open('components-PETR4.png', 'rb')
    bot.send_photo(message.chat.id, photo61)

@bot.message_handler(commands=['fore_taee4']) # welcome message handler
def send_welcome(message):
    #bot.reply_to(message, 'Enviando uma image do grafico')   
    photo6 = open('prophet-TAEE4.png', 'rb')
    bot.send_photo(message.chat.id, photo6)
    photo61 = open('components-TAEE4.png', 'rb')
    bot.send_photo(message.chat.id, photo61)

@bot.message_handler(commands=['fore_itsa4']) # welcome message handler
def send_welcome(message):
    #bot.reply_to(message, 'Enviando uma image do grafico')   
    photo6 = open('prophet-ITSA4.png', 'rb')
    bot.send_photo(message.chat.id, photo6)
    photo61 = open('components-ITSA4.png', 'rb')
    bot.send_photo(message.chat.id, photo61)
#####################################################

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://app-ibovbot.herokuapp.com/'+TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
