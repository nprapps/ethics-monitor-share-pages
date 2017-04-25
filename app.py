#!/usr/bin/env python
# _*_ coding:utf-8 _*_
"""
Example application views.

Note that `render_template` is wrapped with `make_response` in all application
routes. While not necessary for most Flask apps, it is required in the
App Template for static publishing.
"""

import app_config
import logging
import oauth
import static

from flask import Flask, make_response, render_template
from num2words import num2words
from render_utils import make_context, smarty_filter, urlencode_filter
from werkzeug.debug import DebuggedApplication

app = Flask(__name__)
app.debug = app_config.DEBUG

app.add_template_filter(smarty_filter, name='smarty')
app.add_template_filter(urlencode_filter, name='urlencode')


logging.basicConfig(format=app_config.LOG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(app_config.LOG_LEVEL)

@app.route('/')
@oauth.oauth_required
def index():
    """
    Example view demonstrating rendering a simple HTML page.
    """
    context = make_context()

    return make_response(render_template('index.html', **context))

@app.route('/share/<promise>/')
@oauth.oauth_required
def share(promise):
    CATEGORY_KEY = {
        'Statement': 'have no evidence of progress.',
        'Evidence': 'have some evidence of progress.',
        'Resolution': 'have been resolved.',
        'Probation': 'are under watch for the duration of Trump\'s presidency.'
    }

    context = make_context()

    for row in context['COPY']['data']:
        if row['slug'] == promise:
            total = context['COPY']['overview_data'][row['current_status']]['value']
            context['total'] = num2words(int(total))
            context['category'] = CATEGORY_KEY[row['current_status']]
            context['promise'] = row


    return make_response(render_template('share.html', **context))

app.register_blueprint(static.static)
app.register_blueprint(oauth.oauth)

# Enable Werkzeug debug pages
if app_config.DEBUG:
    wsgi_app = DebuggedApplication(app, evalex=False)
else:
    wsgi_app = app

# Catch attempts to run the app directly
if __name__ == '__main__':
    logging.error('This command has been removed! Please run "fab app" instead!')
