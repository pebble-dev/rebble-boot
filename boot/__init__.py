try:
    import googleclouddebugger
    googleclouddebugger.enable()
except ImportError:
    pass

import time
import urllib.parse

import beeline
from beeline.patch import requests
import requests

from flask import Flask, session, redirect, url_for, render_template, request, send_from_directory
from beeline.middleware.flask import HoneyMiddleware
import werkzeug
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_sslify import SSLify

from .stage1 import init_app as init_stage1
from .stage2 import init_app as init_stage2
from .auth import rebble, init_app as init_auth
from .cobble import init_app as init_cobble
from .settings import config

app = Flask(__name__)
app.config.update(**config)
if config['HONEYCOMB_KEY']:
     beeline.init(writekey=config['HONEYCOMB_KEY'], dataset='rws', service_name='boot')
     HoneyMiddleware(app, db_events = True)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
sslify = SSLify(app, skips = ['heartbeat'])
if not app.debug:
    app.config['PREFERRED_URL_SCHEME'] = 'https'
init_stage1(app)
init_stage2(app)
init_auth(app)
init_cobble(app)

# XXX: upstream this
import beeline

@app.before_request
def before_request():
    beeline.add_context_field("route", request.endpoint)
    if session.get('access_token'):
        beeline.add_context_field("access_token", session['access_token'][-6:])

@app.route('/')
def index():
    if not session.get('access_token'):
        return redirect(url_for('auth.auth_start'))
    pebble_request = rebble.get('me/pebble/auth')

    platform = request.user_agent.platform

    is_ios = platform in ('iphone', 'ipad')
    is_android = (platform == 'android' or 'BB10' in request.user_agent.string)  # BB10 runs Pebble Android.
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
                           link=link, name=pebble_request.data['name'])

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/logout')
def logout():
    session['access_token'] = None
    return send_from_directory('templates', 'logged-out.png', mimetype='image/png', cache_timeout=0, add_etags=False)

@app.route('/heartbeat')
@app.route('/boot/heartbeat')
def heartbeat():
    return 'ok'

# XXX: This maybe ought be upstreamed to Beeline.
from wrapt import wrap_function_wrapper
import beeline
import urllib.request

def _urllibopen(_urlopen, instance, args, kwargs):
    if type(args[0]) != urllib.request.Request:
        args[0] = urllib.request.Request(args[0])
    
    span = beeline.start_span(context={"meta.type": "http_client"})
    
    b = beeline.get_beeline()
    if b:
        context = b.tracer_impl.marshal_trace_context()
        if context:
            b.log("urllib lib - adding trace context to outbound request: %s", context)
            args[0].headers['X-Honeycomb-Trace'] = context
        else:
            b.log("urllib lib - no trace context found")
    
    try:
        resp = None
        beeline.add_context({
            "name": "urllib_%s" % args[0].get_method(),
            "request.method": args[0].get_method(),
            "request.uri": args[0].full_url
        })
        resp = _urlopen(*args, **kwargs)
        return resp
    except Exception as e:
        beeline.add_context({
            "request.error_type": str(type(e)),
            "request.error": beeline.internal.stringify_exception(e),
        })
        raise
    finally:
        if resp:
            beeline.add_context_field("response.status_code", resp.status)
            content_type = resp.getheader('content-type')
            if content_type:
                beeline.add_context_field("response.content_type", content_type)
            content_length = resp.getheader('content-length')
            if content_length:
                beeline.add_context_field("response.content_length", content_length)
            
        beeline.finish_span(span)

wrap_function_wrapper('urllib.request', 'urlopen', _urllibopen)

import jinja2
def _render_template(fn, instance, args, kwargs):
    span = beeline.start_span(context = {
        "name": "jinja2_render_template",
        "template.name": instance.name or "[string]",
    })
    
    try:
        return fn(*args, **kwargs)
    finally:
        beeline.finish_span(span)

wrap_function_wrapper('jinja2', 'Template.render', _render_template)
