from google.appengine.ext import ndb
import hashlib
import webapp2
import urllib
import string
import random
from helpers import dropbox as dbx


# Model
class Otaku(ndb.Model):

    # userid will be used as public API key
    userid = ndb.StringProperty()
    api_token = ndb.StringProperty(indexed=False)  # pytaku API private key

    dropbox_state = ndb.StringProperty(indexed=False)
    dropbox_req_token = ndb.StringProperty(indexed=False)
    dropbox_req_secret = ndb.StringProperty(indexed=False)
    dropbox_access_token = ndb.StringProperty(indexed=False)
    dropbox_access_secret = ndb.StringProperty(indexed=False)


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

        state = userid + '_' + generate_state()
        params = {
            'response_type': 'code',
            'client_id': dbx.consumer_key,
            'redirect_uri': 'http://localhost:8080/auth/callback',
            'state': state
        }
        url = dbx.authorize_url + '?' + urllib.urlencode(params)

        self.redirect(url)


class Callback(webapp2.RequestHandler):

    def get(self):
        self.response.write(str(self.request))
