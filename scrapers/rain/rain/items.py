# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class RainItem(scrapy.Item):
	Title = scrapy.Field()
	Date = scrapy.Field()
	Lead = scrapy.Field() # превью статьи, в базе объединяется с основным текстом
	Text = scrapy.Field()
	url = scrapy.Field()
