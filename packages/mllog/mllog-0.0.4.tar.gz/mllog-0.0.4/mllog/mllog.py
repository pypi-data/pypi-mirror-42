from kafka import KafkaProducer
from kafka.errors import KafkaError
import logging


class MLLog:

    def __init__(self, ip, port, queue):
        self.ip = ip
        self.port = port
        self.queue = queue

    def write(self, key, value):
        try:
            logger = logging.getLogger()
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)

            producer = KafkaProducer(bootstrap_servers=[self.ip + ':' + self.port])
            future = producer.send(self.queue, key=bytes(key.encode('utf-8')),
                                   value=bytes(value.encode('utf-8')), partition=0)
            result = future.get(timeout=10)
            logger.info(result)
        except KafkaError:
            logger.exception()
            pass


if __name__ == '__main__':
    log = MLLog('localhost', '9092', 'test')
    log.write("name", "kafka-a")
