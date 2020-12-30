import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    TESTING = False
    SECRET_KEY = b'\x18\xff`\x18T\xe7\x88\xb7\xbdh\x163\xe1\x823\x85'


class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True