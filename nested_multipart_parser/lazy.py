import re

# compatibilty python < 3.9
try:
    from functools import cache
except ImportError:
    from functools import lru_cache as cache


@cache
def lazy_regex_compile(*ar, **kw):
    return re.compile(*ar, **kw)
