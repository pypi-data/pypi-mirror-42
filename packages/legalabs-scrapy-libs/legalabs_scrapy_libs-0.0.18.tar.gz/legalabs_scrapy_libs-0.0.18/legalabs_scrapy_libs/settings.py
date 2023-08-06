# -*- coding: utf-8 -*-

# Scrapy settings for jurisprudencia project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import os

from datetime import datetime

AWS_BUCKET = os.getenv('AWS_BUCKET', 'legallabs-juris')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
SAVE_MODE = os.getenv('SAVE_MODE', 'S3').upper()
VALID_SAVE_MODES = ['s3', 'local', 'none']
ELASTICSEARCH_HOST = os.getenv(
    'ELASTICSEARCH_HOST',
    os.getenv('ELASTICSEARCH_SERVER', 'juris.st.legalabs.com.br')
)
ELASTICSEARCH_SERVER = ELASTICSEARCH_HOST
ELASTICSEARCH_PORT = 9200
ELASTICSEARCH_BUFFER_LENGTH = 500

# if AWS_ACCESS_KEY_ID is None:
    # raise Exception('Env. variable "AWS_ACCESS_KEY_ID" must be defined')

# if AWS_SECRET_ACCESS_KEY is None:
    # raise Exception('Env. variable "AWS_SECRET_ACCESS_KEY" must be defined')

# if SAVE_MODE.lower() not in VALID_SAVE_MODES:
    # raise Exception('Env. variable "SAVE_MODE" must be one of: [{}]'.format(
        # ', '.join('"{}"'.format(x.upper()) for x in VALID_SAVE_MODES)
    # ))

BOT_NAME = 'jurisprudencia'

SPIDER_MODULES = ['spiders']
NEWSPIDER_MODULE = 'spiders'

DATA_DIRECTORY = 'data'

RETRY_TIMES = 10

CRAWLER_DATE = datetime.now()
CRAWLER_DATE_LEN = 1

INSTANCIA = 0

LOG_LEVEL = 'INFO'

#FEED_FORMAT = 'json'
#FEED_URI = 'jurisprudencia.json'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'diario (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 20
CONCURRENT_REQUESTS_PER_DOMAIN=1000

#DOWNLOAD_DELAY = 3
#COOKIES_ENABLED = False
#TELNETCONSOLE_ENABLED = False

#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'jurisprudencia.middlewares.JurisprudenciaSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'jurisprudencia.middlewares.JurisprudenciaDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'scrapy_libs.pipelines.JurisprudenciaPipeline': 300,
   'scrapy_libs.pipelines.ElasticSearchPipeline': 305,
   'scrapy_libs.pipelines.JurisprudenciaOABPipeline': 310
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
