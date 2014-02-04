import ConfigParser
import urllib
from google.appengine.api import urlfetch
import threading

config = ConfigParser.ConfigParser()
config.read("config.ini")

consumer_key = config.get("Dropbox", "ConsumerKey")
consumer_secret = config.get("Dropbox", "ConsumerSecret")
token_url = config.get("Dropbox", "TokenURL")
authorize_url = config.get("Dropbox", "AuthorizeURL")
files_put_url = 'https://api-content.dropbox.com/1/files_put/sandbox'


def upload(name, content, token):
    params = {
        'locale': 'en-US',
        'overwrite': 'true',
    }
    url = '%s/%s/?%s' % (files_put_url,
                         urllib.pathname2url(name),
                         urllib.urlencode(params))
    headers = {'Authorization': 'Bearer ' + token}

    # Make async call, returns whole rpc object
    rpc = urlfetch.create_rpc()
    urlfetch.make_fetch_call(rpc, url, content, 'PUT', headers)
    return (rpc, name, content)


def async_upload(name, content, token):
    threading.Thread(target=upload, args=(name, content, token)).start()
