import urlparse
from google.appengine.api import urlfetch


# Factory function, return instance of suitable "site" class from url
def get_site(url):
    parsed = urlparse.urlparse(url)
    if parsed.netloc == 'kissmanga.com':
        import kissmanga
        return kissmanga.Kissmanga()
    else:
        return None


# Return whole html string of the fetched url, return None if failed
def get_html(url):
    try:
        resp = urlfetch.fetch(url)
        if resp.status_code == 200:
            return resp.content
        else:
            return None
    except:
        return None
