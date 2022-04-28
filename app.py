from flask import Flask, render_template,redirect,url_for,request
from Predictions import Fetcher
from datetime import datetime
from datetime import timedelta
import pickle as pkl
from tensorflow.keras.models import load_model
from requests import get

app = Flask(__name__)

model=load_model("./models/minutes-model-60to2")
apikey="823616fee413d23338ea60dcdb269e52"
liveurl="http://api.coinlayer.com/live?access_key={}&target=usd&symbols=".format(apikey)

bitcoinopenscaler=pkl.load(open("./models/btcscalers/openscaler","rb"))
bitcoinclosescaler=pkl.load(open("./models/btcscalers/closescaler","rb"))
bitcoinlowscaler=pkl.load(open("./models/btcscalers/lowscaler","rb"))
bitcoinhighscaler=pkl.load(open("./models/btcscalers/highscaler","rb"))
@app.route("/register")
def register():
    return render_template("register.html")
@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/bitcoin")
def bitcoin():
    solanaprice=get("https://api.cryptowat.ch/markets/kraken/solusd/price").json()['result']['price']
    avaxprice=get("https://api.cryptowat.ch/markets/kraken/avaxusd/price").json()['result']['price']
    moneroprice=get("https://api.cryptowat.ch/markets/kraken/ltcusd/price").json()['result']['price']
    fetcher=Fetcher("btcusd",bitcoinopenscaler,bitcoinclosescaler,bitcoinhighscaler,bitcoinlowscaler)
    histodata=fetcher.getlast60()
    predicted=model.predict(histodata)
    predicted=bitcoinopenscaler.inverse_transform(predicted)
    predicted=predicted[0]
    last3=fetcher.getlast3()
    print(last3)
    data=[]
    now=datetime.now()
    data.append([(now-timedelta(minutes=2)).strftime("%H:%M"),last3[0][0]])
    data.append([(now-timedelta(minutes=1)).strftime("%H:%M"),last3[1][0]])
    data.append([now.strftime("%H:%M"),last3[2][0]])
    data.append([(now+timedelta(minutes=1)).strftime("%H:%M"),predicted[0]])
    data.append([(now+timedelta(minutes=2)).strftime("%H:%M"),predicted[1]])
    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    return render_template("bitcoin.html", labels=labels, values=values,solana=solanaprice,avax=avaxprice,monero=moneroprice)

@app.route("/solana")
def solana():
    fetcher=Fetcher("solusd",solanaopenscaler,solanaclosescaler,solanahighscaler,solanalowscaler)
    histodata=fetcher.getlast60()
    predicted=model.predict(histodata)
    predicted=solanaopenscaler.inverse_transform(predicted)
    predicted=predicted[0]
    last3=fetcher.getlast3()
    data=[]
    now=datetime.now()
    data.append([(now-timedelta(minutes=2)).strftime("%H:%M"),last3[0][0]])
    data.append([(now-timedelta(minutes=1)).strftime("%H:%M"),last3[1][0]])
    data.append([now.strftime("%H:%M"),last3[2][0]])
    data.append([(now+timedelta(minutes=1)).strftime("%H:%M"),predicted[0]])
    data.append([(now+timedelta(minutes=2)).strftime("%H:%M"),predicted[1]])
    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    return render_template("solana.html", labels=labels, values=values)
@app.route("/monero")
def monero():
    fetcher=Fetcher("xmrusd")
    histodata=fetcher.getlast60()
    predicted=model.predict_values(histodata)
    last3=fetcher.getlast3()
    data=[]
    now=datetime.now()
    data.append([(now-timedelta(minutes=2)).strftime("%H:%M"),last3[0][0]])
    data.append([(now-timedelta(minutes=1)).strftime("%H:%M"),last3[1][0]])
    data.append([now.strftime("%H:%M"),last3[2][0]])
    data.append([(now+timedelta(minutes=1)).strftime("%H:%M"),predicted[0]])
    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    return render_template("monero.html", labels=labels, values=values)
@app.route("/avalanche")
def avalanche():
    etcher=Fetcher("avaxusd")
    histodata=fetcher.getlast60()
    predicted=model.predict_values(histodata)
    last3=fetcher.getlast3()
    data=[]
    now=datetime.now()
    data.append([(now-timedelta(minutes=2)).strftime("%H:%M"),last3[0][0]])
    data.append([(now-timedelta(minutes=1)).strftime("%H:%M"),last3[1][0]])
    data.append([now.strftime("%H:%M"),last3[2][0]])
    data.append([(now+timedelta(minutes=1)).strftime("%H:%M"),predicted[0]])
    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    return render_template("avalanche.html", labels=labels, values=values)
if __name__== '__main__' :
    app.run(debug=True)
    