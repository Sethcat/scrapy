# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem

class MeizicoPipeline(ImagesPipeline):
   # def process_item(self, item, spider):
   #     return item
    def get_media_request(self, item, info):
    	for image_url in item['image_urls']:
    		yield scrapy.Request(image_url)
    def item_completed(self, results, item, info):
    	image_path = [x['path'] for ok, x in results if ok]
    	if not image_path:
    		raise DropItem("Item no images")
    	item['image_paths'] = image_path
    	return item
    def file_path(self, request, response=None, info=None):
        open("image_urls.txt","a").write(request.url + "\n")
        image_guid = request.url.split('/')[-1]
        return 'full/%s' % (image_guid)