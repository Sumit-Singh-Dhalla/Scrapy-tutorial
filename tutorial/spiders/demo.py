import pdb
import uuid

import pymongo
import scrapy
from bson import ObjectId
from scrapy.http import HtmlResponse
from scrapy import signals
from scrapy.exceptions import NotSupported
import pandas as pd

from tutorial.utils.dump_data import get_table_data, get_headers, get_tag_text


class CaaSpider(scrapy.Spider):
    name = "demo"
    crawled_urls = {}
    page = 1
    index = 1
    # start_urls = ["https://www.shouhiseikatu.metro.tokyo.lg.jp/torihiki/shobun/shobun230531.html"]
    start_urls = ["https://www.google.com/"]

    # def start_requests(self):
        # urls = [
        #     self.base_url.format(page_no=self.page)
        # ]
        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        # html_content = response.text
        client = pymongo.MongoClient("localhost", 27017)
        db = client["cdl"]
        obj = db["detail_html_content"].find_one({"_id": ObjectId("64c9e95b8f89349ad65cfb28")})
        response = HtmlResponse(url=response.url, body=obj['content'], encoding='utf-8')
        print(response)
        children = response.css('div#LayerContentsInner > *')
        pdb.set_trace()
        print(get_tag_text(children[11], "h1"))

        # db["detail_html_content"].insert_one({"link": response.url, "content": html_content})
        client.close()

        # children = response.css('div#LayerContentsInner > *')
        # data = get_headers(children[21]),
        # print("here is the data->", data)
        # dump_file(response, "response1.json")
        # data = response.css("div#LayerContentsInner ::text").getall()
        # # pdb.set_trace()
        # print(data)
        # with open("all_data.txt", 'w') as _file:
        #     for obj in data:
        #         _file.write(obj)
        #     _file.close()
        # all_tables = response.css("table")
        # for table in all_tables:
        #     table_data = pd.read_html(table.get())
        #     # pdb.set_trace()
        #     if isinstance(table_data, list):
        #         for i, df in enumerate(table_data):
        #             # Dump each DataFrame to a CSV file
        #             df.to_csv(f'table_{self.index + 1}.csv', index=False)
        #             self.index += 1
        return {"name": "Sumit Singh"}