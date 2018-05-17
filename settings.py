import os

from configparser import ConfigParser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PLATFORM_CONFIG_NAME = 'screen-bot.conf'
production_config = os.path.join('/etc', 'screen-bot', PLATFORM_CONFIG_NAME)
development_config = os.path.join(BASE_DIR, 'conf', PLATFORM_CONFIG_NAME)
config_path = production_config if os.path.exists(production_config) else development_config
config = ConfigParser()

config.read(config_path)

TOKEN = config.get('main', 'token', fallback='')
TBB_FX_PATH = config.get('main', 'tbb_fx_path', fallback='')
GECKODRIVER_PATH = config.get('main', 'geckodriver_path', fallback='')
MEDIA_PATH = config.get('main', 'media_path', fallback='')
