from os import environ

domain_root = environ.get('DOMAIN_ROOT')
http_protocol = environ.get('HTTP_PROTOCOL', 'https')

config = {
#    'SERVER_NAME': f"boot.{environ['DOMAIN_ROOT']}",
    'SECRET_KEY': environ['SECRET_KEY'],
    'DOMAIN_ROOT': domain_root,
    'REBBLE_AUTH_URL': environ.get('REBBLE_AUTH_URL', f"{http_protocol}://auth.{domain_root}"),
    'REBBLE_AUTH_INT_URL': environ.get('REBBLE_AUTH_INT_URL', f"{http_protocol}://auth.{domain_root}"),
    'REBBLE_TIMELINE_URL': environ.get('REBBLE_TIMELINE_URL', f"{http_protocol}://timeline-api.{domain_root}"),
    'APPSTORE_URL': environ.get('APPSTORE_URL', f"http://apps.{domain_root}"),
    'APPSTORE_API_URL': environ.get('APPSTORE_API_URL', f"http://appstore-api.{domain_root}"),
    'COHORTS_URL': environ.get('COHORTS_URL', f"http://cohorts.{domain_root}"),
    'LANGUAGE_PACK_URL': environ.get('LANGUAGE_PACK_URL', f"http://lp.{domain_root}"),
    'WEATHER_URL': environ.get('WEATHER_URL', f'http://weather.{domain_root}'),
    'ASR_ROOT': environ.get('ASR_ROOT', f"asr.{domain_root}"),
    'AUTH_REBBLE': {
        'consumer_key': environ['REBBLE_CONSUMER_KEY'],
        'consumer_secret': environ['REBBLE_CONSUMER_SECRET'],
    },
    'HONEYCOMB_KEY': environ.get('HONEYCOMB_KEY', None),
}
