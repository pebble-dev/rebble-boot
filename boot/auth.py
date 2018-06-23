import secrets

from flask import abort, request, session, url_for, Blueprint, redirect
from flask_oauthlib.client import OAuth

from .settings import config

oauth = OAuth()

auth_blueprint = Blueprint('auth', __name__)


def prepare_state():
    session['oauth_state'] = secrets.token_urlsafe()


def get_state():
    return session['oauth_state']


def validate_state():
    expected_state = session['oauth_state']
    if expected_state is None:
        abort(401)
    del session['oauth_state']
    if request.args.get('state') != expected_state:
        abort(401)


rebble = oauth.remote_app(
    'rebble',
    base_url=f'{config["REBBLE_AUTH"]}/api/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url=f'{config["REBBLE_AUTH"]}/oauth/token',
    authorize_url=f'{config["REBBLE_AUTH"]}/oauth/authorise',
    request_token_params={'scope': 'pebble_token pebble profile', 'state': get_state},
    app_key='AUTH_REBBLE',
)


@auth_blueprint.route('/')
def auth_start():
    prepare_state()
    return rebble.authorize(url_for('.auth_complete', _external=True))


@auth_blueprint.route('/complete')
def auth_complete():
    validate_state()
    resp = rebble.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Failed.'
    session['access_token'] = resp['access_token']
    return_to = session.get('return_to')
    if return_to:
        del session['return_to']
        return redirect(return_to)
    return redirect('/')


@rebble.tokengetter
def get_token():
    return request.args.get('access_token') or session.get('access_token'),


def init_app(app, prefix='/auth'):
    app.register_blueprint(auth_blueprint, url_prefix=prefix)