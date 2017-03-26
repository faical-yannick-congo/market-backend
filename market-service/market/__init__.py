"""SMS Market Service module."""
import flask as fk
from marketdb.common.core import setup_app
from marketdb.common.models import Market
import tempfile
from io import StringIO
from io import BytesIO
import os
import simplejson as json
import datetime
import traceback

import requests
from datetime import date, timedelta
from functools import update_wrapper
from calendar import monthrange
import time

import glob

# Flask app instance
app = setup_app(__name__)

# The sms market service's version
SERVICE_VERSION = 0.1
# The sms market service base url
SERVICE_URL = '/sms/services/market/v{0}'.format(SERVICE_VERSION)


def service_response(code, title, content):
    """Provides a common structure to represent the response
    from any api's endpoints.
        Returns:
            Flask response with a prettified json content.
    """
    import flask as fk
    response = {'service':'sms-market', 'code':code, 'title':title, 'content':content}
    return fk.Response(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')), mimetype='application/json')

def data_pop(data=None, element=''):
    """Pop an element of a dictionary.
    """
    if data != None:
        try:
            del data[element]
        except:
            pass

def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def menu():
    return "Welcome to the Market Messaging Service. Thank you for trusting us in delivering your daily market messages."

def get_one_number(country):
    r = requests.get('http://54.196.141.56:5300/sms/services/sso/v0.1/users/country/{0}'.format(country))
    response = json.loads(r.text)
    return response['content']['users'][0]['phone']

def get_user_city(country, phone):
    r = requests.get('http://54.196.141.56:5300/sms/services/sso/v0.1/users/country/{0}'.format(country))
    response = json.loads(r.text)
    for us in response['content']['users']:
        if us["phone"] == phone:
            return us["city"]
    return None

def get_cities(country):
    r = requests.get('http://54.196.141.56:5300/sms/services/sso/v0.1/users/cities/{0}'.format(country))
    response = json.loads(r.text)
    return [c['name'] for c in response['content']['cities']], response['content']['language']

def get_country(country):
    r = requests.get('http://54.196.141.56:5300/sms/services/sso/v0.1/users/countries')
    response = json.loads(r.text)
    for cnt in response['content']['countries']:
        if int(cnt["code"]) == int(country):
            return cnt
    return None

# import all the api endpoints.
import market.endpoints
