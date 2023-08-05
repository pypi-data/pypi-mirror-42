import json
import logging
import os
import sys
from confluent_kafka import Producer
from ..utils.filesystem import get_project_root



def delivery_callback(err, msg):
    if err:
        sys.stderr.write('%% Message failed delivery: %s\n' % err)
    else:
        pass
        sys.stderr.write('%% Message delivered to %s [%d] @ %o\n' %
                         (msg.topic(), msg.partition(), msg.offset()))


class ConfluentProducer:

    def __init__(self, *args, **kwargs):
        self.__servers = kwargs.pop('servers', None)
        self.topic = kwargs.pop('topic', None)
        self.security_protocol = kwargs.pop('security_protocol', 'plaintext')
        self.ssl_ca_location = kwargs.pop('ssl_ca_location','./configuration/cacert.pem')

        if not self.topic:
            sys.stderr.write('%% Topic name not specified: \n')
            raise ValueError("Topic name not specified")
        logging.basicConfig(
            format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
            level=logging.ERROR
        )
        logging.getLogger('kafka').setLevel(logging.INFO)
        conf = {'bootstrap.servers': self.__servers,
                'log.connection.close': 'false',
                'security.protocol': self.security_protocol,
                'ssl.ca.location': self.ssl_ca_location

                }

        # Create MsgProducer instance
        self.producer = Producer(**conf)

    def produce_message(self, **kwargs):
        message = kwargs.pop('message', None)
        try:
            self.producer.produce(self.topic, value=json.dumps(message), callback=delivery_callback)

        except BufferError as e:
            sys.stderr.write('%% Local producer queue is full ' \
                             '(%d messages awaiting delivery): try again\n' %
                             len(self.producer))
            return None
        self.producer.poll(0)
        self.producer.flush()
        return {"topic": self.topic, "sent": True}
