# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from datetime import datetime, date
import logging
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, MapCompose, TakeFirst, Join

logger = logging.getLogger(__name__)

class StripText:
	def __init__(self, chars = '\r\t\n'):
		self.chars = chars

	def __call__(self, value):
		try:
			return value.strip(self.chars)
		except:
			return value

def standardize_date(x):
    """
    Convert x from recognized input formats to desired output format,
    or leave unchanged if input format is not recognized.
    """
    fmt_fail = False

    for fmt in ["%b %d, %Y", "%B %d, %Y"]:
        try:
            return datetime.strptime(x, fmt).strftime("%Y-%m-%d")
        except ValueError:
            fmt_fail = True

    # Induce year to current year if it is missing.
    for fmt in ["%b %d", "%B %d"]:
        try:
            d = datetime.strptime(x, fmt)
            d = d.replace(year=date.today().year)
            return d.strftime("%Y-%m-%d")
        except ValueError:
            fmt_fail = True

    if fmt_fail:
        logger.debug(f"Could not process date {x}")

        return x

def str_to_int(x):
	x = x.replace(',', '')
	try:
		return int(x)
	except:
		return x

def str_to_float(x):
	x = x.replace(',', '')
	try:
		return float(x)
	except:
		return x




class ProductItem(scrapy.Item):
    # define the fields for your item here like:
    product = scrapy.Field()
    rel_date = scrapy.Field()

    title = scrapy.Field()
    genre = scrapy.Field(
        output_processor=Compose(TakeFirst(),
            lambda x:x.split(','),
            MapCompose(StripText()
            )
        )
    )
    developer = scrapy.Field()
    publisher = scrapy.Field()
    release_date = scrapy.Field(output_processor=Compose(TakeFirst(), StripText(), standardize_date)
    )
    price = scrapy.Field(
    	output_processor=Compose(TakeFirst(),
    			StripText(chars = '$\n\t\r'),
    			str_to_float)
    )
    discount_price = scrapy.Field(
    	output_processor=Compose(TakeFirst(),
    			StripText(chars = '$\n\t\r'),
    			str_to_float)
    )
    sentiment = scrapy.Field()
    n_reviews = scrapy.Field(
    	output_processor=Compose(
    		MapCompose(
    			StripText(),
    			lambda x:x.replace(",", ""),
    			str_to_int),
    		max
    	)
    )
    tags = scrapy.Field(
    	output_processor=Compose(
    		MapCompose(
    			StripText()
    		)
    	)
    )


    metascore = scrapy.Field(
        output_processor=Compose(TakeFirst(),
                    StripText(),
                    str_to_int
                )
    )
    early_access = scrapy.Field()

    metascore = scrapy.Field(
        output_processor=Compose(
            TakeFirst(), StripText(), 
            str_to_int)
    )


class ProductItemLoader(ItemLoader):
    default_output_processor=Compose(TakeFirst(), StripText())
