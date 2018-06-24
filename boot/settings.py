from os import environ

config = {
#    'SERVER_NAME': f"boot.{environ['DOMAIN_ROOT']}",
    'SECRET_KEY': environ['SECRET_KEY'],
    'DOMAIN_ROOT': environ.get('DOMAIN_ROOT'),
    'REBBLE_AUTH_URL': environ.get('REBBLE_AUTH_URL', f"http://auth.{environ['DOMAIN_ROOT']}"),
    'APPSTORE_URL': environ.get('APPSTORE_URL', f"http://apps.{environ['DOMAIN_ROOT']}"),
    'COHORTS_URL': environ.get('COHORTS_URL', f"http://cohorts.{environ['DOMAIN_ROOT']}"),
    'AUTH_REBBLE': {
        'consumer_key': environ['REBBLE_CONSUMER_KEY'],
        'consumer_secret': environ['REBBLE_CONSUMER_SECRET'],
    }
}
