import os
import gzip
import bz2

from typing import TextIO, List

from kafka_event_hub.producers.base_producer import AbstractBaseProducer
from kafka_event_hub.config import LineProducerConfig


class LineProducer(AbstractBaseProducer):
    """
    Reads a text file or a directory of text files and sends each line as a message into kafka.
    The key is the line count across all files.

    Can handle gzip and bz2 compressed files.
    """

    def __init__(self, config: str):
        super().__init__(config, config_parser=LineProducerConfig)
        self.count = 0

    def process(self):
        path = self.configuration.path
        if not os.path.exists(path):
            self.close()
            raise FileNotFoundError("Path {} does not exist".format(path))
        else:
            paths: List[str] = []
            if os.path.isdir(path):
                for root, _, files in os.walk(path):
                    paths.extend(root + files)
            else:
                paths.append(path)
   
            for path in paths:
                fp = self._read_file(path)
                self._send_lines(fp)
                fp.close()

        self._time_logger.info("Producer published %s messages to topic %s.", self.count, self.configuration.topic['name'])

        self.flush()
        self.close()

    @staticmethod
    def _read_file(path: str) -> TextIO:
        if path.endswith('.gz'):
            return gzip.open(path, mode='r')
        elif path.endswith('.bz2'):
            return bz2.open(path, mode='r')
        else:
            return open(path, 'r')

    def _send_lines(self, fp: TextIO):
        for line in fp:
            if isinstance(line, bytes):
                line = line.decode('utf-8')
            line = line.strip()
            # self._error_logger.debug("Produced Message %s from Line: %s", self.count, line)
            self.send('{}'.format(self.count).encode('utf8'), line.encode('utf-8'))
            self.count += 1
