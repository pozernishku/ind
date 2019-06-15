# -*- coding: utf-8 -*-
import scrapy


class IndSpSpider(scrapy.Spider):
    name = 'ind_sp'
    allowed_domains = ['fcainfoweb.nic.in']
    start_urls = ['https://fcainfoweb.nic.in/']

    def parse(self, response):
        pass
