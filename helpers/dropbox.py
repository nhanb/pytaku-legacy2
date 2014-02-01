import ConfigParser
import urllib
from google.appengine.api import urlfetch

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
    url = files_put_url + '/' + name + '?' + urllib.urlencode(params)
    headers = {'Authorization': 'Bearer ' + token}
    resp = urlfetch.fetch(url, content, 'PUT', headers)
    return resp.content
