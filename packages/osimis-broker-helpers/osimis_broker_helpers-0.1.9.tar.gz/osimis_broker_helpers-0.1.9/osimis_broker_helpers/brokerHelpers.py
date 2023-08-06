from osimis_broker_helpers.exceptions import *
import typing
import pika
import threading
from osimis_logging import LogHelpers
import datetime

"""
Helpers for automatic retry/requeue.
"""

class BrokerHelpers:
    """
    This is only an abstract class and shouldn't be used as it.
    """
    def __init__(self, hostname: str,
                 login: str,
                 password: str,
                 port: int = 5672,
                 logger = LogHelpers.getNullLogger()
                 ):
        '''
        :param hostname: hostname of the rabbitmq broker
        :param login: login of the rabbitmq broker
        :param password: password of the rabbitmq broker
        '''

        self._hostname = hostname
        self._port = port
        self._login = login
        self._password = password
        self._logger = logger

    def _connect(self) -> pika.channel.Channel:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host = self._hostname,
                port = self._port,
                credentials = pika.PlainCredentials(username = self._login, password = self._password)
            ))
        except Exception as ex:
            self._logger.error("Unable to connect to Rabbitmq, exception: " + str(ex))
            raise Exception("Unable to connect to Rabbitmq, inner exception: " + str(ex))
        return connection.channel()

    def _disconnect(self, channel: pika.channel.Channel):
        channel.close()
        channel.connection.close()

class ProducerHelper(BrokerHelpers):
    """
    This has to be instantiated in producer side : where messages are produced.
    """

    def __init__(self, exchangeName: str,
                 hostname: str,
                 port: int = 5672,
                 login: str = "rabbit",
                 password: str = "123456",
                 logger = LogHelpers.getNullLogger()
                 ):
        """

        :param exchangeName: name of the exchange, consumer(s) will have to be aware of that name
        :param hostname: hostname of the rabbitmq service
        :param port : port used by rabbitmq
        :param login: rabbitmq login
        :param password: rabbitmq password
        """
        super().__init__(hostname = hostname, port = port, login = login, password = password, logger = logger)
        self._exchangeName = exchangeName

    def configure(self):
        """
        This will create and configure the Exchange dedicated to the reception
        of messages sent by the producer.
        E.g: a Lify study ID is sent by the forwarder to this exchange in order to be
        processed by some services like SMS sender, hl7 client,...
        :return:
        """
        self._logger.info("Configuring producer...")
        channel = self._connect()
        channel.exchange_declare(exchange = self._exchangeName, exchange_type = 'fanout')
        self._disconnect(channel)
        self._logger.info("Configured producer.")


    def pushMessageToProducerExchange(self, message: str):
        """
        Push the message in the broker (to the producer exchange).
        Just push the message and forget it, if rabbitmq container has a volume binded, message
        will be persistent and so processed.
        :param message: the message to push
        :return:
        """

        self._logger.info("Pushing message to broker...")
        self._logger.debug("Message : {msg}".format(msg = str(message)))
        channel = self._connect()
        channel.basic_publish(exchange = self._exchangeName,
                              routing_key = '',
                              body = message,
                              properties = pika.BasicProperties(
                                  delivery_mode = 2,  # make message persistent
                              )
                              )
        self._disconnect(channel)


class ConsumerHelper(BrokerHelpers):
    """
    This has to be instantiated in consumer side : where messages are processed.
    Several consumers can be created, the 'queueName' has to be unique for each one.
    """
    def __init__(self, producerExchangeName: str,
                 queueName: str,
                 hostname: str,
                 callbackMethod,
                 port: int = 5672,
                 login: str = "rabbit",
                 password: str = "123456",
                 retryPeriod: int = 60,
                 lifetime: int = 86400, # default = one day
                 logger = LogHelpers.getNullLogger()
                 ):
        """

        :param producerExchangeName: The name of the exchange to bind the consumer (queue) to (has to be the same
        than the one defined in the producer service)
        :param queueName: name of the Queue which will be binded to exchange. Has to be unique in regards of queues from
        other services dealing with the same producer exchange.
        :param hostname: rabbitmq hostname
        :param port : port used by rabbitmq
        :param callback: the method which will be called for each received message
        method signature : callback(message: str)
        method return : true if message has been succesfully processed and/or message has to be removed from the queue;
        false if not (and so message has to be requeued and processed again later on)
        :param login: rabbitmq hostname
        :param password: rabbitmq password
        :param retryPeriod: in s, interval between 2 retries
        :param lifetime: in s, if this period is elapsed, message is deleted (avoid infinitely retries)
        use expiredMessageHandler to be aware of deleted messages


        """
        super().__init__(hostname = hostname, port = port, login = login, password = password, logger = logger)
        self._producerExchangeName = producerExchangeName
        self._queueName = queueName
        self._retryPeriod = retryPeriod
        self._lifetime = lifetime
        self._callbackMethod = callbackMethod

        self._consumingThread = None
        self._consumingChannel = None

        self.expiredMessageHandler = None

    def configure(self):
        """
        This will create and configure the queue (and extra exchanges/queues)
        dedicated to the reception and consuming of messages arriving in broker.

        :return:
        """
        dlxExchangeName = "dlX_" + self._queueName
        dlxQueueName = "waitingQ_" + self._queueName
        retryExchangeName = "retryX_" + self._queueName

        self._logger.info("Configuring consumer...")

        # Connection to rabbitMQ
        channel = self._connect()

        # Producer exchange creation (it should have been created in the producer service,
        # but pika is smart, so exchange will only be created if not existing)
        channel.exchange_declare(exchange = self._producerExchangeName, exchange_type = 'fanout')

        # Queue creation (bound to producer exchange)
        channel.queue_declare(
            queue = self._queueName,
            durable = True,
            arguments = {
                'x-dead-letter-exchange': dlxExchangeName
            }
        )
        channel.queue_bind(exchange = self._producerExchangeName, queue = self._queueName)

        # dead letter exchange creation (allows to retry)
        channel.exchange_declare(exchange = dlxExchangeName, exchange_type = 'fanout')

        # dead letter queue creation (allows to wait before retry)
        channel.queue_declare(
            queue = dlxQueueName,
            durable = True,
            arguments = {
                'x-message-ttl': self._retryPeriod*1000,  # message will go back to main queue (for retry) after this perdiod (default:60 000 ms)
                'x-dead-letter-exchange': retryExchangeName
            }
        )
        channel.queue_bind(exchange = dlxExchangeName, queue = dlxQueueName)

        # retry exchange creation
        # this exchange will receive rejected message after wait period (from dlxQueueName)
        # and post it again in the work queue (queueName)
        channel.exchange_declare(exchange = retryExchangeName, exchange_type = 'fanout')
        channel.queue_bind(exchange = retryExchangeName, queue = self._queueName)

        self._disconnect(channel)
        self._logger.info("Configured consumer.")


    def startConsuming(self):
        """
        Starts the consuming : will wait for messages arriving in the broker and process
        them.

        When a message is received, the _callbackMethod is called.
        If this method returns True, message is discarded.
        If this method returns False, message is requeue and processed later on (depending
        on _retryPeriod).

        When time elapsed between first processing try and last processing try is bigger than
        lifetime, the message is discarded and expiredMessageHandler is called (if it exists).

        This method never exits (use aSyncStartConsuming for threading).
        :return:
        """

        self._logger.info("Start consuming...")

        self._consumingChannel = self._connect()

        self._consumingChannel.basic_consume(self._callback,
                                queue = self._queueName,
                                consumer_tag = self._queueName
                              )
        self._consumingChannel.start_consuming()  # this method never exits

        self._disconnect(self._consumingChannel)

    def aSyncStartConsuming(self):
        """
        Starts the consuming : will wait for messages arriving in the broker and process
        them.

        When a message is received, the _callbackMethod is called.
        If this method returns True, message is discarded.
        If this method returns False, message is requeue and processed later on (depending
        on _retryPeriod).

        When time elapsed between first processing try and last processing try is bigger than
        lifetime, the message is discarded and expiredMessageHandler is called (if it exists).

        :return:
        """
        # create thread
        self._consumingThread = threading.Thread(
            target = self.startConsuming,
            name = 'Consuming Thread'
        )

        # start thread
        self._consumingThread.start()

    def stopConsuming(self):
        """
        If consuming has been started by aSyncStartConsuming, this method allows to
        stop the consuming.
        :return:
        """
        self._logger.info("Stopping consuming...")
        self._consumingChannel.stop_consuming(consumer_tag = self._queueName)
        self._disconnect(self._consumingChannel)

    def _callback(self, ch, method, properties, body):
        # check lifetime
        if properties.headers:
            firstTry = properties.headers['x-death'][0]['time']
            delta = datetime.datetime.now() - firstTry
            if delta.total_seconds() >= self._lifetime:
                self._logger.info("Message expired!")
                ch.basic_ack(delivery_tag = method.delivery_tag)
                if self.expiredMessageHandler is not None:
                    self.expiredMessageHandler(body)
                return

        result = self._callbackMethod(body)
        if result:
            self._logger.debug("Sending ack...")
            ch.basic_ack(delivery_tag = method.delivery_tag)
        else:
            self._logger.debug("Sending Nack...")
            ch.basic_reject(delivery_tag = method.delivery_tag, requeue = False)