from google.appengine.ext import ndb
import hashlib


# Model
class Otaku(ndb.Model):

    # userid will be used as public API key
    userid = ndb.StringProperty()
    api_token = ndb.StringProperty(indexed=False)  # pytaku API private key

    dropbox_req_token = ndb.StringProperty(indexed=False)
    dropbox_req_secret = ndb.StringProperty(indexed=False)
    dropbox_access_token = ndb.StringProperty(indexed=False)
    dropbox_access_secret = ndb.StringProperty(indexed=False)


def pyhash(plain, salt):
    h = hashlib.sha256()
    h.update(plain + salt)
    return h.hexdigest()
