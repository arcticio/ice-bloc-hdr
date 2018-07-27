import aio

aio.debug("loading settings.py")

TEMPLATES = [
    {
        # something else
        'OPTIONS': {
            'debug': DEBUG,
        },
    },
]