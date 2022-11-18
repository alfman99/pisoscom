# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# To index data in Elasticsearch
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from elasticsearch_dsl import Index, analyzer, tokenizer


class PisosPipeline:
    def __init__(self):
        self.elastic_uri = 'http://localhost:9200/'
        self.elastic_db = 'pisoscom'

    def process_item(self, item, spider):
        return item

    def open_spider(self, spider):
        self.client = Elasticsearch()
        try:
            # Drop index if it exists
            ind = Index(self.elastic_db, using=self.client)
            ind.delete()
        except NotFoundError:
            pass
        # then create it
        ind.create()
        ind.close()
        # Configure tokenizer
        my_analyzer = analyzer('default', type='custom',
            tokenizer=tokenizer('standard'),
            filter=['lowercase', 'asciifolding'])
        ind.analyzer(my_analyzer)
        ind.save()
        ind.open()

    def close_spider(self, spider):
        self.client.close()

    # Index data in Elasticsearch
    def process_item(self, item, spider):
        self.client.index(index=self.elastic_db, doc_type='PISO', body=dict(item))

        return item
