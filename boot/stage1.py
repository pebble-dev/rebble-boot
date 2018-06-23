from flask import Blueprint, jsonify, request
import requests
from .settings import config

UPSTREAM_BOOT = 'https://boot.getpebble.com/api/config'
CLOUDPEBBLE_WS_PROXY = f"wss://ws-proxy.cloudpebble.{config['DOMAIN_ROOT']}/device"

stage1 = Blueprint('stage1', __name__)


def patch_boot(endpoint: str, locale: str=None, version: str=None):
    boot = requests.get(f'{UPSTREAM_BOOT}/{endpoint}', params={
        'app_version': version or '4.4',
        'locale': locale or 'en_US'
    }).json()
    boot['config'].get('developer', {})['ws_proxy_url'] = CLOUDPEBBLE_WS_PROXY
    boot['config']['href'] = request.base_url
    return boot


@stage1.route('/ios')
def boot_ios():
    app_version = request.args.get('app_version')
    locale = request.args.get('locale')
    return jsonify(patch_boot('ios/v3/207/28', locale, app_version))


@stage1.route('/android/v3/<int:build>')
def boot_android(build: int):
    app_version = request.args.get('app_version')
    locale = request.args.get('locale')
    return jsonify(patch_boot(f'android/v3/{build}', locale, app_version))


@stage1.route('/')
def boot_base():
    return 'Please be more specific.', 404


def init_app(app, prefix='/api/stage1'):
    app.register_blueprint(stage1, url_prefix=prefix)
