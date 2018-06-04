import scrapy

from ..database import Database
from ..items import ForumMessageItem


class MessageSpider(scrapy.Spider):
    name = "messages"

    def start_requests(self):
        db = Database()
        urls = [topic['url'] for topic in db.get_topics()]
        db.close()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for message in response.css('div.inner'):
            item = ForumMessageItem()
            text = str(message.css('div.content::text').extract_first()).strip()
            item['text'] = "" if text == "None" else text
            item['author'] = str(message.css('p.author strong a::text').extract_first()).strip()
            item['date_time'] = str(message.css('p.author::text').extract()[1]).strip()[7:]
            item['topic_url'] = str(response)[5:len(str(response)) - 1]

            yield item

        next_page = response.css('a.right-box.right::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

