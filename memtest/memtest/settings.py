from os import environ

SECRET_KEY = environ["SECRET_KEY"]
REDIS_HOST = environ["REDIS_HOST"]
REDIS_PORT = environ["REDIS_PORT"]

DEBUG = False
DEBUG_TOOLBAR = False

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = []

MIDDLEWARE = []

ROOT_URLCONF = 'memtest.urls'

CHANNEL_LAYERS = {
    'default': {
        # FIX 1: use `channels.layers.InMemoryChannelLayer`` instead of RedisChannelLayer
        # 'BACKEND': 'channels.layers.InMemoryChannelLayer,
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}

LOGGING = {
    'version': 1,
    'root': {
        # FIX 2: change logging level to INFO
        # 'level': 'INFO',
        'level': 'DEBUG',
    },
}
