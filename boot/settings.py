from os import environ

config = {
#    'SERVER_NAME': f"boot.{environ['DOMAIN_ROOT']}",
    'SECRET_KEY': environ['SECRET_KEY'],
    'DOMAIN_ROOT': environ.get('DOMAIN_ROOT'),
    'REBBLE_AUTH': environ.get('REBBLE_AUTH', f"http://auth.{environ['DOMAIN_ROOT']}"),
    'AUTH_REBBLE': {
        'consumer_key': environ['REBBLE_CONSUMER_KEY'],
        'consumer_secret': environ['REBBLE_CONSUMER_SECRET'],
    }
}
