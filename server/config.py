from pydantic_settings import BaseSettings
from typing import Literal, List
import os
from os import environ


env_dict ={
            'PRODUCTION':'env/.env.production',

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
    KAFKA_BROKER             : str = environ.get('KAFKA_BROKER','')
    KAFKA_NUM_PARTITIONS     : str = environ.get('KAFKA_NUM_PARTITIONS','')
    KAFKA_REPLICATION_FACTOR : str = environ.get('KAFKA_REPLICATION_FACTOR','')

    class Config:
        env_file = env_dict.get(environ.get('ENV','').upper(), 'env/.env.develop')

    def get(self, key: str, default=None):
        """Allows using config.get("KEY") to retrieve attributes."""
        return getattr(self, key, default)

config = Config()