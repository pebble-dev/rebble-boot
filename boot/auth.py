import secrets

from flask import abort, request, session, url_for, Blueprint, redirect, Response
from flask_oauthlib.client import OAuth, OAuthException

from .settings import config
import logging

oauth = OAuth()

auth_blueprint = Blueprint('auth', __name__)

def prepare_state():
    session['oauth_state'] = secrets.token_urlsafe()


def get_state():
    return session.get('oauth_state')


def validate_state():
    expected_state = session.get('oauth_state')
    if expected_state is None:
        logging.error("Missing oauth_state!")
        abort(Response(f"Your <code>oauth_state</code> is missing from your session! Ensure cookies are enabled and <a href='{url_for('.auth_start')}'>try again</a>.", 400))
    del session['oauth_state']
    if request.args.get('state') != expected_state:
        logging.error(f"Incorrect oauth_state! (expected {expected_state}, got {request.args.get('state')})")
        abort(Response(f"Your <code>state</code> is wrong! <a href='{url_for('.auth_start')}'>Try again.</a>", 400))


rebble = oauth.remote_app(
    'rebble',
    base_url=f'{config["REBBLE_AUTH_INT_URL"]}/api/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url=f'{config["REBBLE_AUTH_INT_URL"]}/oauth/token',
    authorize_url=f'{config["REBBLE_AUTH_URL"]}/oauth/authorise',
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
    try:
        resp = rebble.authorized_response()
    except OAuthException as e:
        logging.error(f"OAuth failed: {e}")
        return f"OAuth failed. <a href='{url_for('.auth_start')}'>Try again.</a>", 400
    if resp is None or resp.get('access_token') is None:
        logging.warning("Turned up with no access token.")
        return f"The authentication server rejected us. <a href='{url_for('.auth_start')}'>Try again.</a>", 401
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
