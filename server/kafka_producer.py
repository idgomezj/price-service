from confluent_kafka import Producer, Consumer, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic
import logging
import json
from config import Config


class KafkaProducer():
    def __init__(self, config:Config, topic: str) -> None:
        self._config = config
        self._topic = topic
        self._thread_index = None
        self._logger = logging.getLogger(self.__class__.__name__)
        

        try:
            self._logger.info("Setting up Kafka Producer ")
            self._producer = Producer({'bootstrap.servers': config.KAFKA_BROKER})

            # Initialize AdminClient for topic creation
            self._admin_client = AdminClient({'bootstrap.servers': config.KAFKA_BROKER})

            # Check if the topic exists, and create it if it doesn't
            self._logger.info("Checking if the Kafka topic exists... ")
            self.create_topic_if_not_exists(
                self._topic, 
                num_partitions=self._config.KAFKA_NUM_PARTITIONS, 
                replication_factor=self._config.KAFKA_REPLICATION_FACTOR,
                retention_ms=self._config.KAFKA_RETENTION_MS,
                cleanup_policy=self._config.KAFKA_CLEANUP_POLICY,
                compression_type=self._config.KAFKA_COMPRESSION_TYPE,
                min_insync_replicas=self._config.KAFKA_MIN_INSYNC_REPLICAS,
            )

            self._logger.info("Setting up Kafka Consumer ")
            self._consumer = Consumer({
                'bootstrap.servers': self._config.KAFKA_BROKER,
                'group.id': self._topic,
                'auto.offset.reset': 'earliest',
                'enable.auto.commit': False  # Disable auto-commit to control the offset manually
            })
        except KafkaError as e:
            self._logger.critical(f"Unable to connect to Kafka broker : {e}")
            raise
        except Exception as e:
            self._logger.critical(f"An error occurred during Kafka setup : {e}")
            raise


        self._logger.info(f"Kafka setup complete with topic {self._topic} ")

    def set_thread(self, thread_index: int): self._thread_index = thread_index

    def create_topic_if_not_exists(
        self, 
        topic_name, 
        num_partitions, 
        replication_factor,
        retention_ms = "604800000",
        cleanup_policy = "delete",
        compression_type = "lz4",
        min_insync_replicas = "1"
    ):
        try:
            # Get the existing topics
            metadata = self._admin_client.list_topics(timeout=5)
            if topic_name in metadata.topics:
                self._logger.info(f"Kafka topic '{topic_name}' already exists.")
            else:
                self._logger.info(f"Kafka topic '{topic_name}' does not exist. Creating topic...")

                # Create a new topic
                new_topic = NewTopic(
                    topic_name, 
                    num_partitions=num_partitions, 
                    replication_factor=replication_factor,
                    config={
                        "retention.ms": retention_ms,
                        "cleanup.policy": cleanup_policy ,    
                        "compression.type": compression_type,   
                        "min.insync.replicas": min_insync_replicas   
                    }
                )
                futures = self._admin_client.create_topics([new_topic])

                # Wait for the result of topic creation
                for topic, future in futures.items():
                    try:
                        future.result()  # Block until the topic creation is done
                        self._logger.info(f"Kafka topic '{topic_name}' created successfully. ")
                    except Exception as e:
                        self._logger.error(f"Failed to create Kafka topic '{topic_name}' : {e}")
                        raise

        except KafkaError as e:
            self._logger.critical(f"Error checking or creating Kafka topic : {e}")
            raise
        except Exception as e:
            self._logger.critical(f"An error occurred during topic creation : {e}")
            raise

    def _callback(self, err, message) -> None:
        if err is not None:
            self._logger.warning(f"KAFKA -> Failed to deliver message | Thread [{self._thread_index}]: {err}")
        else:
            self._logger.info(f"KAFKA -> Message delivered to topic [{message.topic()}], partition [{message.partition()}] | Thread [{self._thread_index}]")

    def send(self, data) -> bool:
        try:
            self._producer.produce(
                self._topic,
                json.dumps(data).encode('utf-8'),
                callback=self._callback
            )
            self._producer.flush()
            self._logger.info(f"KAFKA message was sent successfully | Thread [{self._thread_index}]")
            return True
        except KafkaError as e:
            self._logger.error(f"KAFKA error while sending message | Thread [{self._thread_index}]: {e}")
            return False
        except Exception as e:
            self._logger.error(f"Error sending message to KAFKA | Thread [{self._thread_index}]: {e}")
            return False

    def subscribe(self):
        try:
            self._logger.info(f"Subscribing to topic {self._topic} | Thread [{self._thread_index}]")
            self._consumer.subscribe([self._topic])
            return self._consumer
        except KafkaError as e:
            self._logger.error(f"Error subscribing to topic {self._topic} | Thread [{self._thread_index}]: {e}")
            raise
        except Exception as e:
            self._logger.error(f"Error occurred during subscription | Thread [{self._thread_index}]: {e}")
            raise


    def close(self):
        try:
            self._consumer.close()
            self._producer.flush()
            self._logger.warning("Kafka producer and consumer closed | Thread [{self._thread_index}]")
        except KafkaError as e:
            self._logger.error(f"Error closing Kafka producer/consumer | Thread [{self._thread_index}]: {e}")
        except Exception as e:
            self._logger.error(f"Error during Kafka close | Thread [{self._thread_index}]: {e}")