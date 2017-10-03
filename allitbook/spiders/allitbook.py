from allitbook.items import AllitbookItem
from scrapy import Spider, Item, Field, Request
import urllib.parse as urlparse
import re
import validators

class MySpider(Spider):
  name = "allitebooks"
  allowed_domains = ["allitebooks.com"]
  start_urls = ["http://www.allitebooks.com/"]
 
  def parse(self, response):
    links = response.xpath('//a/@href').extract()
    base_url='http://file.allitebooks.com/'
    for i in links:
      if i.endswith('.pdf'):
        i = urlparse.urljoin(base_url, i)
        yield Request(i, callback=self.save_pdf)
    yield AllitbookItem(link=response.url)
    for link in links:
      if validators.url(link):
        yield Request(link)
        
  def save_pdf(self, response):
    path = response.url.split('/')[-1]
    with open(path, 'wb') as f:
      f.write(response.body)   