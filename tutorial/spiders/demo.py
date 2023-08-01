import pdb
import uuid

import scrapy
from scrapy import signals
from scrapy.exceptions import NotSupported
import pandas as pd

from tutorial.utils.dump_data import dump_file, get_table_data, get_headers


class CaaSpider(scrapy.Spider):
    name = "demo"
    crawled_urls = {}
    page = 1
    index = 1
    start_urls = ["https://www.shouhiseikatu.metro.tokyo.lg.jp/torihiki/shobun/shobun230531.html"]

    # def start_requests(self):
        # urls = [
        #     self.base_url.format(page_no=self.page)
        # ]
        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        children = response.css('div#LayerContentsInner > *')
        data = get_headers(children[21]),
        print("here is the data->", data)
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