import http.client as client
import json
import numpy as np

# query?function=TIME_SERIES_DAILY&symbol=qqq&apikey=9KJT5Q7YE3QBML63&outputsize=full
conn = client.HTTPSConnection('www.alphavantage.co')
conn.request('GET', '/query?function=TIME_SERIES_DAILY&symbol=qqq&apikey=9KJT5Q7YE3QBML63')
getresponse = conn.getresponse()
print(getresponse.code, getresponse.reason)
str = getresponse.read().decode('utf-8')
# print(str)
j = json.loads(str)
ts = j['Time Series (Daily)']
print(ts)
conn.close()
dates = sorted(j['Time Series (Daily)'].keys())
print(dates[:10])
priv = dates[0]
dates = dates[1:-1]

vols = []
vols.append(int(ts[priv]['5. volume']))
for d in dates:
    v = float(ts[d]['5. volume'])
    vols.append(v)
st = np.std(vols)
m = np.mean(vols)
vols = (vols - m) / st
vols = vols[1:]

data = []
for i, d in enumerate(dates):
    priv_c = float(ts[priv]['4. close'])
    o = float(ts[d]['1. open']) - priv_c
    h = float(ts[d]['2. high']) - priv_c
    l = float(ts[d]['3. low']) - priv_c
    c = float(ts[d]['4. close']) - priv_c
    v = vols[i]
    data.append((o, h, l, c, v))
print(data[-1:])
