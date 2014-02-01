from google.appengine.ext import ndb
from google.appengine.api import urlfetch
import hashlib
import webapp2
import urllib
import string
import random
from helpers import dropbox as dbx
import urlparse
import json


# Model
class Otaku(ndb.Model):

    # userid will be used as public API key
    userid = ndb.StringProperty()
    api_token = ndb.StringProperty(indexed=False)  # pytaku API private key

    dropbox_state = ndb.StringProperty(indexed=False)
    dropbox_access_token = ndb.StringProperty(indexed=False)


def generate_state():
    size = random.choice(range(20, 30))
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for x in range(size))


def pyhash(plain, salt):
    h = hashlib.sha256()
    h.update(plain + salt)
    return h.hexdigest()


class Init(webapp2.RequestHandler):

    def get(self):
        userid = self.request.get('userid')
        otaku = Otaku.query(Otaku.userid == userid).get()
        if (otaku is None):
            return  # might come up with some better way to handle this error

        state = generate_state()
        ustate = userid + '_' + state
        params = {
            'response_type': 'code',
            'client_id': dbx.consumer_key,
            'redirect_uri': 'https://pytaku.appspot.com/auth/callback',
            'state': ustate
        }
        url = dbx.authorize_url + '?' + urllib.urlencode(params)
        self.redirect(url)

        # Save state to otaku
        otaku.dropbox_state = state
        otaku.put()


class Callback(webapp2.RequestHandler):

    def get(self):
        req_params = urlparse.parse_qs(self.request.query_string)
        code = req_params['code'][0]
        userid, state = req_params['state'][0].split('_')

        otaku = Otaku.query(Otaku.userid == userid).get()
        if (otaku is None or otaku.dropbox_state != state):
            return  # might come up with some better way to handle this error

        params = {
            'code': code,
            'grant_type': 'authorization_code',
            'client_id': dbx.consumer_key,
            'client_secret': dbx.consumer_secret,
            'redirect_uri': 'https://pytaku.appspot.com/auth/callback',
        }

        url = dbx.token_url + '?' + urllib.urlencode(params)

        resp = urlfetch.fetch(url, method='POST').content
        data = json.loads(resp)
        access_token = data.get('access_token')
        if access_token is None:
            msg_params = {
                'msg': "Dropbox authorization failed!",
                'type': 'danger'
            }
        else:
            msg_params = {
                'msg': "Dropbox authorization complete!",
                'type': 'success'
            }

            otaku.dropbox_access_token = access_token
            otaku.put()

        self.redirect('/?' + urllib.urlencode(msg_params))
