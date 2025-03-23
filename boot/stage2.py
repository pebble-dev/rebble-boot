import requests
from flask import Blueprint, jsonify, request, url_for, render_template
import beeline

from .auth import rebble
from .settings import config

UPSTREAM_BOOT = 'https://boot.getpebble.com/api/config'
CLOUDPEBBLE_WS_PROXY = f"wss://ws-proxy.cloudpebble.{config['DOMAIN_ROOT']}/device"

stage2 = Blueprint('stage2', __name__)

@beeline.traced(name='generate_boot')
def generate_boot(platform):
    app_version = request.args.get('app_version')
    access_token = request.args['access_token']
    locale = request.args.get('locale', 'en_US')

    #  Otherwise we end up directing people to nonexistent pages, I guess?
    if locale not in {'en_US', 'fr_FR', 'de_DE', 'es_ES', 'nl_NL', 'pl_PL', 'zh_CN', 'zh_TW'}:
        locale = 'en_US'

    appstore = config['APPSTORE_URL']

    boot = {
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
                "ws_proxy_url": f"{config['WS_PROXY_URL']}"
            },
            "health": {
                "post_activity_endpoint": "https://health-write-api.getpebble.com/v1/activity",
                "post_settings_endpoint": "https://health-write-api.getpebble.com/v1/settings"
            },
            "href": request.url,
            "id": f"{platform}/v1",
            "linked_services": {
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
            },
            "links": {
                # "apps/app_index": "https://dev-portal.getpebble.com/api/categories/index?platform=ios&jsv=200",
                # "apps/categories": "https://dev-portal.getpebble.com/api/categories?platform=ios&jsv=200",
                # "apps/face_index": "https://dev-portal.getpebble.com/api/categories/faces?platform=ios&jsv=200",
                # "apps/failed_upgrades": "https://dev-portal.getpebble.com/api/failed_upgrades?platform=ios&jsv=200",
                # "apps/uuid_upgrades": "https://dev-portal.getpebble.com/api/applications/upgrade?platform=ios&jsv=200",
                "authentication/me": f"{config['REBBLE_AUTH_URL']}/api/v1/me/pebble/auth",
                # "authentication/push_tokens": "https://auth.getpebble.com/api/v1/push_tokens?platform=ios",
                # "diagnostics": "https://auth-api.getpebble.com/api/v2/users/diagnostics",
                "i18n/language_packs": f"{config['LANGUAGE_PACK_URL']}/v1/languages",
                # "remote_device_analytics": "https://pb-collector.getpebble.com/analytics",
                # "resources": "https://dev-portal.getpebble.com/api?platform=ios&jsv=200",
                # "trending_searches": "https://pebble-trending-searches.s3-us-west-2.amazonaws.com/production/data.json?hardware=$$hardware$$&platform=ios",
                # "users/app_locker": f"https://dev-portal.getpebble.com/api/users/locker?platform={platform}&jsv=200",
                "users/me": f"{config['APPSTORE_API_URL']}/api/v0/users/me?platform={platform}"
            },
            "locker": {
                "add_endpoint": f"{config['APPSTORE_API_URL']}/api/v1/locker/$$app_uuid$$",
                "get_endpoint": f"{config['APPSTORE_API_LOCKER_URL']}/api/v1/locker",
                "onboarding_data": f"https://pebble-onboarding-data.s3-us-west-2.amazonaws.com/production/{platform}/$$hardware$$.json",
                "remove_endpoint": f"{config['APPSTORE_API_URL']}/api/v1/locker/$$app_uuid$$"
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
            "treasure_data": {
                "endpoint": "https://treasure.rebble.io",
            },
            "voice": {
                "first_party_uuids": [
                    "3351e678-c9c3-4299-b573-47637aebe34a"
                ],
                "languages": [],
            },
            "webviews": {
                "appstore/application": f"{appstore}/{locale}/application/$$id$$?&access_token={access_token}&platform={platform}&release_id=207&app_version=4.4&pebble_color=$$pebble_color$$&hardware=$$hardware$$&jsv=200&uid=$$user_id$$&mid=$$phone_id$$&pid=$$pebble_id$$&$$extras$$",
                "appstore/application_changelog": f"{appstore}/{locale}/changelog/$$id$$?&access_token={access_token}&platform={platform}&release_id=207&app_version=4.4&pebble_color=$$pebble_color$$&hardware=$$hardware$$&jsv=200&uid=$$user_id$$&mid=$$phone_id$$&pid=$$pebble_id$$&$$extras$$",
                "appstore/application_share": f"{appstore}/{locale}/applications/$$id$$",
                "appstore/developer_apps": f"{appstore}/{locale}/developer/$$id$$?&access_token={access_token}&platform={platform}&release_id=207&app_version=4.4&pebble_color=$$pebble_color$$&hardware=$$hardware$$&jsv=200&uid=$$user_id$$&mid=$$phone_id$$&pid=$$pebble_id$$&$$extras$$",
                "appstore/search": f"{appstore}/{locale}/search?&access_token={access_token}&platform={platform}&release_id=207&app_version=4.4&pebble_color=$$pebble_color$$&hardware=$$hardware$$&jsv=200&uid=$$user_id$$&mid=$$phone_id$$&pid=$$pebble_id$$&$$extras$$",
                "appstore/search/query": f"{appstore}/{locale}/search/$$search_type$$?&access_token={access_token}&native=true&query=$$query$$&platform={platform}&release_id=207&app_version=4.4&pebble_color=$$pebble_color$$&hardware=$$hardware$$&jsv=200&uid=$$user_id$$&mid=$$phone_id$$&pid=$$pebble_id$$&$$extras$$",
                "appstore/watchapps": f"{appstore}/{locale}/watchapps?&access_token={access_token}&platform={platform}&release_id=207&app_version=4.4&pebble_color=$$pebble_color$$&hardware=$$hardware$$&jsv=200&uid=$$user_id$$&mid=$$phone_id$$&pid=$$pebble_id$$&$$extras$$",
                "appstore/watchfaces": f"{appstore}/{locale}/watchfaces?&access_token={access_token}&platform={platform}&release_id=207&app_version=4.4&pebble_color=$$pebble_color$$&hardware=$$hardware$$&jsv=200&uid=$$user_id$$&mid=$$phone_id$$&pid=$$pebble_id$$&$$extras$$",
                "authentication/sign_in": f"{url_for('.auth', _external=True)}?&access_token={access_token}&platform={platform}&release_id=207&ap_version=4.4&mid=$$phone_id$$&pid=$$pebble_id$$&redirect_uri=pebble%3A%2F%2Flogin",
                "authentication/sign_up": f"{url_for('.auth', _external=True)}?&access_token={access_token}&platform={platform}&release_id=207&ap_version=4.4&mid=$$phone_id$$&pid=$$pebble_id$$&redirect_uri=pebble%3A%2F%2Flogin",
                "loading/buy_a_pebble": f"https://getpebble.com?utm_campaign=PebbleApp&utm_medium=referral&utm_source={platform}-start-screen",
                "onboarding/get_more_info": "http://help.getpebble.com/customer/portal/articles/1422148-migration",
                "onboarding/get_some_apps": f"{appstore}/{locale}/onboarding/getsomeapps?platform={platform}&release_id=207&app_version=4.4&pebble_color=$$pebble_color$$&hardware=$$hardware$$&jsv=200&uid=$$user_id$$&mid=$$phone_id$$&pid=$$pebble_id$$&$$extras$$",
                "onboarding/migrate": f"{appstore}/{locale}/onboarding/migrate?platform={platform}&release_id=207&app_version=4.4&pebble_color=$$pebble_color$$&hardware=$$hardware$$&jsv=200&uid=$$user_id$$&mid=$$phone_id$$&pid=$$pebble_id$$&$$extras$$",
                "onboarding/nexmo_acceptable_use_policy": "https://www.nexmo.com/acceptable-use/",
                "onboarding/nexmo_privacy_policy": "https://www.nexmo.com/privacy-policy/",
                "onboarding/privacy_policy": "https://www.pebble.com/legal/privacy#",
                "onboarding/sms_privacy_policy": "https://www.pebble.com/legal/privacy#sms",
                "support": "http://pebble-help-legacy.rebble.io/help.getpebble.com/index.html",
                "support/android-actionable-notifications": "http://pebble-help-legacy.rebble.io/help.getpebble.com/customer/en/portal/articles/1819783-android---actionable-notifications.html",
                "support/bt_findcode_help": "http://pebble-help-legacy.rebble.io/help.getpebble.com/customer/portal/articles/1422126-finding-your-pebble-s-bluetooth-name.html",
                "support/bt_pairing_help": {
                    'ios': "http://pebble-help-legacy.rebble.io/help.getpebble.com/customer/en/portal/articles/1786833-ios---pairing.html",
                    'android': "http://pebble-help-legacy.rebble.io/help.getpebble.com/customer/en/portal/articles/1774338-android---pairing.html",
                }[platform],
                "support/community": "http://pebble-help-legacy.rebble.io/help.getpebble.com/customer/en/portal/articles/2643613-help-community22f6.html",
                "support/faq": "http://pebble-help-legacy.rebble.io/help.getpebble.com/customer/en/portal/articles/1949825-frequently-asked-questions.html",
                "support/fw_update_failed_help": {
                    'ios': "http://pebble-help-legacy.rebble.io/help.getpebble.com/customer/en/portal/articles/1774825-ios---update-failed.html",
                    'android': "http://pebble-help-legacy.rebble.io/help.getpebble.com/customer/en/portal/articles/1738034-android---update-fail.html",
                }[platform],
                "support/getting_started": {
                    'ios': "http://pebble-help-legacy.rebble.io/help.getpebble.com/customer/portal/articles/1957400-ios---getting-started-with-pebble-time6d9c.html",
                    'android': "http://pebble-help-legacy.rebble.io/help.getpebble.com/customer/portal/articles/1936231-android---getting-started-with-pebble-time6d9c.html",
                }[platform],
                "support/ios_sms_replies": "http://pebble-help-legacy.rebble.io/help.getpebble.com/customer/portal/articles/2166170-sms-messaging2d1a.html",
                "support/suggest_something": "http://pebble-help-legacy.rebble.io/help.getpebble.com/customer/en/portal/articles/1889438-pebble-time-suggestions.html",
            }
        }
    }

    user = rebble.get(f"me?flag_authed=true")
    user_ok = user.status == 200
    beeline.add_context_field("user.ok", user_ok)
    if user_ok:
        beeline.add_context_field("user", user.data.get('uid'))
        beeline.add_context_field("user.has_timeline", user.data.get('has_timeline', False))
        beeline.add_context_field("user.is_subscribed", user.data.get('is_subscribed', False))

        if user.data.get('has_timeline', False):
            boot['config']['timeline'] = {
                "pin_ttl_seconds": 259200,
                "sandbox_user_token": f"{config['REBBLE_TIMELINE_URL']}/v1/tokens/sandbox/$$uuid$$",
                "subscribe_to_topic": f"{config['REBBLE_TIMELINE_URL']}/v1/user/subscriptions/$$topic_id$$",
                "subscriptions_list": f"{config['REBBLE_TIMELINE_URL']}/v1/user/subscriptions",
                "sync_endpoint":      f"{config['REBBLE_TIMELINE_URL']}/v1/sync",
                "sync_policy_minutes": user.data.get('timeline_ttl', 3 * 60)
            }
        
        # A user can override with something like 'rebble.noident=True' or
        # something, if they would like.
        boot['config']['treasure_data']['write_key'] = f"rebble.user={user.data.get('uid')},rebble.subscribed={user.data.get('is_subscribed', False)}"

        if user.data.get('is_subscribed', False):
            boot['config']['weather'] = {
                'url': f"{config['WEATHER_URL']}/api/v1/geocode/$$latitude$$/$$longitude$$/?access_token={access_token}&language=$$language$$&units=$$units$$"
            }
            asr_token_req = rebble.get(f"dictation-token",)
            if asr_token_req.status == 200:
                asr_token = asr_token_req.data['token']
                boot['config']['voice']['languages'] = [{
                    'endpoint': f"{asr_token}-{code.replace('_', '-').lower()}.{config['ASR_ROOT']}",
                    'four_char_locale': code,
                    'six_char_locale': nuance_code,
                } for code, nuance_code in [
                    ('af_ZA', 'afr-SAF'),
                    ('cs-CZ', 'ces-CES'),
                    ('da_DK', 'dan-DNK'),
                    ('de_DE', 'deu-DEU'),
                    ('en_AU', 'eng-AUS'),
                    ('en_US', 'eng-USA'),
                    ('en_GB', 'eng-ENG'),
                    ('en_IN', 'eng-IND'),
                    ('en_CA', 'eng-CAN'),
                    ('fi_FI', 'fin-FIN'),
                    ('fil_PH', 'fil-PIL'),
                    ('fr_CA', 'fra-CAN'),
                    ('fr_FR', 'fra-FRA'),
                    ('gl_ES', 'gal-ESP'),
                    ('id_ID', 'bah-IND'),
                    ('is_IS', 'isl-ISL'),
                    ('it_IT', 'ita_ITA'),
                    ('ko_KR', 'kor_KOR'),
                    ('lv_LV', 'lat-LAT'),
                    ('lt_LT', 'lie-LIE'),
                    ('hr_HR', 'hrv-HRV'),
                    ('hu_HU', 'mag-MAG'),
                    ('ms_MY', 'bah-MAL'),
                    ('nl_NL', 'nld-NLD'),
                    ('nb_NO', 'nor-NOR'),
                    ('pt_PT', 'por-PRT'),
                    ('pl_PL', 'pol-POL'),
                    ('ro_RO', 'rom-ROM'),
                    ('ru_RU', 'rus-RUS'),
                    ('uk_UA', 'ukr-UKR'),
                    ('es_ES', 'spa-ESP'),
                    ('es_MX', 'spa-XLA'),
                    ('es_US', 'spa-USA'),
                    ('sk_SK', 'slk-SLK'),
                    ('sl_SL', 'sln-SLN'),
                    ('sv_SE', 'swe-SWE'),
                    ('sw_TZ', 'swa-TAN'),
                    ('sw_KE', 'swa-KEN'),
                    ('tr_TR', 'tur-TUR'),
                    ('zu-ZA', 'zul-SAF'),
                    ('cmn-Hant-TW', 'man-TAI'),
                    ('cmn-Hans-CN', 'man-CHI'),
                ]]
                boot['config']['voice']['languages'].append({
                    'endpoint': f"{asr_token}-auto-auto.{config['ASR_ROOT']}",
                    'four_char_locale': 'Auto',
                    'six_char_locale': 'ato-ATO'
                })

        overrides = user.data.get('boot_overrides', None)
        if overrides and type(overrides) == dict:
            allowed_overrides = {
                "config": {
                    "voice": True,
                    "health": True,
                    "weather": {
                        "url": True,
                        "provider_name": True
                    },
                    "webviews": {
                        "appstore/application": True,
                        "appstore/application_changelog": True, 
                        "appstore/application_share": True,
                        "appstore/developer_apps": True,
                        "appstore/search": True,
                        "appstore/search/query": True,
                        "appstore/watchapps": True,
                        "appstore/watchfaces": True
                    },
                    "treasure_data": {
                        "endpoint": True,
                        "write_key": True,
                    },
                }
            }
            
            def recur_overrides(ovr, cfg, allowed):
                for key in ovr:
                    if key not in allowed:
                        continue
                    
                    if allowed[key] == True:
                        # We could do a better job traversing downwards, I
                        # suppose.  But this will work for now.
                        if type(ovr[key]) == str:
                            cfg[key] = ovr[key].format(access_token = access_token, platform = platform)
                        else:
                            cfg[key] = ovr[key]
                    elif type(allowed[key]) == dict:
                        if key not in cfg:
                            cfg[key] = {}
                        recur_overrides(ovr[key], cfg[key], allowed[key])
                    else:
                        raise Exception("invalid override")
            
            recur_overrides(overrides, boot, allowed_overrides)

    return boot


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
    me = rebble.get(f"me/pebble/auth")
    link = f"pebble://login#access_token={request.args['access_token']}&refresh_token=null&expires_in=null&signed_eula=2015-05-01&signed_privacy_policy=2015-11-18"
    return render_template('complete-auth.html', link=link, name=me.data['name'])


def init_app(app, prefix='/api/stage2'):
    app.register_blueprint(stage2, url_prefix=prefix)
