import pdb
import uuid

import scrapy
from scrapy import signals, FormRequest
from scrapy.exceptions import NotSupported
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.http import HtmlResponse
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse


class MlitSpider(scrapy.Spider):
    name = "mlit"
    visited_urls = set()

    def __init__(self, **kwargs):
        super(MlitSpider, self).__init__(**kwargs)
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run Chrome in headless mode
        self.driver = webdriver.Chrome(options=chrome_options)

    def start_requests(self):
        urls = [
            "https://www.mlit.go.jp/nega-inf/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):

        for ul in response.css("section.step02 div.inner").css("ul.step02__link li"):
            link = ul.css("a::attr(href)").get()
            item = {
                "uuid": str(uuid.uuid4()),
                "link": link,
                "title": ul.css("li a h4::text").get(),
                "description": ul.css("li p::text").get(),
                "to_db": True,
                "to_file": True,
                "type": "mlit_parent"
            }
            if link not in self.visited_urls:  # Check if the link is not visited yet
                self.visited_urls.add(link)  # Add the link to the set of visited URLs
                yield scrapy.Request(link, callback=self.parse_linked_page, dont_filter=True,
                                     cb_kwargs={"uuid": item['uuid']})

            yield item
            break

    def parse_linked_page(self, response, **kwargs):
        # Click the button using Selenium
        self.driver.get(response.url)
        wait = WebDriverWait(self.driver, 10)  # Wait up to 10 seconds
        submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.submit')))
        submit_button.click()

        # Wait for the JavaScript to execute (you can use WebDriverWait if needed)
        self.driver.implicitly_wait(5)  # Wait for 5 seconds (adjust as needed)

        # Get the updated page source after clicking the button
        new_page_source = self.driver.page_source

        # Create a new response object from the updated page source
        updated_response = HtmlResponse(url=response.url, body=new_page_source, encoding='utf-8')

        # Continue parsing the page after clicking the button
        return self.after_click(updated_response, **kwargs)

    def after_click(self, response, **kwargs):
        for tr in response.css("table.result tr")[1:]:

            item = {
                "date": tr.css("td:nth-child(1)::text").get(),
                "name": tr.css("td:nth-child(2)::text").get() + " " + tr.css("td:nth-child(2) span::text").get(),
                "punish": tr.css("td:nth-child(3)::text").get(),
                "detail": tr.css("td:nth-child(4) a::text").getall(),
                "to_db": True,
                "to_file": True,
                "type": "mlit_child",
                "uuid": str(uuid.uuid4()),
                "mlit_id": kwargs.get("uuid")
            }
            yield item
        next_page = response.css("p.pagenation__next a::attr(href)").get()
        print(f"next page-->{next_page}")
        if next_page:
            if int(next_page[-1]) > 2:
                return
            next_page = response.urljoin(next_page)
            print(f"new next page-->", next_page)
            yield scrapy.Request(next_page, callback=self.after_click, cb_kwargs=kwargs)
