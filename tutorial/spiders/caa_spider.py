import pdb
import uuid

import scrapy
from scrapy import signals
from scrapy.exceptions import NotSupported

from tutorial.utils.dump_data import get_table_data, get_tag_text


class CaaSpider(scrapy.Spider):
    name = "caa_spider"
    crawled_urls = []
    page = 1
    index = 1
    base_url = "https://www.no-trouble.caa.go.jp/search/result{page_no}.html"
    call_func = dict()
    # start_urls = []

    def start_requests(self):
        urls = [
            self.base_url.format(page_no=self.page)
        ]

        self.call_func = {
            "https://www.caa.go.jp/notice/entry": self.crawl_caa,
            "https://www.shouhiseikatu.metro.tokyo.lg.jp/torihiki/shobun": self.crawl_shouhiseikatu
        }

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        for table_row in response.css("table tbody tr"):
            link = table_row.css("td")[0].css("p a::attr(href)").get()
            item = {
                "id": self.index,
                "site": response.url,
                "title": get_tag_text(table_row, "td:nth-child(1) p a"),
                "link": link,
                "detail": get_tag_text(table_row, "td:nth-child(2)"),
                "trans_type": get_tag_text(table_row, "td:nth-child(3)"),
                "products": get_tag_text(table_row, "td:nth-child(4) p"),
                "violation": get_tag_text(table_row, "td:nth-child(5) p"),
                "laws": get_tag_text(table_row, "td:nth-child(6) p"),
                "date": get_tag_text(table_row, "td:nth-child(7)"),
                "agency": get_tag_text(table_row, "td:nth-child(8)"),
                "is_pdf": link.endswith(".pdf") if link else False,
                "type": "caa_search",
                "to_db": False,
                "to_file": True,
                "uuid": str(uuid.uuid4())
            }
            self.index += 1
            if not item.get("is_pdf") and link and link not in self.crawled_urls:
                self.crawled_urls.append(link)
                yield scrapy.Request(
                    link, self.parse_nested_page, cb_kwargs=item
                )
            yield item

        # next_page = response.css('li a:contains(">")')
        # try:
        #     next_page[next_page.css("a::text").getall().index(">")].css("a::attr(href)").get()
        # except ValueError:
        #     return
        # if next_page is not None:
        #     self.page += 1
        #     print(f"going to crawl next page {self.page}")
        #     yield response.follow(self.base_url.format(page_no=self.page), callback=self.parse)

    def parse_nested_page(self, response, **kwargs):

        if response.url.startswith("https://www.caa.go.jp/notice/entry"):
            item = self.call_func["https://www.caa.go.jp/notice/entry"](response)
        elif response.url.startswith("https://www.shouhiseikatu.metro.tokyo.lg.jp/torihiki/shobun"):
            item = self.call_func["https://www.shouhiseikatu.metro.tokyo.lg.jp/torihiki/shobun"](response)
        else:
            item = {}
        item.update({
            "uuid": str(uuid.uuid4()),
            "link": response.url,
            "to_db": False,
            "to_file": True,
            "type": "caa_site_detail"
        })

        return item

    def crawl_shouhiseikatu(self, response):
        children = response.css('div#LayerContentsInner > *')
        item = {
            "detail_1": get_tag_text(children[11], "h1"),
            "detail_1_date": get_tag_text(children[1], "p"),
            "detail_2": get_tag_text(children[2], "div"),
            get_tag_text(children[3], "h2"): get_table_data(children[4], "vertical-no-header"),
            get_tag_text(children[6], "h2"): get_tag_text(children[7], "table tr td"),
            get_tag_text(children[8], "h2"): get_tag_text(children[9], "p") + get_tag_text(children[10],
                                                                                           "ol li",
                                                                                           append_by="\n"),
            get_tag_text(children[11], "h2"): get_table_data(children[12], "horizontal"),
            get_tag_text(children[13], "h2"): get_tag_text(children[14], "ol li", append_by="\n"),
            get_tag_text(children[15], "h2"): get_table_data(children[16], "horizontal"),
            get_tag_text(children[17], "h3"): get_tag_text(children[18], "p") + "\n" + get_tag_text(children[19], "p"),
            get_tag_text(children[20], "h2"): get_table_data(children[21], "horizontal-multi-header"),
            get_tag_text(children[22], "h2"): get_tag_text(children[23], "ul li", append_by="\n"),
            get_tag_text(children[24], "h2"): get_tag_text(children[25], "p") + get_tag_text(children[26],
                                                                                             "ul li",
                                                                                             append_by="\n"),
        }
        return item

    def crawl_caa(self, response):
        _item = {}
        for section in response.css("section:has(p)"):
            heading = get_tag_text(section, "h2")
            detail = get_tag_text(section, "p")
            if heading:
                _item.update({heading: detail})
            else:
                _item.update({"open_text": detail})
        return _item
