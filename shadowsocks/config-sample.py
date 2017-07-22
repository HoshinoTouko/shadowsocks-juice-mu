import logging

# Database settings
# -----------------------------
DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_USER = 'user'
DB_PASS = 'pass'
DB_NAME = 'ss'
DB_CHARSET = 'utf-8'
DB_TYPE = 'mysql'
DB_TABLE = 'user'
DB_ALIAS = ['port', 'passwd', 'u', 'd', 'transfer_enable', 'enable', 't', 'switch']
# ['port', 'sspwd', 'flow_up', 'flow_down', 'transfer', 'enable', 'lastConnTime', 'enable']
# For sendya/shadowsocks-panel

# SS settings
# -----------------------------
S_BIND_IP = '127.0.0.1'
S_BIND_PORT = 1088
S_METHOD = 'chacha20-ietf-poly1305'
S_TIMEOUT = 5
S_FASTOPEN = False
S_DEBUG = False
S_OTA = False
S_ENABLE_CUSTOM_METHOD = False
S_LOOP_CIRCLE = 30

S_FIREWALLD = True
S_FIREWALL_MODE = 'blacklist'

# Manager settings
# -----------------------------
MANAGER_BIND_IP = '127.0.0.1'
MANAGER_BIND_PORT = 23333


# Log settings
# -----------------------------
LOG_ENABLE = True
# Available Log Level: logging.NOTSET|DEBUG|INFO|WARNING|ERROR|CRITICAL
LOG_LEVEL = logging.INFO
LOG_FILE = 'shadowsocks.log'
# The following format is the one suggested for debugging
# LOG_FORMAT = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'
LOG_DATE_FORMAT = '%b %d %H:%M:%S'
