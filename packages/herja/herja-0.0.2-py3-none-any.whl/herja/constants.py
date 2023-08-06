"""A collection of constants for use elsewhere."""

import sys as __sys__


#
#   Request Headers
#

HEADER_ACCEPT_KEY = 'Accept'
HEADER_ACCEPT_TEXT_HTML = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'

HEADER_ACCEPT_ENCODING_KEY = 'Accept-Encoding'
HEADER_ACCEPT_ENCODING_GZIP_DEFLATED = 'gzip, deflate'

HEADER_ACCEPT_LANGUAGE_KEY = 'Accept-Language'
HEADER_ACCEPT_LANGUAGE_ENGLISH = 'en-US,en;q=0.5'

HEADER_CACHE_CONTROL_KEY = 'Cache-Control'
HEADER_CACHE_CONTROL_NONE = 'max-age=0'

HEADER_USER_AGENT_KEY = 'User-Agent'
HEADER_USER_AGENT_PALEMOON_27_4_1 = (
    'Mozilla/5.0 (X11; Linux x86_64; rv:45.9) '
    'Gecko/20100101 Goanna/3.2 Firefox/45.9 PaleMoon/27.4.1'
)


# these are held in a list in case order makes the user agent look less suspicious
HEADER_DEFAULTS = [
    (HEADER_USER_AGENT_KEY, HEADER_USER_AGENT_PALEMOON_27_4_1),
    (HEADER_ACCEPT_KEY, HEADER_ACCEPT_TEXT_HTML),
    (HEADER_ACCEPT_LANGUAGE_KEY, HEADER_ACCEPT_LANGUAGE_ENGLISH),
    (HEADER_ACCEPT_ENCODING_KEY, HEADER_ACCEPT_ENCODING_GZIP_DEFLATED),
    (HEADER_CACHE_CONTROL_KEY, HEADER_CACHE_CONTROL_NONE)
]


PY2 = __sys__.version_info.major == 2
PY3 = __sys__.version_info.major == 3

UTF_16 = 'utf-16'
UTF_16_LE = 'utf-16-le'
UTF_8 = 'utf-8'
