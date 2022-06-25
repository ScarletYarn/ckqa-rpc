# -*- coding: utf-8 -*-
from elasticsearch7 import Elasticsearch


class ES:
    def __init__(self):
        self.es = Elasticsearch(hosts='http://192.168.10.162:9200')

    def query(self, entity, index='cskg_vector_new_purge', size=3000):
        resp = self.es.search(index=index, size=size, query={
            'bool': {
                'should': [
                    {
                        'match': {
                            'subject': entity
                        }
                    },
                    {
                        'match': {
                            'object': entity
                        }
                    }
                ]
            }
        })
        return [
            [
                i['_source']['subject'],
                i['_source']['relation'],
                i['_source']['object']
            ] for i in resp['hits']['hits']
        ]
