from flask import Blueprint, jsonify, request, url_for, render_template

from .auth import rebble
from .settings import config

UPSTREAM_BOOT = 'https://boot.getpebble.com/api/config'
CLOUDPEBBLE_WS_PROXY = f"wss://ws-proxy.cloudpebble.{config['DOMAIN_ROOT']}/device"

stage2 = Blueprint('stage2', __name__)


def generate_boot(platform):
    app_version = request.args.get('app_version')
    access_token = request.args['access_token']
    locale = request.args.get('locale', 'en_US')
    appstore = f"https://apps.rebble.io"

    return {
        "config": {
            "algolia": {
                "api_key": "252f4938082b8693a8a9fc0157d1d24f",
                "app_id": "7683OW76EQ",
                "index": "rebble-appstore-production",
            },
            "app_meta": {
                "force_3x_app_migration": False,
                "gcm_sender_id": "946814448057"
            },
            "authentication": {
                "debug_access_token_cookie": {
                    "domain": f".{config['DOMAIN_ROOT']}",
                    "secure": True,
                },
                "method": "oauth2",
                "refresh_token": f"{config['REBBLE_AUTH_URL']}/oauth/token",
                "sign_in": f"{config['REBBLE_AUTH_URL']}/oauth/token",
                "sign_up": f"{config['REBBLE_AUTH_URL']}/oauth/token"
            },
            "cohorts": {
                "endpoint": f"{config['COHORTS_URL']}/cohort"
            },
            "developer": {
                "ws_proxy_url": "wss://cloudpebble-ws-proxy-prod.herokuapp.com/device"
            },
            "health": {
                "post_activity_endpoint": "https://health-write-api.getpebble.com/v1/activity",
                "post_settings_endpoint": "https://health-write-api.getpebble.com/v1/settings"
            },
            "href": request.url,
            "id": f"{platform}/v1",
            # "linked_services": {
            #     "account_refresh_endpoint": "https://linked-accounts.getpebble.com/v1/providers/$$provider$$/refresh",
            #     "account_revoke_endpoint": "https://linked-accounts.getpebble.com/v1/providers/$$provider$$/revoke",
            #     "authorize_sessions_endpoint": "https://linked-accounts.getpebble.com/v1/providers/$$provider$$/authorize/sessions?state=$$state$$",
            #     "email_action_endpoint": "https://email-actions-api.getpebble.com/v1/email/actions/$$action$$/$$transaction_id$$",
                "enabled_providers": [
                    # "att",
                    # "vzw"
                ],
            #     "reauthorize_pin_send_endpoint": "https://linked-accounts.getpebble.com/v1/providers/$$provider$$/reauthorize/pin/send",
            #     "reauthorize_pin_verify_endpoint": "https://linked-accounts.getpebble.com/v1/providers/$$provider$$/reauthorize/pin/verify",
            #     "reauthorize_sessions_endpoint": "https://linked-accounts.getpebble.com/v1/providers/$$provider$$/reauthorize/sessions",
            #     "sms_send_endpoint": "https://sms-api.getpebble.com/v1/sms/actions/send/$$transaction_id$$"
            # },
            "links": {
                # "apps/app_index": "https://dev-portal.getpebble.com/api/categories/index?platform=ios&jsv=28",
                # "apps/categories": "https://dev-portal.getpebble.com/api/categories?platform=ios&jsv=28",
                # "apps/face_index": "https://dev-portal.getpebble.com/api/categories/faces?platform=ios&jsv=28",
                # "apps/failed_upgrades": "https://dev-portal.getpebble.com/api/failed_upgrades?platform=ios&jsv=28",
                # "apps/uuid_upgrades": "https://dev-portal.getpebble.com/api/applications/upgrade?platform=ios&jsv=28",
                "authentication/me": f"{config['REBBLE_AUTH_URL']}/api/v1/me/pebble/auth",
                # "authentication/push_tokens": "https://auth.getpebble.com/api/v1/push_tokens?platform=ios",
                # "diagnostics": "https://auth-api.getpebble.com/api/v2/users/diagnostics",
                "i18n/language_packs": "https://lp.getpebble.com/v1/languages",
                # "remote_device_analytics": "https://pb-collector.getpebble.com/analytics",
                # "resources": "https://dev-portal.getpebble.com/api?platform=ios&jsv=28",
                # "trending_searches": "https://pebble-trending-searches.s3-us-west-2.amazonaws.com/production/data.json?hardware=$$hardware$$&platform=ios",
                "users/app_locker": f"https://dev-portal.getpebble.com/api/users/locker?platform={platform}&jsv=28",
                "users/me": f"{config['APPSTORE_API_URL']}/api/v0/users/me?platform={platform}"
            },
            "locker": {
                "add_endpoint": "https://appstore-api.getpebble.com/v2/locker/$$app_uuid$$",
                "get_endpoint": "https://appstore-api.getpebble.com/v2/locker",
                "onboarding_data": f"https://pebble-onboarding-data.s3-us-west-2.amazonaws.com/production/{platform}/$$hardware$$.json",
                "remove_endpoint": "https://appstore-api.getpebble.com/v2/locker/$$app_uuid$$"
            },
            "notifications": {
                "ios_app_icons": f"http://notif-app-icons.{config['DOMAIN_ROOT']}/{platform}/$$bundle_id$$/$$size$$.jpg"
            },
            "support_request": {
                "email": "support@getpebble.com"
            },
            "timeline": {
                "pin_ttl_seconds": 259200,
                "sandbox_user_token": "https://timeline-sync.getpebble.com/v1/tokens/sandbox/$$uuid$$",
                "subscribe_to_topic": "https://timeline-api.getpebble.com/v1/user/subscriptions/$$topic_id$$",
                "subscriptions_list": "https://timeline-api.getpebble.com/v1/user/subscriptions",
                "sync_endpoint": "https://timeline-sync.getpebble.com/v1/sync",
                "sync_policy_minutes": 60
            },
            "voice": {
                "first_party_uuids": [
                    "3351e678-c9c3-4299-b573-47637aebe34a"
                ],
                "languages": [
                    {
                        "endpoint": "pebble-ncs-dan-DNK.nuancemobility.net",
                        "four_char_locale": "da_DK",
                        "six_char_locale": "dan-DNK"
                    },
                    {
                        "endpoint": "pebble-ncs-deu-DEU.nuancemobility.net",
                        "four_char_locale": "de_DE",
                        "six_char_locale": "deu-DEU"
                    },
                    {
                        "endpoint": "pebble-ncs-eng-AUS.nuancemobility.net",
                        "four_char_locale": "en_AU",
                        "six_char_locale": "eng-AUS"
                    },
                    {
                        "endpoint": "pebble-ncs-eng-GBR.nuancemobility.net",
                        "four_char_locale": "en_GB",
                        "six_char_locale": "eng-GBR"
                    },
                    {
                        "endpoint": "pebble-ncs-eng-USA.nuancemobility.net",
                        "four_char_locale": "en_US",
                        "six_char_locale": "eng-USA"
                    },
                    {
                        "endpoint": "pebble-ncs-fin-FIN.nuancemobility.net",
                        "four_char_locale": "fi_FI",
                        "six_char_locale": "fin-FIN"
                    },
                    {
                        "endpoint": "pebble-ncs-fra-CAN.nuancemobility.net",
                        "four_char_locale": "fr_CA",
                        "six_char_locale": "fra-CAN"
                    },
                    {
                        "endpoint": "pebble-ncs-fra-FRA.nuancemobility.net",
                        "four_char_locale": "fr_FR",
                        "six_char_locale": "fra-FRA"
                    },
                    {
                        "endpoint": "pebble-ncs-ita-ITA.nuancemobility.net",
                        "four_char_locale": "it_IT",
                        "six_char_locale": "ita-ITA"
                    },
                    {
                        "endpoint": "pebble-ncs-nld-NLD.nuancemobility.net",
                        "four_char_locale": "nl_NL",
                        "six_char_locale": "nld-NLD"
                    },
                    {
                        "endpoint": "pebble-ncs-nor-NOR.nuancemobility.net",
                        "four_char_locale": "nb_NO",
                        "six_char_locale": "nor-NOR"
                    },
                    {
                        "endpoint": "pebble-ncs-por-PRT.nuancemobility.net",
                        "four_char_locale": "pt_PT",
                        "six_char_locale": "por-PRT"
                    },
                    {
                        "endpoint": "pebble-ncs-spa-ESP.nuancemobility.net",
                        "four_char_locale": "es_ES",
                        "six_char_locale": "spa-ESP"
                    },
                    {
                        "endpoint": "pebble-ncs-spa-XLA.nuancemobility.net",
                        "four_char_locale": "es_MX",
                        "six_char_locale": "spa-XLA"
                    },
                    {
                        "endpoint": "pebble-ncs-swe-SWE.nuancemobility.net",
                        "four_char_locale": "sv_SE",
                        "six_char_locale": "swe-SWE"
                    }
                ]
            },
            "weather": {
                "url": "https://api.weather.com/v2/geocode/$$latitude$$/$$longitude$$/aggregate.json?apiKey=bbf04402eb962506451832d6a828b4d0&products=conditions,fcstdaily7&language=$$language$$&units=$$units$$"
            },
            "webviews": {
                "appstore/application": f"{appstore}/{locale}/application/$$id$$?access_token={access_token}&platform={platform}&release_id=207&app_version=4.4&pebble_color=$$pebble_color$$&hardware=$$hardware$$&jsv=28&uid=$$user_id$$&mid=$$phone_id$$&pid=$$pebble_id$$&$$extras$$",
                "appstore/application_changelog": f"{appstore}/{locale}/changelog/$$id$$?access_token={access_token}&platform={platform}&release_id=207&app_version=4.4&pebble_color=$$pebble_color$$&hardware=$$hardware$$&jsv=28&uid=$$user_id$$&mid=$$phone_id$$&pid=$$pebble_id$$&$$extras$$",
                "appstore/application_share": f"{appstore}/applications/$$id$$",
                "appstore/developer_apps": f"{appstore}/{locale}/developer/$$id$$?access_token={access_token}&platform={platform}&release_id=207&app_version=4.4&pebble_color=$$pebble_color$$&hardware=$$hardware$$&jsv=28&uid=$$user_id$$&mid=$$phone_id$$&pid=$$pebble_id$$&$$extras$$",
                "appstore/search": f"{appstore}/{locale}/search?access_token={access_token}&platform={platform}&release_id=207&app_version=4.4&pebble_color=$$pebble_color$$&hardware=$$hardware$$&jsv=28&uid=$$user_id$$&mid=$$phone_id$$&pid=$$pebble_id$$&$$extras$$",
                "appstore/search/query": f"{appstore}/{locale}/search/$$search_type$$?access_token={access_token}&native=true&query=$$query$$&platform={platform}&release_id=207&app_version=4.4&pebble_color=$$pebble_color$$&hardware=$$hardware$$&jsv=28&uid=$$user_id$$&mid=$$phone_id$$&pid=$$pebble_id$$&$$extras$$",
                "appstore/watchapps": f"{appstore}/{locale}/watchapps?access_token={access_token}&platform={platform}&release_id=207&app_version=4.4&pebble_color=$$pebble_color$$&hardware=$$hardware$$&jsv=28&uid=$$user_id$$&mid=$$phone_id$$&pid=$$pebble_id$$&$$extras$$",
                "appstore/watchfaces": f"{appstore}/{locale}/watchfaces?access_token={access_token}&platform={platform}&release_id=207&app_version=4.4&pebble_color=$$pebble_color$$&hardware=$$hardware$$&jsv=28&uid=$$user_id$$&mid=$$phone_id$$&pid=$$pebble_id$$&$$extras$$",
                "authentication/sign_in": f"{url_for('.auth', _external=True)}?access_token={access_token}&platform={platform}&release_id=207&ap_version=4.4&mid=$$phone_id$$&pid=$$pebble_id$$&redirect_uri=pebble%3A%2F%2Flogin",
                "authentication/sign_up": f"{url_for('.auth', _external=True)}?access_token={access_token}&platform={platform}&release_id=207&ap_version=4.4&mid=$$phone_id$$&pid=$$pebble_id$$&redirect_uri=pebble%3A%2F%2Flogin",
                "loading/buy_a_pebble": "https://getpebble.com?utm_campaign=PebbleApp&utm_medium=referral&utm_source={platform}-start-screen",
                "onboarding/get_more_info": "http://help.getpebble.com/customer/portal/articles/1422148-migration",
                "onboarding/get_some_apps": f"{appstore}/{locale}/onboarding/getsomeapps?platform={platform}&release_id=207&app_version=4.4&pebble_color=$$pebble_color$$&hardware=$$hardware$$&jsv=28&uid=$$user_id$$&mid=$$phone_id$$&pid=$$pebble_id$$&$$extras$$",
                "onboarding/migrate": f"{appstore}/{locale}/onboarding/migrate?platform={platform}&release_id=207&app_version=4.4&pebble_color=$$pebble_color$$&hardware=$$hardware$$&jsv=28&uid=$$user_id$$&mid=$$phone_id$$&pid=$$pebble_id$$&$$extras$$",
                "onboarding/nexmo_acceptable_use_policy": "https://www.nexmo.com/acceptable-use/",
                "onboarding/nexmo_privacy_policy": "https://www.nexmo.com/privacy-policy/",
                "onboarding/privacy_policy": "https://www.pebble.com/legal/privacy#",
                "onboarding/sms_privacy_policy": "https://www.pebble.com/legal/privacy#sms",
                "support": "http://help.getpebble.com/customer/en/portal/articles",
                "support/android-actionable-notifications": "http://help.getpebble.com/customer/en/portal/articles/1819783",
                "support/bt_findcode_help": "http://help.getpebble.com/customer/en/portal/articles/1422126",
                "support/bt_pairing_help": "http://help.getpebble.com/customer/en/portal/articles/1786833",
                "support/community": "http://help.getpebble.com/customer/en/portal/articles/1422153",
                "support/faq": "http://help.getpebble.com/customer/en/portal/articles/1949825-faq?b_id=8309",
                "support/fw_update_failed_help": "http://help.getpebble.com/customer/en/portal/articles/1774825",
                "support/getting_started": "http://help.getpebble.com/customer/en/portal/articles/1957400?b_id=8309",
                "support/ios_sms_replies": "http://help.getpebble.com/customer/en/portal/articles/2166170",
                "support/suggest_something": "http://help.getpebble.com/customer/en/portal/articles/1889438?b_id=8309"
            }
        }
    }


@stage2.route('/ios')
def boot_ios():
    resp = jsonify(generate_boot('ios'))
    resp.headers['Cache-Control'] = 'private, no-cache'
    return resp


@stage2.route('/android/v3/<int:build>')
def boot_android(build: int):
    resp = jsonify(generate_boot('android'))
    resp.headers['Cache-Control'] = 'private, no-cache'
    return resp


@stage2.route('/')
def boot_base():
    return 'Please be more specific.', 404


@stage2.route('/auth')
def auth():
    me = rebble.get(f"{config['REBBLE_AUTH_URL']}/api/v1/me/pebble/auth")
    link = f"pebble://login#access_token={request.args['access_token']}&refresh_token=null&expires_in=null&signed_eula=2015-05-01&signed_privacy_policy=2015-11-18"
    return render_template('complete-auth.html', link=link, name=me.data['name'])


def init_app(app, prefix='/api/stage2'):
    app.register_blueprint(stage2, url_prefix=prefix)
