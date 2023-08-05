# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import hashlib
import json
import types
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
from six import string_types
from scrapy.exceptions import DropItem
from pprint import pprint
from legalabs_scrapy_libs.items import decisao_validator

class JurisprudenciaPipeline(object):
    def validate(self, item):
        valid = decisao_validator.validate(item)

        if not valid:
            return {'status': False, 'message': decisao_validator.errors}

        return {'status': True}

    def normalize(self, item):
        return decisao_validator.normalized(item)

    def process_item(self, item, spider):
        if item.get('index')!='decisao':
            return item
        validation = self.validate(item)
        if validation['status'] is False:
            del item['body']
            raise DropItem(validation['message'])
        item = self.normalize(item)
        return item

class ElasticSearchPipeline(object):
    settings = None
    es = None
    items_buffer = []

    @classmethod
    def init_es_client(cls, crawler_settings):
        es = Elasticsearch([{'host': crawler_settings.get('ELASTICSEARCH_SERVER'),
                             'port': crawler_settings.get('ELASTICSEARCH_PORT')}],
                             timeout=5)
        return es

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        ext.settings = crawler.settings
        ext.es = cls.init_es_client(crawler.settings)
        return ext

    def index_item(self, item):
        item_ = json.loads(json.dumps(item))
        _id = item_.pop('id')
        _index = item_.pop('index')
        index_action = {
            '_index': _index,
            '_type': '_doc',
            '_id': _id,
            '_source': item_
        }

        self.items_buffer.append(index_action)
        if len(self.items_buffer) >= self.settings.get('ELASTICSEARCH_BUFFER_LENGTH', 100):
            self.send_items()
            self.items_buffer = []

    def send_items(self):
        helpers.bulk(self.es, self.items_buffer)

    def process_item(self, item, spider):
        if item:
            self.index_item(item)
            logging.debug('Item sent to Elastic Search')
        return item

    def close_spider(self, spider):
        if len(self.items_buffer):
            self.send_items()

class JurisprudenciaOABPipeline(object):
    settings = None
    es = None
    items_buffer = []

    @classmethod
    def init_es_client(cls, crawler_settings):
        es = Elasticsearch([{'host': crawler_settings.get('ELASTICSEARCH_SERVER'),
                             'port': crawler_settings.get('ELASTICSEARCH_PORT')}],
                             timeout=5)
        return es

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        ext.settings = crawler.settings
        ext.es = cls.init_es_client(crawler.settings)
        return ext

    def index_item(self, item):
        if item.get('index') != 'decisao':
            return

        metadata = item['metadata']
        if not(metadata['tipo_decisao'] == 'acórdão' and metadata['tem_anexo'] and metadata['anexo']['tipo']=='pdf'):
            print("Droping OAB")
            print(metadata)
            return

        cargo = metadata['relator']['cargo'].replace('Desembargador(a)','Des.').replace('Ministro(a)','Min.')
        converted = {
            'metadata': {
                'tipo': metadata['tipo_decisao'].capitalize(),
                'tribunal': metadata['tribunal'],
                'data_julgamento': metadata['data_julgamento'],
                'diario': {
                    'data_publicacao': metadata['data_publicacao'],
                },
                'relator': {
                    'identificador': f"{cargo} {metadata['relator']['nome']}",
                },
                'orgao_julgador': metadata['orgao_julgador'],
                'identificador_processo': metadata['numero_decisao'],
                'area_de_conhecimento': metadata.get('area_de_conhecimento', ['Variados'])
            },
            'body': {
                'ementa': item['body']['ementa'],
            }
        }
        if 'origem' in metadata and 'estado' in metadata['origem']:
            converted['metadata']['origem'] = {
                'estado': metadata['origem']['estado']
            }

        _id = item['id']
        index_action = {
            '_index': 'juris',
            '_type': '_doc',
            '_id': _id,
            '_source': converted
        }

        self.items_buffer.append(index_action)
        if len(self.items_buffer) >= self.settings.get('ELASTICSEARCH_BUFFER_LENGTH', 100):
            self.send_items()
            self.items_buffer = []

    def send_items(self):
        helpers.bulk(self.es, self.items_buffer)

    def process_item(self, item, spider):
        if item:
            self.index_item(item)
            logging.debug('Item sent to OAB Elastic Search')
        return item

    def close_spider(self, spider):
        if len(self.items_buffer):
            self.send_items()
