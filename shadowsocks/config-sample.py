import logging

# Database settings
# -----------------------------
DB_

# SS settings
# -----------------------------
S_BIND_IP = '127.0.0.1'
S_BIND_PORT = 1088
S_METHOD = 'chacha20-ietf-poly1305'
S_TIMEOUT = 5
S_FASTOPEN = False
S_DEBUG = True
S_OTA = False

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
