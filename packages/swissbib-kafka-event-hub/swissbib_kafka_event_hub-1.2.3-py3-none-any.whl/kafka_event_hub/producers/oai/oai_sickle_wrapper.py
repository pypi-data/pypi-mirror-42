# coding: utf-8


__author__ = 'swissbib - UB Basel, Switzerland, Guenter Hipler'
__copyright__ = "Copyright 2019, swissbib project"
__credits__ = []
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Guenter Hipler"
__email__ = "guenter.hipler@unibas.ch"
__status__ = "in development"
__description__ = """

                    """

from kafka_event_hub.config.content_collector_config import OAIConfig
from kafka_event_hub.utility.producer_utility import transform_from_until, is_detailed_granularity, \
                                                    calculate_day_delta_in_coarse_date
from sickle import Sickle
from sickle.oaiexceptions import OAIError, BadArgument, NoRecordsMatch
from logging import Logger


class OaiSickleWrapper(object):

    def __init__(self, configuration: type(OAIConfig),
                 summary_logger: Logger,
                 exception_logger: Logger):

        self._oaiconfig = configuration
        self._summary_logger = summary_logger
        self._exception_logger = exception_logger
        self._initialize()

    def _initialize(self):
        self.dic = {}

        if not self._oaiconfig.metadata_prefix is None:
            self.dic['metadataPrefix'] = self._oaiconfig.metadata_prefix
        if not self._oaiconfig.oai_set is None:
            self.dic['set'] = self._oaiconfig.oai_set
        if not self._oaiconfig.timestamp_utc is None:
            if is_detailed_granularity(self._oaiconfig.granularity):
                self.dic['from'] = transform_from_until(self._oaiconfig.timestamp_utc,
                                                   self._oaiconfig.granularity)
            else:
                self.dic['from'] = transform_from_until(calculate_day_delta_in_coarse_date(
                                                    self._oaiconfig.timestamp_utc, -1),
                                                    self._oaiconfig.granularity)
        if not self._oaiconfig.oai_until is None:
            self.dic['until'] = transform_from_until(self._oaiconfig.oai_until,
                                                self._oaiconfig.granularity)
        self.dic['verb'] = self._oaiconfig.oai_verb

        self._summary_logger.info('verwendete URL Adresse: {ADRESSE}?{PARAMS}'.format(
            ADRESSE=self._oaiconfig['OAI']['url'],
            PARAMS='&'.join('{}={}'.format(key, value) for key, value in self.dic.items())
        ))


    def fetch_iter(self):

        try:

            sickle = Sickle(self._oaiconfig['OAI']['url'])

            records_iter = sickle.ListRecords(
                **self.dic
            )

            for record in records_iter:
                yield record


        except BadArgument as ba:
            self._exception_logger.error("bad argument exception {EXCEPTION}".format(
                EXCEPTION=str(ba)
            ))
        except OAIError as oaiError:
            self._exception_logger.error("OAIError exception {EXCEPTION}".format(
                EXCEPTION=str(oaiError)
            ))
        except NoRecordsMatch as noRecordsmatch:
            self._summary_logger.error("no records matched {EXCEPTION}".format(
                EXCEPTION=str(noRecordsmatch)
            ))
        except Exception as baseException:
            self._summary_logger.error("base exception occured - not directly related to OAI {EXCEPTION}".format(
                EXCEPTION=str(baseException)
            ))
        else:
            print("oai fetching finished successfully")
            #todo: make better logging

