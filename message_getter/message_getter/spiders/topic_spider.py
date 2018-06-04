import scrapy

from ..items import ForumTopicItem


class TopicSpider(scrapy.Spider):
    name = "topics"
    start_urls = [
        'https://www.talkhealthpartnership.com/forum/viewforum.php?f=171'
    ]

    def parse(self, response):
        for topic in response.css("dl.icon"):
            if int(topic.css('dd.posts::text').extract_first()) > 0:
                item = ForumTopicItem()
                item['name'] = str(topic.css('a.topictitle::text').extract_first()).strip()
                item['url'] = 'https://www.talkhealthpartnership.com/forum' + str(topic.css('a.topictitle::attr(href)').extract_first()).strip()[1:]
                yield item

        next_page = response.css('a.right-box.right::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

