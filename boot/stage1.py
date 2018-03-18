from flask import Blueprint, jsonify, request
import requests
from .settings import config

UPSTREAM_BOOT = 'https://boot.getpebble.com/api/config'
CLOUDPEBBLE_WS_PROXY = f"wss://ws-proxy.cloudpebble.{config['DOMAIN_ROOT']}/device"

boot_api = Blueprint('boot_api', __name__)


def patch_boot(endpoint: str, locale: str=None, version: str=None):
    boot = requests.get(f'{UPSTREAM_BOOT}/{endpoint}', params={
        'app_version': version or '4.4',
        'locale': locale or 'en_US'
    }).json()
    boot['config'].get('developer', {})['ws_proxy_url'] = CLOUDPEBBLE_WS_PROXY
    boot['config']['href'] = request.base_url
    return boot


@boot_api.route('/ios')
def boot_ios():
    app_version = request.args.get('app_version')
    locale = request.args.get('locale')
    return jsonify(patch_boot('ios/v3/207/28', locale, app_version))


@boot_api.route('/android/v3/<int:build>')
def boot_android(build: int):
    app_version = request.args.get('app_version')
    locale = request.args.get('locale')
    return jsonify(patch_boot(f'android/v3/{build}', locale, app_version))
