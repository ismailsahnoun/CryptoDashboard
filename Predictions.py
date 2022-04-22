import tensorflow as tf
import pickle as pkl
from requests import get
import numpy as np
class Predictor():
    def __init__(self):
        self.model=tf.keras.models.load_model('./models/minutes-model-60to2')
        self.openscaler=pkl.load(open('models/openscaler','rb'))
    def predict_values(self,data):
        output=self.model.predict(data)
        output=self.openscaler.inverse_transform(output)
        return output[0]
class Fetcher():
    def __init__(self,coinsym):
        self.coin=coinsym
        self.openscaler=pkl.load(open('models/openscaler','rb'))
        self.closescaler=pkl.load(open('models/closescaler','rb'))
        self.highscaler=pkl.load(open('models/highscaler','rb'))
        self.lowscaler=pkl.load(open('models/lowscaler','rb'))
    def getlast60(self):
        openlist=[]
        closelist=[]
        highlist=[]
        lowlist=[]
        openlist=[]
        closelist=[]
        highlist=[]
        lowlist=[]
        url="https://api.cryptowat.ch/markets/coinbase-pro/{}/ohlc".format(self.coin)
        resp=get(url)
        data=resp.json()
        data=data['result']['60'][-60:]
        for i in range(len(data)):
            openlist.append([data[i][1]])
            highlist.append([data[i][2]])
            lowlist.append([data[i][3]])
            closelist.append([data[i][4]])
        openlist=np.array(openlist)
        highlist=np.array(highlist)
        lowlist=np.array(lowlist)
        closelist=np.array(closelist)
        openlist=self.openscaler.transform(openlist)
        closelist=self.closescaler.transform(closelist)
        highlist=self.highscaler.transform(highlist)
        lowlist=self.lowscaler.transform(lowlist)
        datalist=[]
        for i in range(len(openlist)):
            datalist.append([openlist[i][0],highlist[i][0],lowlist[i][0],closelist[i][0]])
        datalist=np.array([datalist])
        return datalist
    def getlast3(self):
        openlist=[]
        url="https://api.cryptowat.ch/markets/coinbase-pro/{}/ohlc".format(self.coin)
        resp=get(url)
        data=resp.json()
        data=data['result']['60'][-3:]
        for i in range(len(data)):
            openlist.append([data[i][1]])
        openlist=np.array(openlist)
        return openlist

