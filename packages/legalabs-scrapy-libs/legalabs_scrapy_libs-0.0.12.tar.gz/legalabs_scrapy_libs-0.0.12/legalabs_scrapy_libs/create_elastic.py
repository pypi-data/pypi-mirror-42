import os
import json
import pathlib
from datetime import datetime
from elasticsearch import helpers
from elasticsearch import Elasticsearch

host = os.environ.get('ELASTICSEARCH_HOST', 'juris.st.legalabs.com.br')
port = os.environ.get('ELASTICSEARCH_PORT', 9200)

es = Elasticsearch([{'host': host, 'port': port}], timeout=60*60)

mappings_prop = {
    "metadata.origem.estado": {
      "type": "keyword"
    },
    "metadata.origem.comarca": {
      "type": "keyword"
    },
    "metadata.tipo_decisao": {
      "type": "keyword"
    },
    "metadata.area_de_conhecimento": {
      "type": "keyword"
    },
    "metadata.assunto": {
      "type": "keyword"
    },
    "metadata.tribunal": {
      "type": "keyword"
    },
    "metadata.numero_processo.tribunal": {
      "type": "keyword"
    },
    "metadata.numero_processo.cnj": {
      "type": "keyword"
    },
    "metadata.numero_decisao": {
      "type": "keyword"
    },
    "metadata.classe_processual": {
      "type": "keyword"
    },
    "metadata.orgao_julgador": {
      "type": "keyword"
    },
    "metadata.numero_decisao": {
      "type": "keyword"
    },
    "metadata.numero_decisao": {
      "type": "keyword"
    },
    "metadata.data_julgamento": {
      "type": "date",
    },
    "metadata.data_publicacao": {
      "type": "date",
    },
    "metadata.anexo.url": {
      "type": "keyword"
    },
    "metadata.anexo.tipo": {
      "type": "keyword"
    },
    "metadata.anexo.nome": {
      "type": "keyword"
    },
    "metadata.notas": {
      "type": "text",
      "analyzer": "brazilian"
    },
    "metadata.provimento": {
      "type": "text",
      "analyzer": "brazilian"
    },
    "metadata.certidao_julgamento": {
      "type": "keyword"
    },
    "metadata.referencia_jurisprudencial": {
      "type": "text",
      "analyzer": "brazilian"
    },
    "metadata.referencia_legislativa": {
      "type": "text",
      "analyzer": "brazilian"
    },
    "metadata.relator.nome": {
      "type": "keyword"
    },
    "metadata.relator.cargo": {
      "type": "keyword"
    },
    "metadata.relator_para_acordao.nome": {
      "type": "keyword"
    },
    "metadata.relator_para_acordao.cargo": {
      "type": "keyword"
    },
    "metadata.comarca": {
      "type": "keyword"
    },
    "metadata.diario.nome": {
      "type": "keyword"
    },
    "metadata.diario.numero": {
      "type": "keyword"
    },
    "metadata.diario.instancia": {
      "type": "keyword"
    },
    "metadata.diario.comarca": {
      "type": "keyword"
    },
    "metadata.diario.nro_comarca": {
      "type": "keyword"
    },
    "metadata.polo.passivo.nome": {
      "type": "keyword"
    },
    "metadata.polo.passivo.advogados": {
      "type": "keyword"
    },
    "metadata.polo.ativo.nome": {
      "type": "keyword"
    },
    "metadata.polo.ativo.advogados": {
      "type": "keyword"
    },
    "body.ementa": {
      "type": "text",
      "analyzer": "brazilian"
    },
    "body.acordao": {
      "type": "text",
      "analyzer": "brazilian"
    },
    "body.inteiro_teor": {
      "type": "text",
      "analyzer": "brazilian"
    },
}

body = {
  "settings": {
    "index.mapping.total_fields.limit": 100000000,
    "number_of_shards": 6,
    "number_of_replicas": 0,
  },
  "mappings": {
      "_doc": {
          "properties": mappings_prop
      }
  }
}

indexName = 'decisao'
print(json.dumps(es.indices.delete(index=indexName, ignore=[400, 404]), indent=2))
print(json.dumps(es.indices.create(index=indexName, body=body, ignore=400), indent=2))

