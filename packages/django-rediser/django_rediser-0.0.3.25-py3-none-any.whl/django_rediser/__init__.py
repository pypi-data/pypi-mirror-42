# -*- coding: utf-8 -*-
from .config import __version__

version = str(__version__).split('.')
if len(version) < 4:
    version = __version__
else:
    if version[3].lower().startswith('dev'):
        version = __version__
    else:
        version = '{} build {}'.format('.'.join(version[:3]), version[3])

try:
    from .storage import RedisStorage, RedisJSON
except ImportError:
    print('`redis` package not found')
