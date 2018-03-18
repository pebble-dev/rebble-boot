from os import environ

config = {
#    'SERVER_NAME': f"boot.{environ['DOMAIN_ROOT']}",
    'DOMAIN_ROOT': environ['DOMAIN_ROOT'],
}
