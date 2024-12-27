from dataclasses import dataclass
from dotenv import load_dotenv
import os


@dataclass
class Config:
    database_uri: str


def get_config():
    load_dotenv()
    database_uri = os.getenv('DATABASE_URL')
    if not database_uri:
        raise ValueError('DATABASE_URI is not set')
    return Config(database_uri=database_uri)
