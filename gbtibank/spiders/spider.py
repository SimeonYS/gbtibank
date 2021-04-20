import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import GgbtibankItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class GgbtibankSpider(scrapy.Spider):
	name = 'gbtibank'
	start_urls = ['https://www.gbtibank.com/about-us/media-center/']

	def parse(self, response):
		post_links = response.xpath('//a[@title="Read more"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//abbr[@class="published"]/text()').get()
		title = response.xpath('//h2/text()').get()
		content = response.xpath('//div[@class="cmsmasters_post_content entry-content"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=GgbtibankItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
