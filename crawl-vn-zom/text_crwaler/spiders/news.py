import scrapy
import json
import requests
import xml.etree.ElementTree as ET
from tqdm import tqdm
import logging

logging.getLogger('scrapy').propagate = False

def fetch_sitemap(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None

def filter_urls_with_keyword(xml_string, keyword):
    root = ET.fromstring(xml_string)
    filtered_urls = []
    for url in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
        loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
        if keyword in loc:
            filtered_urls.append(loc)
    return filtered_urls

sitemap_url = "https://vn-z.vn/sitemap-1.xml"

sitemap_content = fetch_sitemap(sitemap_url)

if sitemap_content is not None:
    keyword = "/vn-z.vn/threads/"
    filtered_urls = filter_urls_with_keyword(sitemap_content, keyword)
print(len(filtered_urls))

class NewsCrawler (scrapy.Spider):
    name  = 'text_crawler'

    def __init__(self):
        self.start_urls = filtered_urls

    def start_requests(self):
     for i in tqdm(range(0, len(self.start_urls))):
         yield scrapy.Request(
            url=self.start_urls[i]
         )

    def parse(self, response):
        for news in response.css("div.p-body"):

            yield {
            "title" :  news.css("h1.p-title-value::text").get(),
            "link" : response.request.url,
            "field" :  news.css("ul.p-breadcrumbs li a span::text").getall(), 
            "raw_text" : news.css("div.bbWrapper").get(),
            "description" : news.css("div.bbWrapper::text").getall(),
            "ref" : news.css("div.someForums-list dl a::text").getall() ,
            "ref_link" : ["vn-z.vn" + href for href in news.css("div.someForums-list dl a::attr(href)").extract()]
            }


