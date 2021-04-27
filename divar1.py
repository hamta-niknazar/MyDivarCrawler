import requests as req
from bs4 import BeautifulSoup as BS
import time
import json
from flask import Flask

app = Flask(__name__)
@app.route('/')
def index():
    
    lastPage = ""
    url = "https://divar.ir/s/%s/%s?page=%d"%("tehran", "mobile-phones", 0)
    reqToGetTokens = req.get(url)
    
    contentAsBS = BS(reqToGetTokens.text, 'html.parser')
    post_cards = contentAsBS.select(".post-card-item .kt-post-card")

    my_data = []
    for j in range(len(post_cards)):
        data = {}
        reqToGetPhone = req.get("https://api.divar.ir/v5/posts/%s/"%post_cards[j]['href'].split("/")[-1])
        if reqToGetPhone.ok == False:
            lastPage = "Error at page %d item %d"%(i, j + 1)
            break

        data['title'] = reqToGetPhone.json()['data']['seo']['title']
        data['description'] = reqToGetPhone.json()['data']['seo']['description']
        data['price'] = reqToGetPhone.json()['data']['webengage']['price']
        data['date'] = reqToGetPhone.json()['widgets']['header']['date']
        data['city'] = reqToGetPhone.json()['data']['city']

        try:
            try:
                data['latitude'] = reqToGetPhone.json()['widgets']['location']['latitude']
                data['longitude'] = reqToGetPhone.json()['widgets']['location']['longitude']
            except:
                pass
            try:
                data['thumbnail'] = reqToGetPhone.json()['data']['seo']['thumbnail']
            except:
                pass
            data['web_images'] = reqToGetPhone.json()['widgets']['web_images']
        except:
            pass
        my_data.append(data)

        # time.sleep(1)
    # print(my_data)
    return json.dumps(my_data)
# server
app.run(host="0.0.0.0")
# local
#app.run(host="127.0.0.1")
