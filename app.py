from flask import Flask, render_template,redirect,url_for,request
from Predictions import Predictor
from Predictions import Fetcher
from datetime import datetime
from datetime import timedelta
model=Predictor()
app = Flask(__name__)
@app.route("/")
def welcome() :
    data = [
        ("01-02-2021",3309),
        ("02-02-2021",2609),
        ("03-02-2021",2409),
        ("04-02-2021",6009),
        ("05-02-2021",7309),
        ("06-02-2021",8309),
        ("07-02-2021",6043),
    ]
    
    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    return render_template("index.html", labels=labels, values=values)
@app.route("/<coin>")
def coin(coin):
    fetcher=Fetcher("btcusd")
    histodata=fetcher.getlast60()
    predicted=model.predict_values(histodata)
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

    return render_template("{}.html".format(coin), labels=labels, values=values)

    
if __name__== '__main__' :
    app.run(debug=True)
    