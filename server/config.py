from pydantic_settings import BaseSettings
from typing import Literal, List
import os
from os import environ


env_dict ={
            'TESTING':'env/.env.production',
        }

class Config(BaseSettings):
    #-----------------------------------------------
    #-----------   EXCHANGES URLS   ----------------
    #-----------------------------------------------
    BIANCE_URL    : str = environ.get('BIANCE_URL','')
    COINBASE_URL  : str = environ.get('COINBASE_URL','')
    DERIBIT_URL   : str = environ.get('DERIBIT_URL','')
    OKX_URL       : str = environ.get('OKX_URL','')

    #-----------------------------------------------
    #-----------------   KAFKA     -----------------
    #-----------------------------------------------
    KAFKA_BROKER              : str = environ.get('KAFKA_BROKER','')
    KAFKA_RETENTION_MS        : str = environ.get('KAFKA_RETENTION_MS','')
    KAFKA_CLEANUP_POLICY      : str = environ.get('KAFKA_CLEANUP_POLICY','')
    KAFKA_COMPRESSION_TYPE    : str = environ.get('KAFKA_COMPRESSION_TYPE','')
    KAFKA_MIN_INSYNC_REPLICAS : str = environ.get('KAFKA_MIN_INSYNC_REPLICAS','')
    KAFKA_GROUP_ID            : str = environ.get('KAFKA_GROUP_ID','')
    KAFKA_NUM_PARTITIONS      : int = int(environ.get('KAFKA_NUM_PARTITIONS',1))
    KAFKA_REPLICATION_FACTOR  : int = int(environ.get('KAFKA_REPLICATION_FACTOR',1))

    class Config:
        env_file = env_dict.get(environ.get('ENV','').upper(), 'env/.env.develop')

    def get(self, key: str, default=None):
        """Allows using config.get("KEY") to retrieve attributes."""
        return getattr(self, key, default)

config = Config()