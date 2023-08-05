from kafka_event_hub.producers.base_producer import AbstractBaseProducer
from kafka_event_hub.config import BaseConfig

import requests
import json


class SRUProducer(AbstractBaseProducer):
    """

    """
    _domain = 'http://sru.swissbib.ch/sru/search/'

    _schemas = {
        'marc/xml': 'info:sru/schema/1/marcxml-v1.1-light',
        'dc/xml': 'info:sru/schema/1/dc-v1.1-light',
        'marc/json': 'info:sru/schema/json'
    }

    def __init__(self, configuration: str):
        super().__init__(configuration, BaseConfig)
        self._search = list()
        self._db = self.configuration['SRU']['database']
        self._schema = self._schemas[self.configuration['SRU']['schema']]
        self._max_records = self.configuration['SRU']['max_records']
        self._query = ''
        self._record_count = 0

    def _params(self, start_record):
        return {
            'query': self._query,
            'operation': 'searchRetrieve',
            'recordSchema': self._schema,
            'maximumRecords': self._max_records,
            'startRecord': start_record,
            'recordPacking': 'XML',
            'availableDBs': self._db
        }

    def add_simple_and_query(self, name, relation, value):
        if self._query == '':
            self._query = '{} {} {}'.format(name, relation, value)
        else:
            self._query = '{} AND {} {} {}'.format(self._query, name, relation, value)

    def set_simple_query(self, name, relation, value):
        self._query = '{} {} {}'.format(name, relation, value)

    def set_query_id_equal_with(self, value):
        self.set_simple_query('dc.id', '=', value)

    def set_query_anywhere_equal_with(self, value):
        self.set_simple_query('dc.anywhere', '=', value)

    def process(self):
        """Load all MARC JSON records from SRU with the given query into Kafka"""
        response = requests.get(self._domain + self._db, params=self._params(0))
        if response.ok:
            records = json.loads(response.text)
            self._record_count += len(records['collection'])
            if len(records['collection']) == 0:
                self._error_logger.info('No messages were found with query: %s', self._query)
            else:
                self._error_logger.info('%s messages were indexed with query: %s', self._query)
                for record in records['collection']:
                    self.send(record['fields'][0]['001'].encode('utf-8'),
                              json.dumps(record, ensure_ascii=False).encode('utf-8'))
            while int(records['numberOfRecords']) > self._record_count:
                response = requests.get(self._domain + self._db,
                                        params=self._params(int(records['startRecord']) + len(records['collection'])))
                if response.ok:
                    records = json.loads(response.text)
                    if len(records['collection']) == 0:
                        self._error_logger.info('No messages were found with query: %s', self._query)
                    else:
                        self._error_logger.info('%s messages were indexed with query: %s', self._query)
                        for record in records['collection']:
                            self.send(record['fields'][0]['001'].encode('utf-8'),
                                      json.dumps(record, ensure_ascii=False).encode('utf-8'))
                else:
                    self._error_logger.error('Could not connect to sru with status code %s. Because of: %s',
                                             response.status_code, response.text)
        else:
            self._error_logger.error('Could not connect to sru with status code %s. Because of: %s',
                                     response.status_code, response.text)

        self.flush()
        self.close()










