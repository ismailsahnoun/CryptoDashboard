from Predictions import Predictor
from Predictions import Fetcher
# btcusd  ethusd  ltcusd  solusd
a=Predictor()
fetcher=Fetcher("btcusd")
data=fetcher.getlast60()
v=a.predict_values(data)
print(v)
last3=fetcher.getlast3()
print(last3)