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

try:
    from scrapy_libs.items import decisao_validator
except:
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
        if item.get('index') != 'decisao':
            return item
        validation = self.validate(item)
        if validation['status'] is False:
            # Make body strings less verbose
            max_length = 40
            if 'body' in item:
                body = item['body']
                for key, value in list(body.items()):
                    if type(value) == str and len(value) > max_length:
                        body[key] = value[:max(1, max_length - 3)] + '...'
            raise DropItem(validation['message'])
        item = self.normalize(item)
        item['_created'] = datetime.now().isoformat()
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

    def index_item(self, item, logger=None):
        if item.get('index') != 'decisao':
            return

        metadata = item['metadata']
        body = item.get('body', {})
        drop_reasons = []

        numero_cnj = None

        if 'numero_processo' in metadata and 'cnj' in metadata['numero_processo']:
            numero_cnj = metadata['numero_processo']['cnj']

        tipo_decisao_value = 'acórdão'

        if 'tipo_decisao' not in metadata or metadata['tipo_decisao'] != tipo_decisao_value:
            drop_reasons.append('Field "metadata.tipo_decisao" is not "{}"'.format(tipo_decisao_value))

        if not metadata['tem_anexo']:
            drop_reasons.append('Field "metadata.tem_anexo" is not True')

        if 'anexo' not in metadata or 'tipo' not in metadata['anexo'] or metadata['anexo']['tipo'] != 'pdf':
            drop_reasons.append('Field "metadata.anexo.tipo" is not "pdf"')

        min_length = 10

        for field in ['ementa', 'acordao', 'inteiro_teor']:
            if field in body and len(body[field]) < min_length:
                drop_reasons.append('Field "body.{}" is too short (min length: {})'.format(field, min_length))

        if len(drop_reasons) > 0:
            if logger is not None:
                logger.warn('Dropping OAB {} - {}{}, reason: {}'.format(
                    item['id'], metadata['data_publicacao'],
                    (' - ' + numero_cnj) if numero_cnj is not None else '',
                    '; '.join(drop_reasons)
                ))
            return

        cargo = metadata['relator']['cargo'].replace('Desembargador(a)', 'Des.').replace('Ministro(a)', 'Min.')
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

        if numero_cnj is not None:
            converted['metadata']['numero_cnj'] = numero_cnj

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
            self.index_item(item, spider.logger)
            logging.debug('Item sent to OAB Elastic Search')
        return item

    def close_spider(self, spider):
        if len(self.items_buffer):
            self.send_items()
