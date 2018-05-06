import scrapy
from items import ArticleItem
from datetime import datetime
import re
import time


class Rain(scrapy.Spider):
    name = "rain_scraper"

    start_urls = []

    # паттерн для страниц архива
    # если search_year, search_month, search_day =0, то поиск статей по всем возможным годам и тд
    url_pattern = "https://tvrain.ru/archive/?search_year=2018&search_month=5&search_day=0&query=&type=&tab=News&page="

    start_urls.append(url_pattern + str(1))

    # получаем количество доступных страниц
    def parse(self, response):
        N = [int(s.strip()) for s in response.xpath(
            "//a[contains(@class, 'pagination__item pagination__item--link')]/descendant::text()").extract()][-1]
        for i in range(1, N + 1):
            url = self.url_pattern + str(i)
            yield scrapy.Request(url, callback=self.parse_pages)

    # парсим страницы
    def parse_pages(self, response):
        for href in response.xpath(
                "//div[contains(@class, 'chrono_list__item__info')]/a[contains(@class, 'chrono_list__item__info__name chrono_list__item__info__name--nocursor')]//@href"):
            # add the scheme, eg http://
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_articles)

    # парсим статьи
    def parse_articles(self, response):
        if response.xpath("//div[@class = 'document-head__f1__l']/a/@href").extract()[0] == '/news/':
            item = ArticleItem()

            item['Title'] = " ".join(
                response.xpath("//div[contains(@class, 'document-head__title')]/descendant::text()").extract()).strip()

            item['Date'] = " ".join(
                response.xpath("//span[contains(@class, 'document-head__date')]/descendant::text()").extract()).strip()

            lead = " ".join(
                response.xpath("//div[contains(@class, 'document-lead')]/descendant::text()").extract()).strip()

            item['Text'] = lead + " ".join(response.xpath("//div[contains(@class, 'article-full__text')]").xpath(
                ".//p/descendant::text()").extract()).strip()

            # Url (The link to the page)
            item['url'] = response.xpath("//meta[@property='og:url']/@content").extract()[0]

            yield item