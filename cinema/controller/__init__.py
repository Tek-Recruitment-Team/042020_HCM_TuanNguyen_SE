import main
# Load san config
import configparser
import os.path

config = configparser.ConfigParser()
config.read(os.path.dirname(__file__) + '/../config_payment.conf') # Tùy đường dẫn server

environment = ['vnpay', 'momo']
settings = {}
for item in environment:
    env_item = dict(config.items(item))
    settings.update({item: env_item})