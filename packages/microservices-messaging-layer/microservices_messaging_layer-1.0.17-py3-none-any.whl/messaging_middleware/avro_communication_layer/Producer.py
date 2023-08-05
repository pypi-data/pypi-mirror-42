from confluent_kafka.avro import AvroProducer
from avro import schema
import sys, requests


def delivery_callback(err, msg):
    if err:
        sys.stderr.write('%% Message failed delivery: %s\n' % err)
    else:
        sys.stderr.write('%% Message delivered to %s [%d]\n' % \
                         (msg.topic(), msg.partition()))


def find_latest_schema(topic,SCHEMA_REGISTRY_URL):
    subject = topic
    versions_response = requests.get(
        url="{}/subjects/{}/versions".format(SCHEMA_REGISTRY_URL, subject),
        headers={
            "Content-Type": "application/vnd.schemaregistry.v1+json",
        },
    )
    #print("versions_response.json()=", versions_response.json())
    latest_version = versions_response.json()[-1]
    #print("latest_version=", latest_version)
    schema_response = requests.get(
        url="{}/subjects/{}/versions/{}".format(SCHEMA_REGISTRY_URL, subject, latest_version),
        headers={
            "Content-Type": "application/vnd.schemaregistry.v1+json",
        },
    )
    #print("schema_response.json()=", schema_response.json())
    schema_response_json = schema_response.json()

    return schema_response_json["id"], schema.Parse(schema_response_json["schema"])


class Producer:
    """
            Avro Producer
            It needs the following kargs
                - bootstrap_servers
                - schema_reqistry_url
                - topic


    """

    def __init__(self, *args, **kwargs):

        self.__servers = kwargs.pop('bootstrap_servers', None)
        self.__registry = kwargs.pop('schema_reqistry_url', None)
        self.topic = kwargs.pop('topic', None)
        self.security_protocol = kwargs.pop('security_protocol', 'plaintext')
        self.ssl_ca_location = kwargs.pop('ssl_ca_location','./configuration/cacert.pem')

        self.debug_level = kwargs.pop('debug_level', 'security')
        if not self.topic:
            sys.stderr.write('%% Topic name not specified: \n')
            raise ValueError("Topic name not specified")

        schema_id, default_value_schema = find_latest_schema(self.topic+"-value",self.__registry)
        schema_id, default_key_schema = find_latest_schema(self.topic+"-key",self.__registry)

        #print("default_value_schema=",default_value_schema)
        #print("default_key_schema=",default_key_schema)

        self.default_value_schema = default_value_schema
        self.producer = AvroProducer({'bootstrap.servers': self.__servers,
                                      'schema.registry.url': self.__registry,
                                      'log.connection.close':'false',
                                      'security.protocol': self.security_protocol,
                                      'ssl.ca.location': self.ssl_ca_location
                                      },
                                     default_key_schema=default_key_schema, default_value_schema=default_value_schema)

    def produce_message(self, **kwargs):

        """
            Sends message to kafka by encoding with specified avro schema
                @:param: topic: topic name
                @:param: value: An object to serialize
                @:param: key: An object to serialize
        """

        # get schemas from  kwargs if defined
        callback_function = kwargs.pop('delivery_callback', delivery_callback)
        value = kwargs.pop('value', None)
        key = kwargs.pop('key', None)
        try:
            self.producer.produce(topic=self.topic, value=value, key=key, callback=callback_function)

        except BufferError as e:
            sys.stderr.write('%% Local producer queue is full ' \
                             '(%d messages awaiting delivery): try again\n' %
                             len(self.producer))
            return None
        self.producer.poll(0)
        self.producer.flush()
        return {"topic": self.topic, "value": value, "sent": True}