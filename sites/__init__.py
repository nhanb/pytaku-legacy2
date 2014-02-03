import urlparse
from google.appengine.api import urlfetch


# Factory function, return instance of suitable "site" class from url
def get_site(url):
    parsed = urlparse.urlparse(url)
    if parsed.netloc == 'kissmanga.com':
        import kissmanga
        return kissmanga.Kissmanga()
    elif parsed.netloc == 'www.batoto.net':
        import batoto
        return batoto.Batoto()
    else:
        return None


def available_sites(options):
    import kissmanga
    import batoto
    return [kissmanga.Kissmanga(), batoto.Batoto()]


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


# Skeleton site. If a site requires special requests (custom headers, etc.)
# then the site implementation should override these methods.
class Site:

    def fetch_manga_seed_page(self, url):
        return urlfetch.fetch(url)

    def fetch_chapter_seed_page(self, url):
        return self.fetch_manga_seed_page(url)

    def fetch_page_image(self, url):
        return self.fetch_manga_seed_page(url)
