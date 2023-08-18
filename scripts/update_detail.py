import pymongo
from scrapy.http import HtmlResponse

# html_content = response.text
client = pymongo.MongoClient("localhost", 27017)
db = client["cdl"]
collection = db["caa_site_detail"]
qs = collection.find()
for obj in qs:
    response = HtmlResponse(url=obj["link"], body=obj['html_content'], encoding='utf-8')
    children = response.css('div#LayerContentsInner > *')
    print(len(children))
    if not children:
        continue
    detail_1 = " ".join(children[0].css("h1 ::text").getall())
    print(f"detail 1 is->{detail_1}")
    myquery = {"_id": obj['_id']}
    new_values = {"$set": {"detail_1": detail_1}}

    collection.update_one(myquery, new_values)

client.close()
