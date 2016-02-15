# coding:utf-8
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import  Selector
from meizico.items import MeizicoItem
from scrapy import FormRequest,Request
import sys
import random
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware

reload(sys)
sys.setdefaultencoding('utf-8')

class MeizicoSpider(CrawlSpider):
	name = "meizi"
	allowed_domain = ['meizico.com']
	start_url = ['http://www.meizico.com/']

	def start_requests(self):
		yield FormRequest("http://www.meizico.com/",callback=self.parse_category)

	def parse_category(self, response):
		sel = Selector(response)
		category = sel.xpath('//div[@class = "header clearfix"]/div/ul/li/a//text()').extract()
		category_url = sel.xpath('//div[@class = "header clearfix"]/div/ul/li/a/@href').extract()
		menu_list = list()
		for i in range(len(category)):
			temp_menu = sel.xpath('//ul[@class="menu"]/li[%d]/ul/li/a//text()'%(i+1)).extract()
			
			if temp_menu:
				temp_menu_url = sel.xpath('//ul[@class="menu"]/li[%d]/ul/li/a/@href'%(i+1)).extract()
				temp_list = list()
				for j in range(len(temp_menu)):
					menu_list.append({"%s"%(temp_menu[j]):temp_menu_url[j]})
			else:
				menu_list.append({"%s"%(category[i]):category_url[i]})
		print menu_list		
		for menu in menu_list:
			for k,v in menu.items():
				yield Request(url= v, meta={'url': v, 'count':0},callback=self.parse_page)
	def parse_page(self,response):
		sel = Selector(response)
		girls_url = sel.xpath('//div[@class="pic"]/a/@href').extract() 
		if girls_url:
			for girl in girls_url:
				yield Request(url=girl, callback=self.parse_item)
			url = response.meta['url']
			page = response.meta['count']+1
			yield Request(url= url.encode('utf-8')+'/page/'+str(page),meta={'url':url, 'count':page},callback=self.parse_page)
		else:
			print('404 not found!')

	def parse_item(self,response):
		sel = Selector(response)
		name = sel.xpath('//title//text()').extract()
		imgs = sel.xpath('//div[@class="post-content"]/p/a/img/@src').extract()
		item = MeizicoItem()
		item['image_urls'] = imgs
		item['image_name'] = name
		return item		

