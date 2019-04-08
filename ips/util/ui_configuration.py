import os

from ips_common.config.configuration import Configuration


class UIConfiguration(Configuration):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Hello, my name is Rudolf and I have a secret...'
    CACHE_NO_NULL_WARNING = True
    BOOTSTRAP_SERVE_LOCAL = True
    USERS_PER_PAGE = 5
    LDAP_SERVER = ''
    ENV = 'dev'
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG_TB_ENABLED = True
    CACHE_TYPE = 'null'
    ITEMS_PER_PAGE = 40
    MAX_ITEMS_RETURNED = 5000

    def __init__(self):
        super().__init__(__name__, 'config.yaml')

    def get_api_uri(self):
        protocol = self.cfg['app']['api-server']['protocol'] or "http"
        host = self.cfg['app']['api-server']['host'] or "127.0.0.1"
        port = self.cfg['app']['api-server']['port'] or "5000"
        portSetting = ""

        if port is not None:
            portSetting = ":" + port

        return protocol + "://" + host + portSetting

    def get_hostname(self):
        return self.cfg['app']['hostname'] or "0.0.0.0"

    def get_port(self):
        return self.cfg['app']['port']


class ProdConfig(UIConfiguration):

    ENV = 'prod'
    CACHE_TYPE = 'simple'


class DevConfig(UIConfiguration):

    ENV = 'dev'
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'null'
    ASSETS_DEBUG = True


class TestConfig(UIConfiguration):

    ENV = 'test'
    DEBUG = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    CACHE_TYPE = 'null'
    WTF_CSRF_ENABLED = False



