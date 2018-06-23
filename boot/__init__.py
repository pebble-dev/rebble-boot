import time
import urllib.parse

from flask import Flask, session, redirect, url_for, render_template, request

from .stage1 import init_app as init_stage1
from .stage2 import init_app as init_stage2
from .auth import rebble, init_app as init_auth
from .settings import config

app = Flask(__name__)
app.config.update(**config)
init_stage1(app)
init_stage2(app)
init_auth(app)


@app.route('/')
def index():
    if not session.get('access_token'):
        return redirect(url_for('auth.auth_start'))
    stuff = rebble.get('me/pebble/auth')
    if stuff.status != 200:
        return render_template('need-pebble.html')

    platform = request.user_agent.platform

    is_ios = platform in ('iphone', 'ipad')
    is_android = platform == 'android'
    os_path = ''
    if is_ios:
        os = 'ios'
        os_path = 'ios'
    elif is_android:
        os = 'android'
    else:
        os = 'pc'

    os_display = {
        'ios': 'iOS',
        'android': 'Android',
        'pc': 'PC',
    }

    url = url_for('stage2.boot_base', _external=True)
    new_path = urllib.parse.quote(f"{url}{os_path}?access_token={session['access_token']}&t={int(time.time())}", safe='')

    link = f"pebble://custom-boot-config-url/{new_path}"

    return render_template('get-started.html', os=os, os_display=os_display[os], base=f"boot.{config['DOMAIN_ROOT']}",
                           link=link, name=stuff.data['name'])
