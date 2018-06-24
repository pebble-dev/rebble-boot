from os import environ

domain_root = environ.get('DOMAIN_ROOT')

config = {
#    'SERVER_NAME': f"boot.{environ['DOMAIN_ROOT']}",
    'SECRET_KEY': environ['SECRET_KEY'],
    'DOMAIN_ROOT': domain_root,
    'REBBLE_AUTH_URL': environ.get('REBBLE_AUTH_URL', f"http://auth.{domain_root}"),
    'APPSTORE_URL': environ.get('APPSTORE_URL', f"http://apps.{domain_root}"),
    'APPSTORE_API_URL': environ.get('APPSTORE_API_URL', f"http://appstore-api.{domain_root}"),
    'COHORTS_URL': environ.get('COHORTS_URL', f"http://cohorts.{domain_root}"),
    'AUTH_REBBLE': {
        'consumer_key': environ['REBBLE_CONSUMER_KEY'],
        'consumer_secret': environ['REBBLE_CONSUMER_SECRET'],
    }
}
