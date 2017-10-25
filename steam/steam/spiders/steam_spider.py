import logging
import re
from w3lib.url import canonicalize_url, url_query_cleaner
from scrapy.http import FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import ProductItem, ProductItemLoader

logger = logging.getLogger(__name__)


def load_product(response):
	logger.debug(f"Loading product at {response.url}.")
	loader = ProductItemLoader(item=ProductItem(), response=response)

	product = response.xpath('//div[@class="apphub_AppName"]/text()').extract()
	loader.add_value('product', product)

	details = response.css('.details_block').extract_first()
	try:
		details = details.split('<br>')

		for line in details:
			line = re.sub('<[^<]+?>', '', line)  # Remove tags.
			line = re.sub('[\r\t\n]', '', line).strip()
			for prop, name in [
				('Title:', 'title'),
				('Genre:', 'genre'),
				('Developer:', 'developer'),
				('Publisher:', 'publisher'),
				('Release Date:', 'release_date')
			]:
				if prop in line:
					item = line.replace(prop, '').strip()
					loader.add_value(name, item)
	except:
		pass


	rel_date = response.xpath('//div[@class="date"]/text()').extract()
	loader.add_value('rel_date', rel_date)

	price = response.css('.game_purchase_price ::text').extract_first()
	discount_price = price
	if not price:
		price = response.css('.discount_original_price ::text').extract_first()
		discount_price = response.css('.discount_final_price ::text').extract_first()
	loader.add_value('price', price)
	loader.add_value('discount_price', discount_price)

	loader.add_xpath(
		'metascore',
		'//div[@id="game_area_metascore"]/div[contains(@class, "score")]/text()')

	sentiment = response.css('.game_review_summary').xpath('../*[@itemprop="description"]/text()').extract()
	loader.add_value('sentiment', sentiment)

	n_reviews = response.xpath('//span[@class="responsive_hidden"]/text()').extract()
	loader.add_value('n_reviews', n_reviews)

	tags = response.xpath('//a[@class="app_tag"]/text()').extract()
	loader.add_value('tags', tags)

	early_access = response.css('.early_access_header')
	if early_access:
		loader.add_value('early_access', True)
	else:
		loader.add_value('early_access', False)

	return loader.load_item()


class steam_spider(CrawlSpider):
	name = "products"

	allowed_urls = ['http://store.steampowered.com/']
	start_urls = ['http://store.steampowered.com/search/?sort_by=Reviews_DESC']

	allowed_domains=["steampowered.com"]

	rules = [
        Rule(LinkExtractor(
                allow='/app/(.+)/',
                restrict_css='#search_result_container'),
                callback='parse_product'),
        Rule(LinkExtractor(
                allow='page=(\d+)',
                restrict_css='.search_pagination_right'))
		]

	def parse_product(self, response):
		logger.debug(f"Parsing production at {response.url}.")
		# Circumvent age selection form.
		if '/agecheck/app' in response.url:
			logger.debug(f"Form-type age check triggered for {response.url}.")

			form = response.css('#agegate_box form')

			action = form.xpath('@action').extract_first()
			name = form.xpath('input/@name').extract_first()
			value = form.xpath('input/@value').extract_first()

			formdata = {
				name: value,
				'ageDay': '4',
				'ageMonth': '8',
				'ageYear': '1980'
			}

			yield FormRequest(
				url=action,
				method='POST',
				formdata=formdata,
				callback=self.parse_product
			)

		else:
			yield load_product(response)
