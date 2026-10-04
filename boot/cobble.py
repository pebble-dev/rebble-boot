from flask import Blueprint, jsonify, request
import requests

from .settings import config

cobble = Blueprint('cobble', __name__)

@cobble.route('/')
def boot_cobble():
    build = request.args.get('build')
    platform = request.args.get('platform')
    locale = request.args.get('locale', 'en_US')
    boot = {
        "auth": {
            "base": f"{config['REBBLE_AUTH_URL']}/api",
            "authorize_url": f"{config['REBBLE_AUTH_URL']}/oauth/authorise",
            "refresh_url": f"{config['REBBLE_AUTH_URL']}/oauth/token",
            "client_id": config['COBBLE_OAUTH_CLIENT_ID']
        },
        "appstore": {
            "base": f"{config['APPSTORE_API_URL']}/api"
        },
        "locker": {
            "add_endpoint": f"{config['APPSTORE_API_URL']}/api/v1/locker/$$app_uuid$$",
            "get_endpoint": f"{config['APPSTORE_API_LOCKER_URL']}/api/v1/locker",
            "remove_endpoint": f"{config['APPSTORE_API_URL']}/api/v1/locker/$$app_uuid$$"
        },
        "timeline": {
            "pin_endpoint": f"{config['REBBLE_TIMELINE_URL']}/v1/user/pins/$$pin_id$$",
            "pin_ttl_seconds": 259200,
            "sandbox_user_token": f"{config['REBBLE_TIMELINE_URL']}/v1/tokens/sandbox/$$uuid$$",
            "subscribe_to_topic": f"{config['REBBLE_TIMELINE_URL']}/v1/user/subscriptions/$$topic_id$$",
            "subscriptions_list": f"{config['REBBLE_TIMELINE_URL']}/v1/user/subscriptions",
            "sync_endpoint": f"{config['REBBLE_TIMELINE_URL']}/v1/sync",
            "sync_policy_minutes": 60
        },
        "webviews": {
            "appstoreApplication": f"{config['APPSTORE_URL']}/{locale}/application/",
            "appstoreWatchapps": f"{config['APPSTORE_URL']}/{locale}/watchapps",
            "appstoreWatchfaces": f"{config['APPSTORE_URL']}/{locale}/watchfaces",
            "manageAccount": config['REBBLE_ACCOUNT_URL']
        }
    }
    return jsonify(boot)

def init_app(app, prefix='/api/cobble'):
    app.register_blueprint(cobble, url_prefix=prefix)
