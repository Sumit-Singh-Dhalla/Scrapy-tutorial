import logging
import string
import uuid

import scrapy

from tutorial.utils.dump_data import get_tag_text, get_hash
from tutorial.utils.templates import TEMPLATES


class CaaSpider(scrapy.Spider):
    name = "caa_spider"
    crawled_urls = []
    exists = dict()
    page = 1
    index = 1
    base_url = "https://www.no-trouble.caa.go.jp/search/result{page_no}.html"
    start_urls = ["https://www.no-trouble.caa.go.jp/search/result.html"]

    def parse(self, response, **kwargs):
        return self.parse_search_page(response)

    def parse_search_page(self, response):
        for table_row in response.css("table tbody tr"):

            link = table_row.css("td")[0].css("p a::attr(href)").get()
            item = {
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
                "to_db": True,
                "to_file": True,
                "uuid": str(uuid.uuid4())
                }

            test_str = "".join([item['title'], item['detail'], item['trans_type'], item['products'], item['violation'],
                                item['laws'], item['date'], item['agency']])
            test_str = test_str.translate(str.maketrans('', '', string.punctuation)).replace(" ", "")
            hash = get_hash(test_str)
            if self.db["caa_search"].find_one({"hash": hash}):
                if (self.index - 1) in self.exists and (self.index - 2) in self.exists:
                    logging.info("The records are repeating now")
                    break
                self.exists.update({self.index: hash})
                self.index += 1
                continue

            # add hash in db update too
            item.update({"hash": hash})
            if not item.get("is_pdf") and link and link not in self.crawled_urls:
                self.crawled_urls.append(link)
                yield scrapy.Request(
                    link, self.parse_nested_page, cb_kwargs=item
                )

            self.index += 1

            yield item

        next_page = response.css('li a:contains(">")')
        try:
            next_page[next_page.css("a::text").getall().index(">")].css("a::attr(href)").get()
        except ValueError:
            return
        if next_page is not None:
            self.page += 1
            print(f"going to crawl next page {self.page}")
            yield response.follow(self.base_url.format(page_no=self.page), callback=self.parse)

    def parse_nested_page(self, response, **kwargs):
        template_used = response.url[:len(".".join(response.url.split("/")[:3]))+1]
        call_func = TEMPLATES.get(template_used, "")
        if call_func:
            item = call_func(response)
        else:
            item = {}
        item.update({
            "uuid": str(uuid.uuid4()),
            "link": response.url,
            "to_db": True,
            "to_file": True,
            "type": "caa_site_detail",
            "html_content": response.text,
            "template_used": template_used
        })

        return item

